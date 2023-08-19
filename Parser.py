import re


class Parser:
    """
    Encapsulates access to the input code. Reads an assembly language command,
    parses it, and provides convenient access to the command's components
    (fields and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, filepath: str) -> None:
        """
        Opens the input file/stream, reads in the contents, removes all
        whitespaces and comments.
        """
        self.index = 0
        self.empty_line = r"^[\s]+?$"
        self.comment = r"\/\/.*$"
        self.white_space = r"[\s]+"

        self.parsed: list[str] = []

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
        pass

    def commandType(self) -> None:
        pass

    def symbol(self) -> None:
        pass

    def dest(self) -> None:
        pass

    def comp(self) -> None:
        pass

    def jump(self) -> None:
        pass
