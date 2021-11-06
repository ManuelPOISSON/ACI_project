import pyaudio
import struct
import math
import signal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# We are going to measure the root mean square RMS Amplitude for the noise 
# The RMS is calculated by the square root of the average of the squares of the individual samples 
# We need to simulate the Sinusoidal Waveform somehow
# We are going to iniate a threshold which is going to decide who is the noisy block and the quite block
# If the block's RMS aplitude is greater than this threshold, it's a noisy block, if not a quite one 

format_audio = pyaudio.paInt16 # 16-bit resolution
channel = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
input_block_time = 0.05 # we are going to read a block of samples at a time, let's say 0.05 seconds
input_frames_per_block = int(samp_rate*input_block_time) 

dev_index = 1 # device index found by p.get_device_info_by_index() (from the pyaudio library)
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#p = pyaudio.PyAudio()
#for i in range(p.get_device_count()):
#    print(p.get_device_info_by_index(i))

def get_rms(block):
    # We need to convert this string of bytes (block) into 
    # a string of 16-bit samples
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack(format, block)
    # iterate over the block.
    ms = 0.0
    for sample in shorts:
        # Normalizing sample to 1.0 
        sample = sample * (1.0/32768)
        ms += sample*sample
    ms = ms / count 
    rms = math.sqrt(ms)
    return rms

@app.post("/")
def send_amplitude_to_server(device_id: int, amplitude):
    return {
        "dev_id": device_id,
        "amplitude": amplitude
    }


# Initiating pyaudio stream for the Microphone
audio = pyaudio.PyAudio()

# creating pyaudio stream
stream = audio.open(format = format_audio, rate = samp_rate, channels = channel, input_device_index = dev_index, input = True, frames_per_buffer = input_frames_per_block)


# Threshold - variable for noise detecting
threshold = 0.010 # just trying 

# Manage Ctrl+C terminaison
terminate = False
def signal_handling(signum, frame):
    global terminate
    terminate = True

signal.signal(signal.SIGINT, signal_handling)

# Start Listening
while not terminate:
    # gathering data
    block = stream.read(input_frames_per_block, exception_on_overflow=False)         
    amplitude = get_rms(block)
    print(amplitude)

    # Send Post to a server, error handling 

    if amplitude > threshold: # if greater -> noise  
        print("Noise", flush=True)
    else: # Else, it's quite
        print("Quite", flush=True)

print("Bye")
