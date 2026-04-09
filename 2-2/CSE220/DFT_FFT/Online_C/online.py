import numpy as np
import matplotlib.pyplot as plt
from discrete_framework import DiscreteSignal, FastFourierTransform

#implement the necessary functions here

def cross_correlate(o, s):
    dan = FastFourierTransform()
    O = dan.compute_dft(o)
    S = dan.compute_dft(s)
    C = O * np.conjugate(S)
    c = dan.compute_idft(C)
    N = len(c)
    temp = np.argmax(np.abs(c))
    
    if(temp>N//2):
        return temp - N
    else:
        return temp

image = plt.imread("image.png")
shifted_image = plt.imread("shifted_image.png")

o_col = np.argmax(np.sum(image, axis=0))
s_col = np.argmax(np.sum(shifted_image, axis=0))

o_row = np.argmax(np.sum(image, axis=1))
s_row = np.argmax(np.sum(shifted_image, axis=1))

print(f"{o_col} {o_row}")
print(f"{s_col} {s_row}")

o_r = image[o_row, :]
s_r = shifted_image[s_row, :]

o_c = image[:, o_col]
s_c = shifted_image[:, s_col]

dx = cross_correlate(o_r, s_r)
dy = cross_correlate(o_c, s_c)

print(dx)
print(dy)

reversed_shifted_image = np.roll(shifted_image, dx, axis = 1)
reversed_shifted_image = np.roll(reversed_shifted_image, dy, axis = 0)

plt.figure(figsize=(12, 8))

# Original Image
plt.subplot(2, 3, 1)
plt.imshow(image, cmap='gray')
plt.title("Original Image")
plt.axis('off')

# Shifted Image
plt.subplot(2, 3, 2)
plt.imshow(shifted_image, cmap='gray')
plt.title(f"Shifted Image")
plt.axis('off')


# Reversed Shifted Image
plt.subplot(2, 3, 3)
plt.imshow(reversed_shifted_image, cmap='gray')
plt.title("Reversed Shifted Image")
plt.axis('off')

plt.tight_layout()
plt.show()
