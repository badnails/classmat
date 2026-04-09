#!/usr/bin/env python3
"""
4-bit MIPS Assembler (CSE 210 July 2025)
- Instruction width: 16 bits
- Formats:
  R: opcode(4) rs(4) rt(4) rd(4)
  S: opcode(4) rs(4) rd(4) shamt(4)
  I: opcode(4) rs(4) rt/rd(4) imm/addr(4)
  J: opcode(4) target(8) 0000

Supports labels:
  - beq/bneq use 4-bit signed PC-relative offset: (label_addr - (pc+1))
    If offset is out of range [-8..7], a branch-over-jump is emitted instead:
      <inverted_branch> rs, rt, +1   ; skip the jump
      j <target>
  - j uses 8-bit absolute instruction address (0..255)

Pseudo-instructions:
  push $rt   ->  sw $rt, 0($sp)      store register to top of stack
                 addi $sp, $sp, -1   decrement stack pointer

  pop $rt    ->  addi $sp, $sp, 1    increment stack pointer
                 lw $rt, 0($sp)      load from top of stack

Register set (4-bit codes):
  $zero=0, $t0=1, $t1=2, $t2=3, $t3=4, $t4=5, $sp=6

Usage:
  python asm4bit_mips.py input.asm [output.rom.txt]
Outputs:
  - prints machine code as: address : binary  hex  ; original/expanded line
  - writes Logisim Evolution ROM image
"""

import re
import sys

# ---------------------------
# 1) Your lab group's opcode mapping
# Sequence gives opcode 0..15 by order of instruction IDs in that sequence.
# Instruction IDs A..P correspond to:
# A add, B addi, C sub, D subi, E and, F andi, G or, H ori, I sll, J srl,
# K nor, L lw, M sw, N beq, O bneq, P j
# ---------------------------
LAB_GROUP_SEQUENCE = "GACONMPDLEJBHKFI"  # user-provided

ID_TO_MNEMONIC = {
    "A": "add",
    "B": "addi",
    "C": "sub",
    "D": "subi",
    "E": "and",
    "F": "andi",
    "G": "or",
    "H": "ori",
    "I": "sll",
    "J": "srl",
    "K": "nor",
    "L": "lw",
    "M": "sw",
    "N": "beq",
    "O": "bneq",
    "P": "j",
}

MNEMONIC_TO_ID = {v: k for k, v in ID_TO_MNEMONIC.items()}

def build_opcode_map(seq: str):
    if len(seq) != 16:
        raise ValueError("Opcode sequence must be length 16.")
    op = {}
    for opcode_value, instr_id in enumerate(seq):
        if instr_id not in ID_TO_MNEMONIC:
            raise ValueError(f"Invalid instruction ID in sequence: {instr_id}")
        mnemonic = ID_TO_MNEMONIC[instr_id]
        op[mnemonic] = opcode_value
    return op

OPCODE = build_opcode_map(LAB_GROUP_SEQUENCE)

# ---------------------------
# 2) Register encoding
# ---------------------------
REG = {
    "$zero": 0,
    "$0":    0,   # alias for $zero
    "$t0": 1,
    "$t1": 2,
    "$t2": 3,
    "$t3": 4,
    "$t4": 5,
    "$sp": 6,     # stack pointer (used by push/pop)
}

# ---------------------------
# 3) Helpers: number parsing + bit packing
# ---------------------------
def to_uint(value: int, bits: int) -> int:
    """Mask into unsigned range."""
    mask = (1 << bits) - 1
    return value & mask

def to_sint4(value: int) -> int:
    """Convert signed integer into 4-bit two's complement."""
    if not (-8 <= value <= 7):
        raise ValueError(f"4-bit signed immediate out of range [-8..7]: {value}")
    return to_uint(value, 4)

