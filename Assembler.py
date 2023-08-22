import sys
from io import TextIOWrapper


class Assembler:
    def __init__(self, filepath: str) -> None:
        """
        Initialize the assembler, add read-handle and write-handle for output .hack file.
        """
        pass

    def first_pass(self) -> None:
        """
        Go through the entire assembly program, line by line, and build the
        symbol table without generating any code.
        Pseudo-commands like (LOOP) can appear later in the code, but used anywhere.
        So, we need to add all these symbols into our symbol table before code gen.
        """
        pass

    def second_pass(self) -> None:
        """
        Now go again through the entire program, and parse each line.
        Convert the result to binary, and add as individual lines in the
        output file.
        """
        pass

    def get_address(self, symbol: str) -> int | str:
        """
        Encapsulate all A-Instructions, given the instruction @Xxx where Xxx is
        a symbol and not a number, look up Xxx in the symbol table. If the
        symbol is found in the table, replace it with its numeric meaning and
        complete the command's translation. If the symbol isn't found in the
        table, then it must represent a new variable. To handle it, add the pair
        (Xxx, n) to the symbol table, where n is the next available RAM address,
        and complete the command's translation. The allocated RAM addresses are
        consecutive numbers, starting at address 16.
        """
        pass

    def assemble(self):
        """
        Run the assembler.
        """
        self.first_pass()
        self.second_pass()

    def _init_writefile(self) -> TextIOWrapper:
        """
        Initialize the output file, and return a file handle for writing to it.
        """
        pass


if __name__ == "__main__":
    # Run this script as: python program.asm
    # Generates a binary file program.hack which can be directly run on the given hardware.
    filepath = sys.argv[1]
    asm = Assembler(filepath)
    asm.assemble()
