class SymbolTable:
    """
    Keeps a correspondence between symbolic labels like "(LOOP)" and numeric
    addresses (RAM and ROM).
    """

    def __init__(self) -> None:
        """
        Initializes a new empty symbol table, and adds predefined values.
        """
        pass

    def add_entry(self, symbol: str, address: int) -> None:
        """
        Adds the pair (symbol, address) to the table.
        """
        pass

    def contains(self, symbol: str) -> bool:
        """
        Returns a bool denoting whether the symbol table contain the given symbol.
        """
        pass

    def get_address(self, symbol: str) -> int:
        """
        Returns the address associated with the symbol.
        """
        pass