def parse_imm(token: str) -> int:
    """Parse decimal or hex immediate: 7, -3, 0xA, -0x2."""
    token = token.strip()
    neg = token.startswith("-")
    if neg:
        token2 = token[1:]
    else:
        token2 = token

    if token2.lower().startswith("0x"):
        val = int(token2, 16)
    else:
        val = int(token2, 10)

    return -val if neg else val

def pack_R(op, rs, rt, rd) -> int:
    return (op << 12) | (rs << 8) | (rt << 4) | rd

def pack_S(op, rs, rd, shamt) -> int:
    return (op << 12) | (rs << 8) | (rd << 4) | shamt

def pack_I(op, rs, rt, imm4) -> int:
    return (op << 12) | (rs << 8) | (rt << 4) | imm4

def pack_J(op, target8) -> int:
    return (op << 12) | (target8 << 4)  # low 4 bits are 0

def bin16(x: int) -> str:
    return format(x & 0xFFFF, "016b")

def hex4(x: int) -> str:
    return format(x & 0xFFFF, "04X")

# ---------------------------
# 4) Parsing lines
# ---------------------------
COMMENT_RE = re.compile(r"(?://|[#;]).*$")  # supports //, #, and ; comments

def clean_line(line: str) -> str:
    line = COMMENT_RE.sub("", line)
    return line.strip()

LABEL_RE = re.compile(r"^([A-Za-z_]\w*):\s*(.*)$")

def tokenize_operands(s: str):
    # split by commas and whitespace
    parts = [p.strip() for p in re.split(r"[,\s]+", s.strip()) if p.strip()]
    return parts

MEM_RE = re.compile(r"^(-?(?:0x[0-9A-Fa-f]+|\d+))\s*\(\s*(\$[A-Za-z0-9]+)\s*\)$")

# Pseudo-instructions and the number of real instructions each expands to.
PSEUDO_SIZES = {
    "push": 2,   # sw $rt, 0($sp)  +  addi $sp, $sp, -1
    "pop":  2,   # addi $sp, $sp, 1  +  lw $rt, 0($sp)
}

# Branch inversion table for long-branch expansion.
BRANCH_INVERT = {
    "beq":  "bneq",
    "bneq": "beq",
}

# ---------------------------
# 5) Pre-expansion pass
#    Expands pseudo-instructions into their real instruction sequences so that
#    labels are assigned correct PC values before encoding begins.
#
#    Each entry in the returned list is a tuple:
#      (original_source_line, display_label, mnemonic, operands)
#
#    'original_source_line' is passed through to the console listing.
#    'display_label' is a short annotation shown in the listing, e.g.
#      "[push $t0 #1/2]" for the first expanded instruction of a push.
# ---------------------------
def pre_expand(lines):
    """
    Returns:
        labels  : dict {name -> pc}
        expanded: list of (src_line, display, mnemonic, operands_list)
    """
    labels   = {}
    expanded = []
    pc       = 0

    for raw in lines:
        original = raw.rstrip("\n")
        cl = clean_line(original)
        if not cl:
            continue

        # Strip label prefix
        m = LABEL_RE.match(cl)
        if m:
            label = m.group(1)
            rest  = m.group(2).strip()
            if label in labels:
                raise ValueError(f"Duplicate label: {label}")
            labels[label] = pc
            cl = rest
            if not cl:
                continue

        toks     = tokenize_operands(cl)
        mnemonic = toks[0].lower()
        operands = toks[1:]

        if mnemonic == "push":
            # push $rt  ->
            #   [0] sw $rt, 0($sp)
            #   [1] addi $sp, $sp, -1
            if len(operands) != 1:
                raise ValueError(f"push expects 1 operand (register), got: {cl}")
            rt = operands[0]
            src = original
            expanded.append((src, f"[push {rt} 1/2] sw {rt}, 0($sp)",  "sw",   [rt, "0($sp)"]))
            expanded.append((src, f"[push {rt} 2/2] addi $sp, $sp, -1","addi", ["$sp", "$sp", "-1"]))
            pc += 2

        elif mnemonic == "pop":
            # pop $rt  ->
            #   [0] addi $sp, $sp, 1
            #   [1] lw $rt, 0($sp)
            if len(operands) != 1:
                raise ValueError(f"pop expects 1 operand (register), got: {cl}")
            rt = operands[0]
            src = original
            expanded.append((src, f"[pop {rt} 1/2] addi $sp, $sp, 1", "addi", ["$sp", "$sp", "1"]))
            expanded.append((src, f"[pop {rt} 2/2] lw {rt}, 0($sp)",  "lw",   [rt, "0($sp)"]))
            pc += 2

        else:
            # Normal instruction — keep as-is; branch expansion happens in pass 2
            # because we need to know the final PC of the target label first.
            expanded.append((original, cl, mnemonic, operands))
            pc += 1

    return labels, expanded


