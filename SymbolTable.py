class SymbolTable:
    """
    Keeps a correspondence between symbolic labels like "(LOOP)" and numeric
    addresses (RAM and ROM).
    """

    # Predefined symbols.
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
        """
        Add the predefined key-value pairs into the symbol table.
        """
        self.symbol_table = {**self.symbol_table, **self.predefined}

    def add_entry(self, symbol: str, address: int) -> None:
        """
        Adds the pair (symbol, address) to the table.
        """
        self.symbol_table[symbol] = address

    def contains(self, symbol: str) -> bool:
        """
        Returns a bool denoting whether the symbol table contains the given symbol.
        """
        return symbol in self.symbol_table

    def get_address(self, symbol: str) -> int:
        """
        Returns the address associated with the symbol.
        """
        return self.symbol_table[symbol]
