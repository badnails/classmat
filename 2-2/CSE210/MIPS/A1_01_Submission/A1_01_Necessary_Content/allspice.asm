# ==========================================
# INITIALIZATION
# ==========================================
# Assuming $t0 starts with garbage, we can clear it by subtracting it from itself.
sub  $t0, $t0, $t0      # $t0 = 0 (Clears register)

# ==========================================
# ARITHMETIC INSTRUCTIONS (A, B, C, D)
# Testing basic arithmetic and negative immediates within 4-bit limits (-8 to +7)
# ==========================================
addi $t1, $t0, 3        # (B) $t1 = 0 + 3 = 3
addi $t2, $t0, -2       # (B) $t2 = 0 + (-2) = -2 (Testing negative number)

add  $t3, $t1, $t2      # (A) $t3 = 3 + (-2) = 1
sub  $t4, $t1, $t2      # (C) $t4 = 3 - (-2) = 5
subi $t3, $t4, 7        # (D) $t3 = 5 - 7 = -2 (Testing subi and negative result)

# ==========================================
# LOGIC INSTRUCTIONS (E, F, G, H, I, J, K)
# Operating on 4-bit binary values
# ==========================================
# Current state: $t1 = 3 (0011), $t2 = -2 (1110)
and  $t3, $t1, $t2      # (E) $t3 = 0011 & 1110 = 0010 (2)
andi $t4, $t1, 5        # (F) $t4 = 0011 & 0101 = 0001 (1)

or   $t3, $t1, $t2      # (G) $t3 = 0011 | 1110 = 1111 (-1)
ori  $t4, $t1, -4       # (H) $t4 = 0011 | 1100 = 1111 (-1)

sll  $t3, $t1, 1        # (I) $t3 = 0011 << 1 = 0110 (6)
srl  $t4, $t1, 1        # (J) $t4 = 0011 >> 1 = 0001 (1)

nor  $t3, $t1, $t0      # (K) $t3 = ~(0011 | 0000) = 1100 (-4)

# ==========================================
# MEMORY INSTRUCTIONS (L, M)
# Testing stack pointer ($sp) with positive and negative offsets
# ==========================================
sw   $t1, 4($sp)        # (M) Store $t1 (3) at positive offset 4
sw   $t2, -4($sp)       # (M) Store $t2 (-2) at negative offset -4 (Testing negative offset)

lw   $t3, 4($sp)        # (L) Load the value from offset 4 into $t3
lw   $t4, -4($sp)       # (L) Load the value from offset -4 into $t4

# ==========================================
# CONTROL INSTRUCTIONS (N, O, P)
# Testing branching and jumping
# ==========================================
addi $t1, $t0, 1        # $t1 = 1
addi $t2, $t0, 1        # $t2 = 1

beq  $t1, $t2, branch1  # (N) 1 == 1, so it WILL branch
sub  $t0, $t0, $t0      # (Skipped instruction)

branch1:
addi $t2, $t0, -3       # $t2 = -3
bneq $t1, $t2, branch2  # (O) 1 != -3, so it WILL branch
sub  $t0, $t0, $t0      # (Skipped instruction)

branch2:
j    end                # (P) Unconditional jump to end
sub  $t0, $t0, $t0      # (Skipped instruction)

end:
j branch2
# End of test program