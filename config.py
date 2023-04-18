from pathlib import Path

version = 'V03.05.01.70168'

_root = Path(__file__).parent.resolve()
assets_root = _root / 'assets'
cache_root = _root / 'cache'
output_dir = _root / 'out'

languages = ['chinese', 'english']
language_codes = ['zh', 'en']
wiki_language = 'english'
