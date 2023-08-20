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

    def dest(self, mnemonic: Optional[str]) -> str:
        mnemonic = self._sort_string(mnemonic)
        return self._to_binary(Code.dest_symbol_table[mnemonic])

    def jump(self, mnemonic: Optional[str]) -> str:
        return self._to_binary(Code.jmp_symbol_table[mnemonic])

    def _to_binary(self, integer: int) -> str:
        return bin(integer).split("b")[1]

    def _sort_string(self, string: Optional[str]) -> Optional[str]:
        if not string:
            return string
        else:
            l = list(string)
            l.sort()
            return "".join(l)
