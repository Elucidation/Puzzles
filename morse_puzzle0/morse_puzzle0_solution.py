# Decodes a gif back into the original raw message
import imageio
import numpy as np
import morse

# Build gif reader
reader = imageio.get_reader('burl_puzzle0.gif')
print(reader.get_meta_data())
nframes = reader.get_length()
# width, height = reader.get_meta_data()['size']
width, height = reader.get_data(0).shape # Get shape from first frame

# Turn gif into 3d matrix containing all pixel data, feasible for such
# small data sizes as these
data = np.zeros([width, height, nframes], dtype=np.uint8)

# Read data in from gif
for i, im in enumerate(reader):
  data[:,:,i] = im

# Since pixel 0,0 only contains clock signal, we can ignore it as we know it
# is telling us that every char consists of 3 bits

# Instead, we just look at pixel 0,1 (or any other pixel) and over all frames
# to get the entire encoded message
print(data[0,1,:]/255)

# We reshape the flat sequence into 3-bit tries for easy processing
bit_seq = np.reshape(data[0,1,:]/255, [-1,3])

def bitsToMorseChar(bits):
  if bits == [1,0,0]:
    return '.'
  elif bits == [1,1,0]:
    return '-'
  elif bits == [0,0,0]:
    return ' '
  else:
    raise('Unexpected sequence')

# We then map each 3-bit trie using bitsToMorseChar to convert back to 
# a morse code sequence.
morse_msg = ''.join(map(lambda x: bitsToMorseChar(list(x)), bit_seq))
print(morse_msg)

# We then use our original morse code to ascii convertor to get the original msg
raw_msg = morse.readMorse(morse_msg)
print(raw_msg)