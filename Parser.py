import re
from typing import Any, Optional


class Parser:
    """
    Encapsulates access to the input code. Reads an assembly language command,
    parses it, and provides convenient access to the command's components
    (fields and symbols). In addition, removes all whitespaces and comments.
    """

    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2

    # Regex strings
    # A-Instruction
    # @ + a_start + a_symbol | a_constant
    # @ + a_start + a_constant -> Type 1
    # @ + a_start + a_symbol -> Type 2
    a_ins_cons = r"\d+(\.\d+)?"
    a_ins_sym = r"[0-9A-Za-z_.$:]+"
    a_ins_start = r"^@"
    a_ins_t1 = re.compile(a_ins_start + a_ins_cons)  # A-Instruction type 1
    a_ins_t2 = re.compile(a_ins_start + a_ins_sym)  # A-Instruction type 2

    # C-Instruction
    # c_ins_tok0 + = + c_ins_tok1 + c_ins_op + c_ins_tok2 + ; + c_ins_jmp
    c_ins_tok0 = r"[ADM10]{0,3}"
    c_ins_tok1 = r"[ADM10]{0,1}"
    c_ins_op = r"[-+!|&]{0,1}"
    c_ins_tok2 = r"[ADM10]{1}"
    c_ins_jmp = r"(JGT|JEQ|JGE|JLT|JNE|JLE|JMP)"
    # dest=comp
    c_ins_dest_comp = re.compile(c_ins_tok0 + "=" + c_ins_tok1 + c_ins_op + c_ins_tok2)
    # comp
    c_ins_comp = re.compile(c_ins_tok1 + c_ins_op + c_ins_tok2)
    # comp;jump
    c_ins_comp_jump = re.compile(c_ins_tok1 + c_ins_op + c_ins_tok2 + ";" + c_ins_jmp)

    # L-Instruction
    l_ins = re.compile(r"\(" + a_ins_sym + r"\)")

    # Misc
    empty_line = r"^[\s]+?$"
    comment = r"\/\/.*$"
    white_spaces = r"[\s]+"

    def __init__(self, filepath: str) -> None:
        """
        Opens the input file/stream, reads in the contents, removes all
        whitespaces and comments.
        """
        self.parsed: list[str] = []
        with open(filepath, "r") as f:
            data = f.read()
        self.instructions = data.split("\n")

        for ins in self.instructions:
            ins_wo_comments = re.sub(pattern=self.comment, repl="", string=ins)
            ins_stripped = re.sub(pattern=self.white_spaces, repl="", string=ins_wo_comments)
            if instruction := ins_stripped.strip():
                self.parsed.append(instruction)

    def __init_vars__(self) -> None:
        """
        Instantiate class variables, and provide a handy to reset them.
        """
        self.index = -1
        self.current_command = ""
        self.l_ins_count: int = 0  # Count of L-instructions.
        # Required for skipping them while getting line number of goto instruction.
        self.mem_loc = 16  # User variables mapping to memory location.

    def has_more_commands(self) -> bool:
        """
        Returns a boolean, denoting if there are more commands in the parsed input.
        """
        return self.index < len(self.parsed) - 1

    def advance(self) -> None:
        """
        Reads the next command, updating current_command and the command index.
        """
        self.index += 1
        self.current_command = self.parsed[self.index]

    def command_type(self) -> Any:
        """
        Returns the type of the current command: A_COMMAND (0), C_COMMAND (1), L_COMMAND (2).
        """
        command = self.current_command
        if self._is_a_command(command):
            return Parser.A_COMMAND
        elif self._is_c_command(command):
            return Parser.C_COMMAND
        elif self._is_l_command(command):
            return Parser.L_COMMAND

    def a_command_type(self) -> int:
        """
        Returns the type of the current A-instruction value, symbol or decimal.
        1 : @constant
        2 : @symbol
        """
        command = self.current_command
        if self._is_match(self.a_ins_t1, command):
            return 1
        elif self._is_match(self.a_ins_t2, command):
            return 2
        else:
            return 0

    def symbol(self) -> str:
        """
        Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx).
        """
        command = self.current_command
        a_l_ins_symbol = re.compile(self.a_ins_sym)
        res = self._match_result(a_l_ins_symbol, command)
        return self._validate_value(res)

    def dest(self) -> Optional[str]:
        """
        Returns the dest mnemonic in the current C-command.
        """
        command = self.current_command
        destination = re.compile(self.c_ins_tok0)
        # dest=comp
        if self._is_match(self.c_ins_dest_comp, command):
            return self._match_result(destination, command.split("=")[0])

    def comp(self) -> str:
        """
        Returns the comp mnemonic in the current C-command.
        """
        command = self.current_command
        # dest=comp
        if self._is_match(self.c_ins_dest_comp, command):
            res = self._match_result(self.c_ins_comp, command.split("=")[1])
        # comp
        elif self._is_match(self.c_ins_comp, command):
            res = self._match_result(self.c_ins_comp, command)
        # comp;jump
        # elif self._is_match(self.c_ins_comp_jump, command):
        else:
            res = self._match_result(self.c_ins_comp, command)
        return self._validate_value(res)

    def jump(self) -> Optional[str]:
        """
        Returns the jump mnemonic in the current C-command.
        """
        command = self.current_command
        c_jump = re.compile(self.c_ins_jmp)
        # comp;jump
        return self._match_result(c_jump, command)

    def _is_a_command(self, command: str) -> bool:
        """
        Return a bool denoting if command is an A command.
        """
        return self._is_match(self.a_ins_t1, command) or self._is_match(self.a_ins_t2, command)

    def _is_c_command(self, command: str) -> bool:
        """
        Return a bool denoting if command is a C command.
        """
        return (self._is_match(self.c_ins_comp, command) or self._is_match(self.c_ins_comp_jump,
                                                                           command) or self._is_match(
            self.c_ins_dest_comp, command))

    def _is_l_command(self, command: str) -> bool:
        """
        Return a bool denoting if command is an L-command.
        """
        return self._is_match(self.l_ins, command)

    def _is_match(self, pattern: re.Pattern[str], string: str) -> bool:
        """
        Returns if a match is found for `pattern` in `string`.
        """
        return re.fullmatch(pattern, string) is not None

    def _match_result(self, pattern: re.Pattern[str], string: str) -> Optional[str]:
        """
        Return match results found for `pattern` in `string`.
        Returns None if no match found.
        """
        matched = re.search(pattern, string)
        if matched is not None:
            return matched.group()

    def _validate_value(self, value: Optional[Any]) -> Any:
        """
        Validate the output of parsing isn't None.
        """
        if not value:
            raise Exception(f"Unidentified symbol : {value}")
        else:
            return value
