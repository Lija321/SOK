from enum import Enum, auto
from typing import Dict, Callable, Any
import shlex

class Command(Enum):
    EDIT_EDGE = auto()
    CLEAR_GRAPH = auto()
    EDIT_NODE = auto()
    SELECT_VISUALIZER = auto()
    FILTER_GRAPH = auto()
    SEARCH_GRAPH = auto()
    REMOVE_FILTER = auto()
    CLEAR_SEARCH = auto()
    CREATE_NODE = auto()
    CREATE_EDGE = auto()
    DELETE_EDGE = auto()
    DELETE_NODE = auto()
    SELECT_WORKSPACE = auto()
    CREATE_WORKSPACE = auto()

class CommandProcessor:
    def __init__(self):
        """initializing list of commands"""
        self.commands: Dict[Command, Callable[..., Any]] = {}

    def register(self, command: Command, func: Callable[..., Any]):
        """This functions serves as to register/bind Command enum literal to actual given function
        so the job of calling and function is to give and ENUM literal and arguments"""
        self.commands[command] = func

    def execute(self, command: Command, **kwargs) -> Any:
        """Execute a command by enum value with given params.
        Params are undefined, so passing the args of different commands can be generic
        where calling the command would be self.app.command_processor.execute(COMMAND_NAME,arg1 = some_arg,arg2=....)"""
        if command not in self.commands:
            raise ValueError(f"Unknown command: {command}")
        return self.commands[command](**kwargs)

    def parse_and_execute(self, command_str: str) -> Any:
        """
        Example commands
        "create node --id=1 --property Name=Alice --property Age=25"
        "create edge --origin=1 --target=2 --property type=knows"
        "delete edge --origin=1 --target=2"
        "edit edge --origin=1 --target=2 --property weight=5"
        """
        tokens = shlex.split(command_str)
        if not tokens:
            return "No command given."

        cmd = tokens[0].lower()
        entity = tokens[1].lower() if len(tokens) > 1 else None

        if cmd == "create":
            if entity == "node":
                kwargs = self._parse_properties(tokens[2:], edge_mode=False)
                return self.execute(Command.CREATE_NODE, **kwargs)
            elif entity == "edge":
                kwargs = self._parse_properties(tokens[2:], edge_mode=True)
                return self.execute(Command.CREATE_EDGE, **kwargs)

        elif cmd == "delete":
            if entity == "node":
                kwargs = self._parse_properties(tokens[2:], edge_mode=False)
                return self.execute(Command.DELETE_NODE, **kwargs)
            elif entity == "edge":
                kwargs = self._parse_properties(tokens[2:], edge_mode=True)
                return self.execute(Command.DELETE_EDGE, **kwargs)

        elif cmd == "edit":
            if entity == "node":
                kwargs = self._parse_properties(tokens[2:], edge_mode=False)
                return self.execute(Command.EDIT_NODE, **kwargs)
            elif entity == "edge":
                kwargs = self._parse_properties(tokens[2:], edge_mode=True)
                return self.execute(Command.EDIT_EDGE, **kwargs)

        elif cmd == "filter":
            filter_str = " ".join(tokens[1:])
            return self.execute(Command.FILTER_GRAPH, filter_expr=filter_str)

        elif cmd == "search":
            search_str = " ".join(tokens[1:])
            return self.execute(Command.SEARCH_GRAPH, search_expr=search_str)

        elif cmd == "clear":
            return self.execute(Command.CLEAR_GRAPH)

        else:
            return f"Unknown command: {command_str}"

    def _parse_value(self, val: str):
        """Convert string to int, float, or bool if possible; fallback to string."""
        if val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
            return int(val)
        elif '.' in val:
            try:
                return float(val)
            except ValueError:
                return val
        elif val.lower() in ['true', 'false']:
            return val.lower() == 'true'
        return val

    def _parse_properties(self, tokens, edge_mode=False):
        """
        Parse CLI tokens into kwargs for node or edge creation/edit.
        If edge_mode=True, --origin and --target go in kwargs separately.
        """
        kwargs = {}
        props = {}
        i = 0

        while i < len(tokens):
            token = tokens[i]

            if token.startswith("--id="):
                kwargs["id"] = self._parse_value(token.split("=", 1)[1])
            elif token.startswith("--origin="):
                val = self._parse_value(token.split("=", 1)[1])
                if edge_mode:
                    kwargs["origin_id"] = val
                else:
                    props["origin"] = val
            elif token.startswith("--target="):
                val = self._parse_value(token.split("=", 1)[1])
                if edge_mode:
                    kwargs["target_id"] = val
                else:
                    props["target"] = val
            elif token.startswith("--property"):
                if i + 1 < len(tokens):
                    key_val = tokens[i + 1]
                    if "=" in key_val:
                        key, val = key_val.split("=", 1)
                        props[key] = self._parse_value(val)
                        i += 1
            i += 1

        if props:
            kwargs["properties"] = props
        return kwargs