# ---------------------------
# 6) Branch expansion sizing
#    Branches whose offset would exceed [-8..7] need 2 slots (branch + jump).
#    We must iterate until slot assignments stabilise (rare but correct).
# ---------------------------
def resolve_sizes(labels_initial, expanded):
    """
    Compute final sizes for every entry in `expanded`, accounting for
    long-branch expansion.  Returns (labels, sizes) where sizes[i] is 1 or 2.

    Iterates until stable because expanding a branch can shift labels and
    cause other branches to cross the threshold.
    """
    n = len(expanded)
    sizes = [1] * n

    for _iteration in range(n + 1):          # bounded; converges in O(n) rounds
        # Recompute PC offsets from current sizes
        pc_of = []
        cur = 0
        for s in sizes:
            pc_of.append(cur)
            cur += s

        # Rebuild label map with updated PCs
        labels = dict(labels_initial)        # start fresh (labels set in pre_expand)
        # (Labels were captured at pre-expansion time with pc_of values from
        # that pass.  We need to re-derive them using current sizes.)
        # Re-derive labels by replaying the original source ordering.
        # We stored them in labels_initial keyed to their pre-expansion index;
        # here we just recompute from pc_of directly.
        # Actually labels_initial maps name->index-in-expanded-list.
        # Remap to actual PC.
        labels = {name: pc_of[idx] for name, idx in labels_initial.items()}

        new_sizes = list(sizes)
        for i, (src, display, mnemonic, operands) in enumerate(expanded):
            if mnemonic not in ("beq", "bneq"):
                continue
            if len(operands) != 3:
                continue
            _, _, target = operands
            if target not in labels:
                # Raw immediate — check range
                try:
                    off = parse_imm(target)
                except ValueError:
                    continue
                new_sizes[i] = 1 if -8 <= off <= 7 else 2
            else:
                branch_pc = pc_of[i]
                target_pc = labels[target]
                # offset computed as if this slot is size-1 (branch only)
                off = target_pc - (branch_pc + 1)
                new_sizes[i] = 1 if -8 <= off <= 7 else 2

        if new_sizes == sizes:
            break
        sizes = new_sizes
    else:
        raise RuntimeError("Branch size resolution did not converge.")

    # Final label map
    pc_of = []
    cur = 0
    for s in sizes:
        pc_of.append(cur)
        cur += s
    labels = {name: pc_of[idx] for name, idx in labels_initial.items()}

    return labels, sizes, pc_of


# ---------------------------
# 7) Label-index map builder
#    Returns {label_name -> index_in_expanded} so resolve_sizes can remap.
# ---------------------------
def build_label_index_map(lines):
    """
    Replay the source lines to capture {label_name -> index-in-expanded-list}.
    This is needed because pre_expand only gives us the expanded list, and
    resolve_sizes needs to remap label PCs as slot sizes change.
    """
    label_index = {}
    idx = 0   # index into expanded list

    for raw in lines:
        original = raw.rstrip("\n")
        cl = clean_line(original)
        if not cl:
            continue

        m = LABEL_RE.match(cl)
        label_here = None
        if m:
            label_here = m.group(1)
            cl = m.group(2).strip()
            if not cl:
                if label_here:
                    label_index[label_here] = idx
                continue

        toks     = tokenize_operands(cl)
        mnemonic = toks[0].lower()

        if label_here:
            label_index[label_here] = idx

        if mnemonic in PSEUDO_SIZES:
            idx += PSEUDO_SIZES[mnemonic]
        else:
            idx += 1

    return label_index


