from types import NoneType
from typing import Any, List, Self
from .html_tags import code as html_code, b

def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

class Module:
    name: str
    author: str|Any|None
    version: str|Any|None
    description: str|Any|None
    commands: List[dict]

    def __init__(self, name, *, author=None, version=None, description=None) -> None:
        self.name = name
        self.author = author
        self.version = version
        self.description = description
        self.commands: List[dict] = []
        
    
    def add_command(self, command_names: list|str, command_description: str, command_args: list|None = None) -> Self:
        self.commands.append(
            dict(
            commands=(command_names if type(command_names) in (list, set, tuple) else [command_names]),
            description=command_description,
            args=([] if command_args == None else command_args)
        ))
        return self
    
    

    def as_dict(self) -> dict:
        return dict(
            name=self.name,
            author=self.author,
            version=self.version,
            description=self.description,
            commands=self.commands
        )

    def load(dict_module: dict) -> Self:
        print(dict_module)
        m = Module(
            name = dict_module['name'],
            author = dict_module['author'],
            version = dict_module['version'],
            description = dict_module['description']
        )
        for command in dict_module['commands']:
            m.add_command(
                command['commands'],
                command['description'],
                command['args'],
            )
        return m
        

hl = {
    'module': {
        'name': str,
        'description': str,
        'author': str,
        'commands': [
            {
                'commands': ['t', 'test'],
                'args': [],
                'description': 'test'
            }
        ]
    }
}

@singleton
class HelpList:
    def __init__(self) -> None:
        self.help_list: dict[str, dict[str,List[dict]]] = {}
    
    def get(self, module: str, default=NoneType) -> dict|None:
        default = [] if default == NoneType else default
        return Module.load(self.help_list.get(module, default))
    
    def add_module(self, module: Module):
        self.help_list[module.name] = module.as_dict()
    
    def format(self, _module, prefix) -> str:
        module: Module = self.get(_module, None)
        if module is None:
            return b("модуль ") + html_code(_module) + b("Не найден!")
        o  = 'Модуль (плагин) ' + b(module.name) + "\n"
        o += ('  Разработчик: ' + b(module.author) + "\n" if module.author else '')
        o += ('  Описание: ' + module.description + "\n" if module.description else '')
        o +=  '  Комманды:\n'
        for command in module.commands:
            o += f'    • {b(command["description"])}\n    '
            o += '|'.join(map(lambda c: f'{html_code(prefix + c)}', command['commands']))
            o += ' '
            for arg in command.get('args', []):
                o += f'[{arg}] '
            o += '\n'
        return o

    def get_modules(self) -> list[str]:
        return list(self.help_list.keys())

    def get_modules_count(self) -> int:
        return int(len(self.help_list))
    
    def get_commands_count_module(self, module: str) -> int:
        return int(len(self.help_list.get(module, [])))
    
    def get_commands_count(self) -> int:
        return int(sum([
            self.get_commands_count_module(module)
            for module in self.get_modules()
        ]))

