import re

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"<{self.type}, {self.value}>"


KEYWORDS = {
    "int", "float", "double", "char", "if", "else",
    "while", "for", "return", "void", "break", "continue"
}


TOKEN_SPEC = [
    ("COMMENT",            r"//.*|/\*[\s\S]*?\*/"),
    ("KEYWORD",            r"\b(?:int|float|double|char|if|else|while|for|return|void|break|continue)\b"),
    ("IDENTIFIER",         r"[A-Za-z_]\w*"),
    ("NUMERIC_CONSTANT",   r"\b\d+(\.\d+)?\b"),
    ("CHARACTER_CONSTANT", r"'.'"),
    ("OPERATOR",           r"==|!=|<=|>=|[-+*/=<>]"),
    ("SPECIAL_CHARACTER",  r"[{}()[\];,]"),
    ("WHITE_SPACE",        r"[ \t]+"),
    ("NEWLINE",            r"\n"),
    ("MISMATCH",           r"."),
]

token_pattern = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)



class Scanner:
    def __init__(self, code):
        self.code = code

    def scan(self):
        tokens = []
        line_num = 1
        line_start = 0

        for match in re.finditer(token_pattern, self.code):
            Type = match.lastgroup
            value = match.group()
            column = match.start() - line_start + 1

            if Type == "NEWLINE":
                tokens.append(Token("NEWLINE", "\\n", line_num, column))
                line_num += 1
                line_start = match.end()
            elif Type == "WHITE_SPACE":
                continue
            elif Type == "COMMENT":
                tokens.append(Token("COMMENT", value.strip(), line_num, column))
            elif Type == "MISMATCH":
                continue
            else:
                tokens.append(Token(Type, value, line_num, column))

        return tokens



def main():
    print("C Scanner \n")
    print("Enter your C code \n")

    lines = []
    while True:
      line = input()
      if line.strip() == "":  
        break
      lines.append(line)


    code = "\n".join(lines)
    scanner = Scanner(code)
    tokens = scanner.scan()

    print("\nTokens Found:\n")
    for token in tokens:
        print(f"<{token.type.replace('_', ' ')}, {token.value}>")


if __name__ == "__main__":
    main()