# ---------------------------
# 8) Two-pass assembler
# ---------------------------
def assemble(lines):
    # ---- Pre-expansion pass (expands push/pop) ----
    _labels_pre, expanded = pre_expand(lines)

    # ---- Build label-to-expanded-index map ----
    label_index = build_label_index_map(lines)

    # ---- Resolve sizes (handles long branches) ----
    labels, sizes, pc_of = resolve_sizes(label_index, expanded)

    # ---- Encode ----
    machine = []   # list of (pc, code, display_label)

    for i, (src, display, mnemonic, operands) in enumerate(expanded):
        base_pc = pc_of[i]
        try:
            if mnemonic not in OPCODE:
                raise ValueError(f"Unknown instruction '{mnemonic}'")

            op = OPCODE[mnemonic]

            # -------- R-type --------
            if mnemonic in ("add", "sub", "and", "or", "nor"):
                if len(operands) != 3:
                    raise ValueError(f"{mnemonic} expects 3 operands")
                rd, rs, rt = operands
                if rd not in REG or rs not in REG or rt not in REG:
                    raise ValueError(f"Bad register in: {display}")
                code = pack_R(op, REG[rs], REG[rt], REG[rd])
                machine.append((base_pc, code, display))

            # -------- I-type (imm) --------
            elif mnemonic in ("addi", "subi", "andi", "ori"):
                if len(operands) != 3:
                    raise ValueError(f"{mnemonic} expects 3 operands")
                rd, rs, imm = operands
                if rd not in REG or rs not in REG:
                    raise ValueError(f"Bad register in: {display}")
                imm_val = parse_imm(imm)
                imm4    = to_sint4(imm_val)
                code    = pack_I(op, REG[rs], REG[rd], imm4)
                machine.append((base_pc, code, display))

            # -------- Shift (S-type) --------
            elif mnemonic in ("sll", "srl"):
                if len(operands) != 3:
                    raise ValueError(f"{mnemonic} expects 3 operands")
                rd, rs, sh = operands
                if rd not in REG or rs not in REG:
                    raise ValueError(f"Bad register in: {display}")
                shv = parse_imm(sh)
                if not (0 <= shv <= 15):
                    raise ValueError(f"shamt out of range [0..15]: {shv}")
                code = pack_S(op, REG[rs], REG[rd], to_uint(shv, 4))
                machine.append((base_pc, code, display))

            # -------- Memory (I-type) --------
            elif mnemonic in ("lw", "sw"):
                if len(operands) != 2:
                    raise ValueError(f"{mnemonic} expects 2 operands")
                rt  = operands[0]
                mem = operands[1]
                if rt not in REG:
                    raise ValueError(f"Bad register '{rt}'")
                mm = MEM_RE.match(mem)
                if not mm:
                    raise ValueError(f"Bad memory operand '{mem}' (expected imm(base))")
                off  = parse_imm(mm.group(1))
                base = mm.group(2)
                if base not in REG:
                    raise ValueError(f"Bad base register '{base}'")
                imm4 = to_sint4(off)
                code = pack_I(op, REG[base], REG[rt], imm4)
                machine.append((base_pc, code, display))

            # -------- Branch (I-type PC-relative, with long-branch expansion) --------
            elif mnemonic in ("beq", "bneq"):
                if len(operands) != 3:
                    raise ValueError(f"{mnemonic} expects 3 operands")
                rs, rt, target = operands
                if rs not in REG or rt not in REG:
                    raise ValueError(f"Bad register in: {display}")

                # Resolve target PC
                if target in labels:
                    target_pc = labels[target]
                else:
                    raw_off = parse_imm(target)
                    # Treat as absolute PC for range check purposes
                    target_pc = base_pc + 1 + raw_off

                offset = target_pc - (base_pc + 1)

                if sizes[i] == 1:
                    # Short branch — fits in 4-bit signed offset
                    imm4 = to_sint4(offset)
                    code = pack_I(op, REG[rs], REG[rt], imm4)
                    machine.append((base_pc, code, display))
                else:
                    # Long branch — branch-over-jump pattern:
                    #   <inverted> rs, rt, +1   (offset=1 skips the jump)
                    #   j <target_pc>
                    inv_mnemonic = BRANCH_INVERT[mnemonic]
                    inv_op       = OPCODE[inv_mnemonic]
                    skip_imm4    = to_sint4(1)   # skip over the j instruction
                    branch_code  = pack_I(inv_op, REG[rs], REG[rt], skip_imm4)

                    if not (0 <= target_pc <= 255):
                        raise ValueError(
                            f"Long-branch jump target PC={target_pc} out of range [0..255]"
                        )
                    jump_code = pack_J(OPCODE["j"], to_uint(target_pc, 8))

                    machine.append((base_pc,     branch_code,
                                    f"[long-branch #{base_pc}: {inv_mnemonic} {rs},{rt},+1] {display}"))
                    machine.append((base_pc + 1, jump_code,
                                    f"[long-branch #{base_pc+1}: j {target_pc}] {display}"))

            # -------- Jump (J-type absolute) --------
            elif mnemonic == "j":
                if len(operands) != 1:
                    raise ValueError("j expects 1 operand")
                target = operands[0]
                if target in labels:
                    addr = labels[target]
                else:
                    addr = parse_imm(target)
                if not (0 <= addr <= 255):
                    raise ValueError(f"Jump target out of range [0..255]: {addr}")
                code = pack_J(op, to_uint(addr, 8))
                machine.append((base_pc, code, display))

            else:
                raise ValueError(f"Unhandled instruction: {mnemonic}")

        except ValueError as e:
            raise ValueError(f"PC={base_pc:03} ({display}): {e}") from None

    return machine


