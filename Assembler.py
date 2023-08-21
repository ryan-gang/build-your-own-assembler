from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable


class Assembler:
    def __init__(self, filepath: str) -> None:
        self.p = Parser(filepath)
        self.p.__init_vars__()
        self.c = Code()
        self.st = SymbolTable()

    def first_pass(self, p: Parser, st: SymbolTable) -> None:
        while p.has_more_commands():
            p.advance()
            if p.command_type() == 2:  # L
                symbol = p.symbol()
                c_line = p.index - p.l_ins
                st.add_entry(symbol, c_line)
                p.l_ins += 1

        p.__init_vars__()  # Reset variables for 2nd pass.

    def second_pass(self, p: Parser, st: SymbolTable, c: Code) -> None:
        while p.has_more_commands():
            p.advance()
            c_type = p.command_type()
            if c_type == 0:  # A
                symbol = p.symbol()
                if p.a_command_type() == 1:  # Constant
                    ins = c.value(symbol)
                else:
                    if st.contains(symbol):
                        val = st.get_address(symbol)
                        ins = c.value(val)
                    else:
                        st.add_entry(symbol, p.mem_loc)
                        ins = c.value(p.mem_loc)
                        p.mem_loc += 1
            elif c_type == 1:  # C
                ins = c.c_instruction_binary(c.comp(p.comp()), c.dest(p.dest()), c.jump(p.jump()))
            else:  # L
                continue
            print(ins)
