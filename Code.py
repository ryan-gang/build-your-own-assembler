from typing import Optional, Any


class Code:
    """
    Translates Hack assembly language mnemonics into binary codes.
    """

    # DEST mnemonics and their binary mapping.
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
    # JUMP mnemonics and their binary mapping.
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
    # COMP mnemonics and their binary mapping.
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
        """
        Returns the binary code of the dest mnemonic.
        """
        pass

    def jump(self, mnemonic: Optional[str]) -> str:
        """
        Returns the binary code of the jump mnemonic.
        """
        pass

    def comp(self, mnemonic: str) -> str:
        """
        Returns the binary code of the comp mnemonic.
        """
        pass

    def a_instruction_binary(self, mnemonic: str | int) -> str:
        """
        Returns the binary code of the value mnemonic in an A-Instruction.
        """
        pass

    def c_instruction_binary(self, comp: str, dest: str, jump: str) -> str:
        """
        Returns the binary code of the full C-Instruction.
        """
        pass

    def _to_binary(self, integer: int, bits: int) -> str:
        """
        Helper method to convert ints into binary and pad with zero bits.
        """
        pass
