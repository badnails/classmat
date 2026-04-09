
addi $t1, $zero, 4      # limit = 4
addi $t2, $zero, 0      # index = 0
addi $t0, $zero, 1      # value = 1 (We will 4 integers from 0)

# ================================
# PHASE 1: STORE ARRAY [1,2,3,4]
# ================================

store_loop:
    sw   $t0, 0($t2)        # MEM[0] = 1; MEM[1] = 2; MEM[2] = 3; MEM[3] = 4;
    addi $t2, $t2, 1
    addi $t0, $t0, 1
    bneq  $t2, $t1, store_loop

# ================================
# PHASE 2 & 3: REVERSE VIA STACK
# ================================
addi $t2, $zero, 0
push_loop:                  # MEM[15] = 1, MEM[14] = 2, MEM[13] = 3, MEM[12] = 4
    lw   $t3, 0($t2)
    sw   $t3, 0($sp)
    subi $sp, $sp, 1
    addi $t2, $t2, 1
    bneq  $t2, $t1, push_loop

addi $t2, $zero, 0
pop_loop:                 # MEM[4] = 4, MEM[5] = 3, MEM[6] = 2, MEM[7] = 1  
    addi $sp, $sp, 1
    lw   $t3, 0($sp)
    sw   $t3, 4($t2)
    addi $t2, $t2, 1
    bneq  $t2, $t1, pop_loop

# ================================
# PHASE 4: SUM (Result will be 10)
# ================================
addi $t2, $zero, 0
addi $t0, $zero, 0      # $t0 is now SUM

sum_loop:
    lw   $t3, 4($t2)
    add  $t0, $t0, $t3  
    addi $t2, $t2, 1
    bneq  $t2, $t1, sum_loop