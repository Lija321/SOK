from enum import Enum, auto
from typing import Dict, Callable, Any

class Command(Enum):
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
        Params are undefined so passing the args of different commands can be generic
        where calling the command would be self.app.command_processor.execute(COMMAND_NAME,arg1 = some_arg,arg2=....)"""
        if command not in self.commands:
            raise ValueError(f"Unknown command: {command}")
        return self.commands[command](**kwargs)
