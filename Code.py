from typing import Optional


class Code:
    """
    Translates Hack assembly language mnemonics into binary codes.
    """

    dest_symbol_table = {
        None: 0,
        "M": 1,
        "D": 2,
        "DM": 3,
        "A": 4,
        "AM": 5,
        "AD": 6,
        "ADM": 7,
    }
    jmp_symbol_table = {
        None: 0,
        "JGT": 1,
        "JEQ": 2,
        "JGE": 3,
        "JLT": 4,
        "JNE": 5,
        "JLE": 6,
        "JMP": 7,
    }
    comp_symbol_table = {
        "0": 42,
        "1": 63,
        "-1": 58,
        "D": 12,
        "A": 48,
        "!D": 13,
        "!A": 49,
        "-D": 15,
        "-A": 51,
        "D+1": 31,
        "A+1": 55,
        "D-1": 14,
        "A-1": 50,
        "D+A": 2,
        "D-A": 19,
        "A-D": 7,
        "D&A": 0,
        "D|A": 21,
    }

    def dest(self, mnemonic: Optional[str]) -> str:
        bits = 3
        mnemonic = self._sort_string(mnemonic)
        return self._to_binary(Code.dest_symbol_table[mnemonic], bits=bits)

    def jump(self, mnemonic: str) -> str:
        bits = 3
        return self._to_binary(Code.jmp_symbol_table[mnemonic], bits=bits)

    def comp(self, mnemonic: str) -> str:
        a_bit, bits = "0", 6  # "a" bit is added separately
        if "M" in mnemonic:
            a_bit = "1"
            mnemonic = mnemonic.replace("M", "A")
        c_bits = self._to_binary(Code.comp_symbol_table[mnemonic], bits=bits)
        return a_bit + c_bits

    def a_instruction_binary(self, mnemonic: str | int) -> str:
        # A-instruction.
        bits = 15
        binary = self._to_binary(int(mnemonic), bits=bits)
        return "0" + binary

    def c_instruction_binary(self, comp: str, dest: str, jump: str) -> str:
        starting_bits = "111"
        return starting_bits + comp + dest + jump

    def _to_binary(self, integer: int, bits: int) -> str:
        return bin(integer).split("b")[1].zfill(bits)

    def _sort_string(self, string: Optional[str]) -> Optional[str]:
        if not string:
            return string
        else:
            lst = list(string)
            lst.sort()
            return "".join(lst)
