# Encodes the original raw message into a gif
# Each frame of the gif contains a clock signal in pixel 0,0 and the message
# in all other pixels
import imageio
import numpy as np

import sys
sys.path.append('../libs')
import morse

# Load original image
im = imageio.imread('burl_puzzle1.png')

# The image itself highlights the first 5 fragments, which appear to be pairs
# of pixels. We see the top pixel red and green value is constant in all 5, and
# the text says "Found by red and green", suggesting that all the fragments will
# have a pixel with RG values of red=51 and green=8.

# The blue pixel increments from 0 to 4 and the text says 
# "only with blue shall the true succession be revealed", suggesting this is
# the ordering for all the fragments, starting at 0.

# So first, let's search for all pixel coordinates that have RG values of
# 51 and 8

pixel_coords = np.argwhere(np.logical_and(im[:,:,0]==51,im[:,:,1]==8))
# print(pixel_coords)
# print(pixel_coords.shape)

# Then lets take the green values to get the sequence of the fragments
sequence = im[pixel_coords[:,0],pixel_coords[:,1]][:,2]

# We can confirm from this that there are 187 fragments ordered from 0-186
assert(sorted(sequence) == range(len(sequence)))
# [0,1,2,3,...185,186]

# Then we get the index ordering based off of the sorted version of these values
order = np.argsort(sequence)

# Now we noticed that the highlighted fragments contained two pixels, and we
# used the top one, let's see what the bottom ones look like, lets look at
# the first 5 pixels (in no particular order)
print(im[pixel_coords[:,0]+1,pixel_coords[:,1]][:5])
# [[50 50  0]
#  [50  0  0]
#  [50  0  0]
#  [ 0  0  0]
#  [50  0  0]]
# ...
# They appear to be only 50's and 0's, with the same trie form from the previous
# puzzle. Suggesting that they are dots, dashes, and spaces. 

# Let's get all of the fragments and put them in the correct order
# We'll also turn all the 50's to 1's
data = im[pixel_coords[:,0]+1,pixel_coords[:,1]][order] / 50

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
morse_msg = ''.join(map(lambda x: bitsToMorseChar(list(x)), data))
print(morse_msg)

# We then use our original morse code to ascii convertor to get the original msg
raw_msg = morse.readMorse(morse_msg)
print(raw_msg)