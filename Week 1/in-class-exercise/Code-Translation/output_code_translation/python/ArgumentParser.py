from typing import Tuple, Set, Dict, Callable


class ArgumentParser:
    def __init__(self):
        self.arguments: Dict[str, str] = {}
        self.required: Set[str] = set()
        self.types: Dict[str, str] = {}
        self.type_converters: Dict[str, Callable[[str], str]] = {}
        self.initialize_converters()

    def parse_arguments(self, command_string: str) -> Tuple[bool, Set[str]]:
        tokens = command_string.split()
        # discard the first token (command name)
        i = 1
        while i < len(tokens):
            word = tokens[i]
            if word.startswith("--"):
                key_value = word[2:]
                if "=" in key_value:
                    key, value = key_value.split("=", 1)
                else:
                    key, value = key_value, ""
                self.arguments[key] = self.convert_type(
                    key, value if value != "" else "1"
                )
                i += 1
            elif word.startswith("-"):
                key = word[1:]
                # look ahead to see if next token is a value
                if i + 1 < len(tokens) and not tokens[i + 1].startswith("-"):
                    value = tokens[i + 1]
                    self.arguments[key] = self.convert_type(key, value)
                    i += 2
                else:
                    self.arguments[key] = self.convert_type(key, "1")
                    i += 1
            else:
                i += 1

        missing_args = {req for req in self.required if req not in self.arguments}
        return (len(missing_args) == 0, missing_args)

    def get_argument(self, key: str) -> str:
        return self.arguments.get(key, "")

    def add_argument(self, arg: str, required: bool = False, type: str = "string"):
        if required:
            self.required.add(arg)
        self.types[arg] = type

    def convert_type(self, arg: str, value: str) -> str:
        if arg not in self.types:
            return value
        converter = self.type_converters.get(self.types[arg])
        if converter:
            return converter(value)
        return value

    def initialize_converters(self):
        self.type_converters["int"] = lambda value: (
            str(int(value)) if value.lstrip("-").isdigit() else value
        )
        self.type_converters["bool"] = lambda value: (
            "1" if value == "True" else ("0" if value == "False" else value)
        )
