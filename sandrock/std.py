from collections import defaultdict
from collections.abc import Iterator
from functools import cache
import json
from pathlib import Path
import sys
from typing import (
    Any,
    Callable,
    TYPE_CHECKING,
    Type,
    TypeAlias,
    TypeVar,
    TypedDict,
    overload,
)
from xml.etree import ElementTree

PathLike: TypeAlias = Path | str
