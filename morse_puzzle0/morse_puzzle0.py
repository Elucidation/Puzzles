# Encodes the original raw message into a gif
# Each frame of the gif contains a clock signal in pixel 0,0 and the message
# in all other pixels
import imageio
import numpy as np
import sys
sys.path.append('../libs')
import morse

raw_msg = "HELLO AGENT ELIZABETH BURL. YOUR BOYFRIEND THINKS YOU ARE PRETTY CUTE"

# convert raw message to morse string
morse_msg = morse.writeMorse(raw_msg)
print(raw_msg)
print(morse_msg)

# Turn morse character into 3-bit binary sequences
def morseCharToBits(c):
  if c == '.':
    return [1,0,0]
  elif c == '-':
    return [1,1,0]
  elif c == ' ':
    return [0,0,0]
  else:
    raise('Unexpected Char')

data = map(morseCharToBits, morse_msg)
data = np.array(data, dtype=np.uint8).flatten()
# Turn processed message into binary string, where each trie is one character


# Build gif writer
writer = imageio.get_writer('burl_puzzle0.gif', fps=10)

# Turn 1's to 255
msg_data = np.array([int(x)*255 for x in data], dtype=np.uint8)

# Create a clock signal on gif image pixel 0,0
# clock signal is just 100, then 0, then 0, repeating consistently
# this should theoretically make it simpler to figure out timing of the 
# message pixel
clock = np.tile(np.array([100,0,0],dtype=np.uint8), len(msg_data)/3)

# write each bit of the message data to all pixels per unit time
data = np.tile(msg_data, [16,16,1])

# replace pixel 0,0 with the clock value, per unit time
data[0,0,:] = clock

# 1 column, 2 rows, 717 deep frames
# 1x2x717
print(data.shape)

# Write to gif
for i in range(data.shape[2]):
    writer.append_data(data[:, :, i])
writer.close()