from .std import *
from .utils import *

sys.path.append(str(Path(__file__).parents[1]))
import config
sys.path.pop()

class Vector3(TypedDict):
    x: float
    y: float
    z: float
