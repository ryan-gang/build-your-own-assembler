import re
from typing import Any, Optional


class Parser:
    """
    Encapsulates access to the input code. Reads an assembly language command,
    parses it, and provides convenient access to the command's components
    (fields and symbols). In addition, removes all white space and comments.
    """

    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2

    def __init__(self, filepath: str) -> None:
        """
        Opens the input file/stream, reads in the contents, removes all
        whitespaces and comments.
        """
        self.index = -1
        self.empty_line = r"^[\s]+?$"
        self.comment = r"\/\/.*$"
        self.white_space = r"[\s]+"

        self.parsed: list[str] = []
        self.current_command = ""

        with open(filepath, "r") as f:
            data = f.read()

        self.instructions = data.split("\n")

        for line in self.instructions:
            line_wo_comments = re.sub(pattern=self.comment, repl="", string=line)
            stripped_line = re.sub(pattern=self.white_space, repl="", string=line_wo_comments)
            if instruction := stripped_line.strip():
                self.parsed.append(instruction)

    def hasMoreCommands(self) -> bool:
        """
        Returns a boolean, denoting if there more commands in the parsed input.
        """
        return self.index < len(self.parsed) - 1

    def advance(self) -> None:
        """
        Reads the next command, updating current_command and the command index.
        """
        self.index += 1
        self.current_command = self.parsed[self.index]

    def commandType(self) -> Any:
        command = self.current_command
        if self._is_a_command(command):
            return Parser.A_COMMAND
        elif self._is_c_command(command):
            return Parser.C_COMMAND
        elif self._is_l_command(command):
            return Parser.L_COMMAND

    def symbol(self) -> Optional[str]:
        command = self.current_command

        symbol = r"[0-9A-Za-z_.$:]+"
        al_symbol = re.compile(symbol)

        return self._match_result(al_symbol, command)

    def dest(self) -> Optional[str]:
        command = self.current_command

        token1 = r"[ADM10]{0,1}"
        operation = r"[-+!|&]{0,1}"
        token2 = r"[ADM10]"
        destination = re.compile(token1)

        # dest=comp
        c_dest_comp = re.compile(token1 + "=" + token1 + operation + token2)
        if self._is_match(c_dest_comp, command):
            return self._match_result(destination, command.split("=")[0])

    def comp(self) -> Optional[str]:
        command = self.current_command

        token1 = r"[ADM10]{0,1}"
        operation = r"[-+!|&]{0,1}"
        token2 = r"[ADM10]"
        jump = r"(JGT|JEQ|JGE|JLT|JNE|JLE|JMP)"
        computation = re.compile(token1 + operation + token2)

        # dest=comp
        c_dest_comp = re.compile(token1 + "=" + token1 + operation + token2)
        if self._is_match(c_dest_comp, command):
            return self._match_result(computation, command.split("=")[1])

        # comp
        c_comp = re.compile(token1 + operation + token2)
        if self._is_match(c_comp, command):
            return self._match_result(computation, command)

        # comp;jump
        c_comp_jump = re.compile(token1 + operation + token2 + ";" + jump)
        if self._is_match(c_comp_jump, command):
            return self._match_result(computation, command)

    def _is_a_command(self, command: str) -> bool:
        a_constant = r"\d+(\.\d+)?"
        a_symbol = r"[0-9A-Za-z_.$:]+"
        a_start = r"^@"

        a_inst_1 = re.compile(a_start + a_constant)
        a_inst_2 = re.compile(a_start + a_symbol)

        return self._is_match(a_inst_1, command) or self._is_match(a_inst_2, command)

    def _is_c_command(self, command: str) -> bool:
        token1 = r"[ADM10]{0,1}"
        operation = r"[-+!|&]{0,1}"
        token2 = r"[ADM10]"
        jump = r"(JGT|JEQ|JGE|JLT|JNE|JLE|JMP)"

        # dest=comp
        c_dest_comp = re.compile(token1 + "=" + token1 + operation + token2)
        # comp
        c_comp = re.compile(token1 + operation + token2)
        # comp;jump
        c_comp_jump = re.compile(token1 + operation + token2 + ";" + jump)
        return (
            self._is_match(c_comp, command)
            or self._is_match(c_comp_jump, command)
            or self._is_match(c_dest_comp, command)
        )

    def _is_l_command(self, command: str) -> bool:
        a_symbol = r"[0-9A-Za-z_.$:]+"

        l_inst = re.compile(r"\(" + a_symbol + r"\)")

        return self._is_match(l_inst, command)

    def _is_match(self, pattern: re.Pattern[str], string: str) -> bool:
        return re.fullmatch(pattern, string) is not None

    def _match_result(self, pattern: re.Pattern[str], string: str) -> Optional[str]:
        matched = re.search(pattern, string)
        if matched is not None:
            return matched.group()
