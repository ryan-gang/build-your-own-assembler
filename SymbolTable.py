from typing import Optional


class SymbolTable:
    """
    Keeps a correspondence between symbolic labels like "(LOOP)" and numeric
    addresses (RAM and ROM).
    """

    predefined = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        "SCREEN": 16384,
        "KBD": 24576,
    }

    def __init__(self) -> None:
        """
        Initializes a new empty symbol table, and adds predefined values.
        """
        self.symbol_table: dict[str, int] = {}
        self._add_predefined_values()

    def _add_predefined_values(self) -> None:
        self.symbol_table = {**self.symbol_table, **self.predefined}

    def add_entry(self, symbol: Optional[str], address: int) -> None:
        """
        Adds the pair (symbol, address) to the table.
        """
        symbol = self._validate_value(symbol)
        self.symbol_table[symbol] = address

    def contains(self, symbol: Optional[str]) -> bool:
        """
        Returns a bool denoting whether the symbol table contain the given symbol.
        """
        symbol = self._validate_value(symbol)
        return symbol in self.symbol_table

    def get_address(self, symbol: Optional[str]) -> int:
        """
        Returns the address associated with the symbol.
        """
        symbol = self._validate_value(symbol)
        return self.symbol_table[symbol]

    def _validate_value(self, value: Optional[str]) -> str:
        # This shouldn't happen.
        if not value:
            raise Exception(f"Unidentified symbol : {value}")
        else:
            return value