# ---------------------------
# 9) Logisim Evolution ROM image writer
# ---------------------------
def write_logisim_rom(machine, out_path: str, rom_depth: int = 256):
    """
    Write a Logisim Evolution 'v3.0 hex words addressed' ROM image.

    Format:
        v3.0 hex words addressed
        00: HHHH HHHH HHHH HHHH ...   (8 words per line, address on left)

    Unused slots are filled with 0000.
    """
    rom = [0x0000] * rom_depth
    for pc, code, _ in machine:
        if pc >= rom_depth:
            raise ValueError(f"PC {pc} exceeds ROM depth {rom_depth}")
        rom[pc] = code & 0xFFFF

    words_per_line = 8
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("v3.0 hex words addressed\n")
        for base in range(0, rom_depth, words_per_line):
            chunk     = rom[base:base + words_per_line]
            words_str = " ".join(f"{w:04x}" for w in chunk)
            f.write(f"{base:02x}: {words_str}\n")

    print(f"\n[ROM] Logisim Evolution image written -> {out_path}")
    print(f"      {len(machine)} instruction slot(s), ROM depth={rom_depth} words (16-bit each)")


# ---------------------------
# 10) CLI
# ---------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python asm4bit_mips.py input.asm [output.rom.txt]")
        sys.exit(1)
    path = sys.argv[1]

    if len(sys.argv) >= 3:
        rom_path = sys.argv[2]
    else:
        base     = path.rsplit(".", 1)[0] if "." in path else path
        rom_path = base + ".rom.txt"

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    machine = assemble(lines)

    print("PC  :  BINARY(16)           HEX   ; SOURCE / EXPANSION")
    print("-" * 72)
    for pc, code, display in machine:
        print(f"{pc:03}:  {bin16(code)}  {hex4(code)}  ; {display.rstrip()}")

    write_logisim_rom(machine, rom_path)

if __name__ == "__main__":
    main()