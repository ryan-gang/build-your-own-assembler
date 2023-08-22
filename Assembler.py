import sys
from io import TextIOWrapper

from Code import Code
from Parser import Parser
from SymbolTable import SymbolTable


class Assembler:
    def __init__(self, filepath: str) -> None:
        """
        Initialize the assembler, add read-handle and write-handle for output .hack file.
        """
        self.in_file_path = filepath

        self.p = Parser(filepath)
        self.p.__init_vars__()
        self.c = Code()
        self.st = SymbolTable()

        self.write_handle = self._init_writefile()

    def first_pass(self) -> None:
        """
        Go through the entire assembly program, line by line, and build the
        symbol table without generating any code.
        Pseudo-commands like (LOOP) can appear later in the code, but used anywhere.
        So, we need to add all these symbols into our symbol table before code gen.
        """
        while self.p.has_more_commands():
            self.p.advance()
            if self.p.command_type() == 2:  # L
                symbol = self.p.symbol()
                c_line = self.p.index - self.p.l_ins_count
                self.st.add_entry(symbol, c_line)
                self.p.l_ins_count += 1

        self.p.__init_vars__()  # Reset variables for 2nd pass.

    def second_pass(self) -> None:
        """
        Now go again through the entire program, and parse each line.
        Convert the result to binary, and add as individual lines in the
        output file.
        """
        while self.p.has_more_commands():
            self.p.advance()
            c_type = self.p.command_type()
            if c_type == 0:  # A
                symbol = self.p.symbol()
                address = self.get_address(symbol)
                ins = self.c.a_instruction_binary(address)
            elif c_type == 1:  # C
                ins = self.c.c_instruction_binary(
                    self.c.comp(self.p.comp()),
                    self.c.dest(self.p.dest()),
                    self.c.jump(self.p.jump()),
                )
            else:  # L
                continue
            self.write(self.write_handle, ins)
        self.write_handle.close()

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
        if self.p.a_command_type() == 1:  # Constant
            return symbol
        else:
            if self.st.contains(symbol):
                return self.st.get_address(symbol)
            else:
                self.st.add_entry(symbol, self.p.mem_loc)
                self.p.mem_loc += 1
                return self.p.mem_loc - 1

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
        parts = self.in_file_path.split(".")
        parts[-1] = "hack"
        out_file_path = ".".join(parts)
        fhand = open(out_file_path, "w")
        return fhand

    def write(self, fhand: TextIOWrapper, line: str) -> None:
        """
        Write a single line to the provided file handle.
        """
        fhand.write(line)
        fhand.write("\n")


if __name__ == "__main__":
    # Run this script as: python program.asm
    # Generates a binary file program.hack which can be directly run on the given hardware.
    filepath = sys.argv[1]
    asm = Assembler(filepath)
    asm.assemble()
