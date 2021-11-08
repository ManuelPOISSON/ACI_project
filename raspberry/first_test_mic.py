import time
from datetime import datetime
from typing import List, Union, Any

import pyaudio
import struct
import math
import signal
import requests
import os

# We are going to measure the root mean square RMS Amplitude for the noise
# The RMS is calculated by the square root of the average of the squares of the individual samples 
# We need to simulate the Sinusoidal Waveform somehow
# We are going to iniate a threshold which is going to decide who is the noisy block and the quite block
# If the block's RMS amplitude is greater than this threshold, it's a noisy block, if not a quite one


format_audio = pyaudio.paInt16  # 16-bit resolution
channel = 1  # 1 channel
samp_rate = 44100  # 44.1kHz sampling rate
input_block_time = 0.05  # we are going to read a block of samples at a time, let's say 0.05 seconds
input_frames_per_block = int(samp_rate * input_block_time)

dev_index = 1  # device index found by p.get_device_info_by_index() (from the pyaudio library)


# p = pyaudio.PyAudio()
# for i in range(p.get_device_count()):
#    print(p.get_device_info_by_index(i))

def get_rms(block):
    # We need to convert this string of bytes (block) into 
    # a string of 16-bit samples
    count = len(block) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, block)
    # iterate over the block.
    ms = 0.0
    for sample in shorts:
        # Normalizing sample to 1.0 
        sample = sample * (1.0 / 32768)
        ms += sample * sample
    ms = ms / count
    rms = math.sqrt(ms)
    return rms


def format_data(noise_level_data) -> str:
    formatted_data = []
    for date, noise_amplitude in noise_level_data:
        formatted_data.append([date.strftime("%Y-%m-%d %H:%M:%S.%f"), noise_amplitude])
    return str(formatted_data).replace("'", '"').replace(", ", ",")


def post_noise_to_db(rasp_id: int, coord_id: int, noise_level: List[List[Union[Any, float]]]):
    data = format_data(noise_level)
    baseurl = f"http://{os.getenv('IP_SERVER')}:8000"
    route = "/data"
    try:
        response = requests.post(
            f"{baseurl}{route}?raspberry_id={rasp_id}&location_id={coord_id}",
            headers={
                'Content-Type': 'application/json',
                'accept': 'application/json'},
            data=data
        )
        print("send measurements to server")
        # print(response.text)
    except Exception as e:
        print(f"error when using POST: {e}")
        print(f"data was {data}\nnoise_level was {noise_level}\n", "="*20)


# Initiating pyaudio stream for the Microphone
audio = pyaudio.PyAudio()

# creating pyaudio stream
stream = audio.open(format=format_audio, rate=samp_rate, channels=channel, input_device_index=dev_index, input=True,
                    frames_per_buffer=input_frames_per_block)

# Threshold - variable for noise detection
threshold = 0.010  # just trying

# Manage Ctrl+C terminaison
terminate = False


def signal_handling(signum, frame):
    global terminate
    terminate = True


signal.signal(signal.SIGINT, signal_handling)

noise_amplitudes = []
# Start Listening
while not terminate:
    # gathering data
    block = stream.read(input_frames_per_block, exception_on_overflow=False)
    amplitude = get_rms(block)
    noise_amplitudes.append([datetime.now(), amplitude * 80])  # multiply by 80 to amplify variations
    print(f"data mesured : \n")
    for elem in noise_amplitudes:
        print(elem)
    print("="*30)
    if len(noise_amplitudes) == 20:
        # Send Post to a server
        post_noise_to_db(int(os.getenv("RASPBERRY_ID")), int(os.getenv("COORDINATES_ID")), noise_amplitudes)
        noise_amplitudes = []

    time.sleep(2)

print("Bye")
