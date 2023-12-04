from typing import Any, Dict, List, Self
from dataclasses import asdict
from json import dumps

def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

class Argument:
    text: str
    requieried: bool
    
    def __init__(self, text: str = None, requieried: bool = True) -> None:
        self.text = text
        self.requieried = requieried
    
    def __str__(self) -> str:
        if self.text:
            o_br, c_br = ('<', '>') if self.requieried else ('[', ']')
            return o_br + '\xa0' + self.text.replace(' ', '\xa0') + '\xa0' + c_br
        return ''

class Command:
    commands: List[str]
    args: List[Argument]
    description: str

    def __init__(self, commands: list|str, args: list, description: str) -> None:
        self.commands = commands if type(commands) == list else [commands]
        self.args = args
        self.description = description
    

    def as_dict(self) -> dict:
        return asdict(self)

    def __str__(self) -> str:
        return dumps(self.as_dict(), indent=4)

class Feature:
    description: str
    
    def __init__(self, description) -> None:
        self.description = description
    
    def as_dict(self) -> dict:
        return asdict(self)

    def __str__(self) -> str:
        return dumps(self.as_dict(), indent=4)

class Module:
    commands: List[Command]
    features: List[Feature]
    name: str
    description: str
    author: str
    version: Any

    def __init__(
        self: Self,
        name: str,
        *,
        description: str|None = '',
        author: str|None = '',
        version: Any|None = None,
        commands: List[Command] = None,
        features: List[Feature] = None
    ) -> None:
        self.commands = commands if commands else []
        self.features = features if features else []
        self.name = name
        self.description = description
        self.author = author
        self.version = version

    def add_command(self: Self, command: Command, /):
        self.commands.append(command)
        return self
    
    def get_commands_count(self) -> int:
        return len(self.commands)

    def get_commands(self) -> List[Command]:
        return self.commands
    

    def add_feature(self: Self, feature: Feature, /):
        self.features.append(feature)
        return self
    
    def get_features_count(self) -> int:
        return len(self.features)

    def get_features(self) -> List[Feature]:
        return self.features
    

    def as_dict(self) -> dict:
        return asdict(self)

    def __str__(self) -> str:
        return dumps(self.as_dict(), indent=4)

@singleton
class HelpList:
    modules: Dict[str, Module]

    def __init__(self) -> None:
        self.modules = {}
    
    def add_module(self, module: Module, /) -> Self:
        self.modules[module.name] = module
        return self
    
    def get_module(self, name: str, default: Any = None, lower=False) -> Module:
        if not lower:
            return self.modules.get(name, default)
        else:
            return dict(zip(
                map(lambda k: k.lower(), self.modules.keys()),
                self.modules.values()
            )).get(name, default)

    def get_modules_count(self) -> int:
        return len(self.modules)
    
    def get_modules_names(self) -> List[str]:
        return self.modules.keys()
    
    def get_modules(self) -> List[Module]:
        return self.modules.values()
    
    def as_dict(self) -> dict:
        return asdict(self)

    def __str__(self) -> str:
        return dumps(self.as_dict(), indent=4)


