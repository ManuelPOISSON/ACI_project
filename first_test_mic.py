import pyaudio
import struct
import math

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



# Initiating pyaudio stream for the Microphone

audio = pyaudio.PyAudio()

# creating pyaudio stream
stream = audio.open(format = format_audio, rate = samp_rate, channels = channel, input_device_index = dev_index, input = True, frames_per_buffer = input_frames_per_block)


# Threshold - variable for noise detecting 

threshold = 0.010 # just trying 

# Start Listening

amps = []

while True:

    # gathering data
    block = stream.read(input_frames_per_block)         
    amplitude = get_rms(block)
    amps.append(amplitude)
    # print(amplitude)
 
    #Send Post to a server , error handling 

    if amplitude > threshold: # if greater -> noise  
        print("Noise")

    else: # Else , it's quite
        print("Quite")



 
