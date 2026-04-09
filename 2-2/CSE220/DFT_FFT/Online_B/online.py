import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from discrete_framework import DiscreteSignal, DFTAnalyzer, FastFourierTransform


image = Image.open("encrypted_image.tiff")

# Convert the image to a NumPy array
encrypted_image = np.array(image)

plt.figure(figsize=(8, 6))

# Encrypted image
plt.subplot(1, 2, 1)
plt.imshow(encrypted_image, cmap='gray')
plt.title("Encrypted Image")
plt.axis('off')


k = DiscreteSignal(encrypted_image[132])

dan = FastFourierTransform()
K = dan.compute_dft(k)
e = 1e-15
print(e)

decrypted_image = np.zeros_like(encrypted_image)

for n in range(256):
    D = dan.compute_dft(DiscreteSignal(encrypted_image[n, :]))
    temp_X = D/K+e

    decrypted_image[n] = np.real(dan.compute_idft(temp_X))

decrypted_image[132] = encrypted_image[132]



# Decrypted image
plt.subplot(1, 2, 2)
plt.imshow(decrypted_image, cmap='gray')
plt.title("Decrypted Image")
plt.axis('off')

plt.show()