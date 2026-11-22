
import re
import sys
from pathlib import Path


# ==========================================
# 1. PREDEFINED SYMBOL TABLE
# ==========================================

PREDEFINED_SYMBOLS = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}

for i in range(16):
    PREDEFINED_SYMBOLS[f"R{i}"] = i


# ==========================================
# 2. COMPUTATION TABLE
# ==========================================

COMP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",

    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}


# ==========================================
# 3. DESTINATION TABLE
# ==========================================

DEST = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}


# ==========================================
# 4. JUMP TABLE
# ==========================================

JUMP = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}


# ==========================================
# 5. SOURCE CODE CLEANING
# ==========================================

def clean_lines(source):

    instructions = []

    for line_number, line in enumerate(
        source.splitlines(), start=1
    ):

        line = line.split("//", 1)[0]
        line = "".join(line.split())

        if line:
            instructions.append((line_number, line))

    return instructions


# ==========================================
# 6. SYMBOL VALIDATION
# ==========================================

def valid_symbol(symbol):

    return re.fullmatch(
        r"[A-Za-z_.$:][A-Za-z0-9_.$:]*",
        symbol
    ) is not None


# ==========================================
# 7. FIRST PASS - LABEL RESOLUTION
# ==========================================

def first_pass(lines):

    symbols = PREDEFINED_SYMBOLS.copy()
    instructions = []

    rom_address = 0

    for line_number, line in lines:

        if line.startswith("(") or line.endswith(")"):

            if not (
                line.startswith("(")
                and line.endswith(")")
            ):
                raise ValueError(
                    f"Line {line_number}: Invalid label declaration"
                )

            label = line[1:-1]

            if not valid_symbol(label):
                raise ValueError(
                    f"Line {line_number}: Invalid label '{label}'"
                )

            if label in symbols:
                raise ValueError(
                    f"Line {line_number}: Duplicate or reserved "
                    f"symbol '{label}'"
                )

            symbols[label] = rom_address

        else:

            if rom_address >= 32768:
                raise ValueError(
                    f"Line {line_number}: ROM capacity exceeded"
                )

            instructions.append((line_number, line))
            rom_address += 1

    return symbols, instructions


# ==========================================
# 8. A-INSTRUCTION TRANSLATION
# ==========================================

def assemble_a_instruction(
    instruction,
    symbols,
    next_variable_address,
    line_number
):

    symbol = instruction[1:]

    if not symbol:
        raise ValueError(
            f"Line {line_number}: Missing A-instruction value"
        )

    if symbol.isdecimal():

        address = int(symbol)

    else:

        if not valid_symbol(symbol):
            raise ValueError(
                f"Line {line_number}: Invalid symbol '{symbol}'"
            )

        if symbol not in symbols:

            if next_variable_address > 16383:
                raise ValueError(
                    f"Line {line_number}: RAM variable space exhausted"
                )

            symbols[symbol] = next_variable_address
            address = next_variable_address

            next_variable_address += 1

        else:
            address = symbols[symbol]

    if not 0 <= address <= 32767:
        raise ValueError(
            f"Line {line_number}: Address must be between 0 and 32767"
        )

    return f"{address:016b}", next_variable_address


# ==========================================
# 9. C-INSTRUCTION TRANSLATION
# ==========================================

def assemble_c_instruction(instruction, line_number):

    if instruction.count("=") > 1:
        raise ValueError(
            f"Line {line_number}: Multiple '=' operators"
        )

    if instruction.count(";") > 1:
        raise ValueError(
            f"Line {line_number}: Multiple ';' operators"
        )

    if "=" in instruction:
        dest, remaining = instruction.split("=", 1)
    else:
        dest, remaining = "", instruction

    if ";" in remaining:
        comp, jump = remaining.split(";", 1)
    else:
        comp, jump = remaining, ""

    if dest not in DEST:
        raise ValueError(
            f"Line {line_number}: Invalid destination '{dest}'"
        )

    if comp not in COMP:
        raise ValueError(
            f"Line {line_number}: Invalid computation '{comp}'"
        )

    if jump not in JUMP:
        raise ValueError(
            f"Line {line_number}: Invalid jump '{jump}'"
        )

    return (
        "111"
        + COMP[comp]
        + DEST[dest]
        + JUMP[jump]
    )


# ==========================================
# 10. SECOND PASS - MACHINE CODE GENERATION
# ==========================================

def second_pass(symbols, instructions):

    machine_code = []
    next_variable_address = 16

    for line_number, instruction in instructions:

        if instruction.startswith("@"):

            binary, next_variable_address = (
                assemble_a_instruction(
                    instruction,
                    symbols,
                    next_variable_address,
                    line_number
                )
            )

        else:

            binary = assemble_c_instruction(
                instruction,
                line_number
            )

        machine_code.append(binary)

    return machine_code


# ==========================================
# 11. SYMBOL TABLE EXPORT
# ==========================================

def save_symbols(symbols, output_path):

    symbol_file = output_path.parent / "symbols.txt"

    with symbol_file.open("w", encoding="utf-8") as file:

        file.write("HACK ASSEMBLER SYMBOL TABLE\n")
        file.write("=" * 40 + "\n\n")

        file.write(
            f"{'SYMBOL':<20} {'ADDRESS':<10}\n"
        )

        file.write("-" * 40 + "\n")

        for symbol, address in sorted(
            symbols.items(),
            key=lambda item: (item[1], item[0])
        ):

            file.write(
                f"{symbol:<20} {address:<10}\n"
            )

    return symbol_file


# ==========================================
# 12. MAIN ASSEMBLER FUNCTION
# ==========================================

def assemble(input_path):

    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"File not found: {input_path}"
        )

    if input_path.suffix.lower() != ".asm":
        raise ValueError(
            "Input file must have .asm extension"
        )

    source = input_path.read_text(encoding="utf-8")

    lines = clean_lines(source)

    symbols, instructions = first_pass(lines)

    machine_code = second_pass(
        symbols,
        instructions
    )

    output_path = input_path.with_suffix(".hack")

    output_path.write_text(
        "\n".join(machine_code) + "\n",
        encoding="utf-8"
    )

    symbol_path = save_symbols(
        symbols,
        output_path
    )

    print("\n" + "=" * 45)
    print("       HACK ASSEMBLER - SUCCESS")
    print("=" * 45)

    print(f"Input file      : {input_path}")
    print(f"Machine code    : {output_path}")
    print(f"Symbol table    : {symbol_path}")
    print(f"Instructions    : {len(machine_code)}")
    print(f"Total symbols   : {len(symbols)}")

    print("=" * 45)


# ==========================================
# 13. COMMAND LINE INTERFACE
# ==========================================

if __name__ == "__main__":

    if len(sys.argv) != 2:

        print(
            "Usage: python assembler.py <filename.asm>"
        )

        sys.exit(1)

    try:

        assemble(sys.argv[1])

    except (ValueError, OSError) as error:

        print(f"\nASSEMBLER ERROR: {error}")
        sys.exit(1)
