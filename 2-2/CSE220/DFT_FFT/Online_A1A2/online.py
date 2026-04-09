
import numpy as np
from discrete_framework import DiscreteSignal, FastFourierTransform
# Example usage
x = 657678797979071234567899876543234567887654323456789
y = 76545453243543534576543454698765432123456789098712345678976542234567897652345678

dan = FastFourierTransform()

#converting to digit arrays(discrete signal)
x_digits = [int(digit) for digit in str(x)][::-1]

y_digits = [int(digit) for digit in str(y)][::-1]

size = 1<<(len(x_digits) + len(y_digits) -1).bit_length()
print(size)
dx = DiscreteSignal(x_digits)
dx = dx.pad(size)

dy = DiscreteSignal(y_digits)
dy = dy.pad(size)

X = dan.compute_dft(dx)
Y = dan.compute_dft(dy)

Z = np.multiply(X, Y)

z = dan.compute_idft(Z)
print(z)

z = np.round(np.real(z)).astype(int)
print(z)

result_digits = []
carry = 0
for i in range(size):
    total = z[i] + carry
    result_digits.append(total % 10)
    carry = total // 10

# Add remaining carry if any
while carry:
    result_digits.append(carry % 10)
    carry //= 10

# 8. Convert back to an integer
# Reverse back to join digits in correct order
fin = int("".join(map(str, result_digits[::-1])))

print(f"FFT Result: {fin}")
print(f"Python Result: {x * y}")
print(f"Match: {fin == x * y}")