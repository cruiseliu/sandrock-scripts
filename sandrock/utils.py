__all__ = [
    'sorted_dict',
    'read_json',
    'write_text',
    'write_json',
    'write_yaml',
    'write_lua',
    'write_xml',
]

from .std import *
from .dump import lua_dump, yaml_dump

K = TypeVar('K')
T = TypeVar('T')
V = TypeVar('V')

def sorted_dict(dict_: dict[K, V]) -> dict[K, V]:
    return dict(sorted(dict_.items()))

@overload
def read_json(Path: PathLike) -> Any: ...
@overload
def read_json(Path: PathLike, json_type: Type[T]) -> T: ...
def read_json(path, json_type=None):
    with open(path) as f:
        return json.load(f)

def write_text(path: PathLike, text: str) -> None:
    with open(_resolve_path(path), 'w') as f:
        f.write(text)

def write_json(path: PathLike, data: Any) -> None:
    with open(_resolve_path(path), 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def write_yaml(path: PathLike, data: Any) -> None:
    s = yaml_dump(data, '', '    ')
    if isinstance(s, list):
        s = '\n'.join(s)
    _resolve_path(path).write_text(s)

def write_lua(path: PathLike, data: Any, indent: str = '\t') -> None:
    s = lua_dump(data, '', indent)
    _resolve_path(path).write_text('return ' + s)

def write_xml(path: PathLike, root: ElementTree.Element) -> None:
    ElementTree.ElementTree(root).write(_resolve_path(path), 'utf_8')

def _resolve_path(path: PathLike) -> Path:
    path = Path(path)
    if not path.is_absolute():
        from .common import config
        path = config.output_dir / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
