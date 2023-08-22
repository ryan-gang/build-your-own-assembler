import re
from typing import Any, Optional


class Parser:
    """
    Encapsulates access to the input code. Reads an assembly language command,
    parses it, and provides convenient access to the command's components
    (fields and symbols). In addition, removes all whitespaces and comments.
    """

    def __init__(self, filepath: str) -> None:
        """
        Opens the input file/stream, reads in the contents, removes all
        whitespaces and comments.
        """
        pass

    def __init_vars__(self) -> None:
        """
        Instantiate class variables, and provide a handy to reset them.
        """
        pass

    def has_more_commands(self) -> bool:
        """
        Returns a boolean, denoting if there are more commands in the parsed input.
        """
        pass

    def advance(self) -> None:
        """
        Reads the next command, updating current_command and the command index.
        """
        pass

    def command_type(self) -> Any:
        """
        Returns the type of the current command: A_COMMAND (0), C_COMMAND (1), L_COMMAND (2).
        """
        pass

    def a_command_type(self) -> int:
        """
        Returns the type of the current A-instruction value, symbol or decimal.
        1 : @constant
        2 : @symbol
        """
        pass

    def symbol(self) -> str:
        """
        Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx).
        """
        pass

    def dest(self) -> Optional[str]:
        """
        Returns the dest mnemonic in the current C-command.
        """
        pass

    def comp(self) -> str:
        """
        Returns the comp mnemonic in the current C-command.
        """
        pass

    def jump(self) -> Optional[str]:
        """
        Returns the jump mnemonic in the current C-command.
        """
        pass

    def _is_a_command(self, command: str) -> bool:
        """
        Return a bool denoting if command is an A command.
        """
        pass

    def _is_c_command(self, command: str) -> bool:
        """
        Return a bool denoting if command is a C command.
        """
        pass

    def _is_l_command(self, command: str) -> bool:
        """
        Return a bool denoting if command is an L-command.
        """
        pass

    def _is_match(self, pattern: re.Pattern[str], string: str) -> bool:
        """
        Returns if a match is found for `pattern` in `string`.
        """
        pass

    def _match_result(self, pattern: re.Pattern[str], string: str) -> Optional[str]:
        """
        Return match results found for `pattern` in `string`.
        Returns None if no match found.
        """
        pass
