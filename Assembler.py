from io import TextIOWrapper
from Code import Code
from Parser import Parser
from SymbolTable import SymbolTable


class Assembler:
    def __init__(self, filepath: str) -> None:
        self.in_file_path = filepath

        self.p = Parser(filepath)
        self.p.__init_vars__()
        self.c = Code()
        self.st = SymbolTable()

        self.write_handle = self._init_writefile()

    def first_pass(self) -> None:
        while self.p.has_more_commands():
            self.p.advance()
            if self.p.command_type() == 2:  # L
                symbol = self.p.symbol()
                c_line = self.p.index - self.p.l_ins_count
                self.st.add_entry(symbol, c_line)
                self.p.l_ins_count += 1

        self.p.__init_vars__()  # Reset variables for 2nd pass.

    def second_pass(self) -> None:
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

    def get_address(self, symbol: str) -> int | str:
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
        self.first_pass()
        self.second_pass()

    def _init_writefile(self) -> TextIOWrapper:
        parts = self.in_file_path.split(".")
        parts[-1] = "hack"
        out_file_path = "".join(parts)
        fhand = open(out_file_path, "w")
        return fhand
