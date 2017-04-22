# Encodes the original raw message into a gif
# Each frame of the gif contains a clock signal in pixel 0,0 and the message
# in all other pixels
import imageio
import numpy as np

import sys
sys.path.append('../libs')
import morse

np.random.seed(8008)
# Generate morse code
raw_msg = "CONGRATULATIONS AGENT BURL. YOU HAVE PASSED PUZZLE 1."

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
data = np.array(data, dtype=np.uint8)*50
N = data.shape[0]
print("There are %d fragments" % N)

print(data.shape)

# Load original image
im = imageio.imread('burl_puzzle1_input.jpg').astype(np.float)
# print(im.shape)
# Add random noise to the image
warp_im = im*(0.2+0.8*np.random.random(im.shape))

# The idea now is to choose N random pixel-pair coords
# in the picture to store the morse bits, we'll use the first
# pixel to be a labeled index with RGB value [51,8,i] where
# i is the index of the bit in the morse sequence. This was manually
# chosen since pixels with Red and Green values of 51 and 8 don't exist in the
# image, making it acceptable as an indexer


# Add morse code index
e = np.matrix(np.arange(N)).T
e_data = np.hstack([np.tile([51,8],[N,1]), e, data])
# print(e_data[-10:,:])

# Choose random locations, since we don't want pairs to overlap
# Or be on the bottom edge of the screen, we choose randomly
# from (height-1)/2 and then double so we always choose even indices
# not including the far edge
p_row = np.random.choice((warp_im.shape[0]-1)/2, N, replace=False)*2
p_col = np.random.choice(warp_im.shape[1], N, replace=False)


# Remove rest of image for testing
# warp_im[:,:,:] = 0

# Add golden highlight around first few coordinates
for i in range(5):
  warp_im[p_row[i]-1:p_row[i]+3,p_col[i]-1:p_col[i]+2] = [243,183,0]
# First 3 rows and cols, corresponding to Y and X in the image
# 282, 396, 332
# 319,  40, 564


# Add index pixel
warp_im[p_row, p_col,:] = e_data[:,:3]

# Then, the pixel adjacent directly below the index pixel contains the RGB value
# that corresponds to the morse code bit where 255 = 1
warp_im[p_row+1, p_col,:] = e_data[:,3:]
print(e_data[-10:,3:])

# Write final encoded image out
warp_im = warp_im.astype(np.uint8)
imageio.imwrite('burl_puzzle1.png', warp_im)

# Confirm that the number of indexed pixels is the same as the number of morse
# bits, meaning the message can be differentiated from the background image
print("Indexed pixels %d vs %d" % (np.sum(np.logical_and(warp_im[:,:,0] == 51, warp_im[:,:, 1] == 8)), N))
assert(N == np.sum(np.logical_and(warp_im[:,:,0] == 51, warp_im[:,:, 1] == 8)))
print("Message is safe")