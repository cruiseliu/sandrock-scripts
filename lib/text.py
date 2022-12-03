from sandrock import config
from .load import DesignerConfig, load_text

class TextEngine:
    @staticmethod
    def text(text_id, language=None, sep='  '):
        texts = []
        for lang, lang_code in zip(config.languages, config.language_codes):
            if language and language != lang and language != lang_code:
                continue
            s = load_text(lang).get(text_id)
            if s:
                texts.append(s)
        return sep.join(texts)

    @classmethod
    def __call__(cls, text_id, sep='  '):
        return cls.text(text_id, sep=sep)

    @classmethod
    def _designer_config_text(cls, config_key, id_, field_name, language=None):
        return cls.text(DesignerConfig[config_key][id_][field_name], language)

    @classmethod
    def item(cls, id_, language=None):
        name = cls._designer_config_text('ItemPrototype', id_, 'nameId', language)
        if language:
            return name
        else:
            return f'({id_}) {name}'

    @classmethod
    def expand_item_names(cls, id_):
        ret = {}
        for lang in config.language_codes:
            ret[f'name_{lang}'] = cls.item(id_, lang)
        return ret

    @classmethod
    def monster(cls, id_):
        return cls._designer_config_text('Monster', id_, 'nameId')

    @classmethod
    def resource(cls, id_):
        return cls._designer_config_text('ResourcePoint', id_, 'showNameID')

    @classmethod
    def scene(cls, id_):
        scenes = [scene for scene in DesignerConfig.Scene if scene['scene'] == id_]
        return cls.text(scenes[0]['nameId'])

    @classmethod
    def store(cls, id_):
        return cls._designer_config_text('StoreBaseData', id_, 'shopName')

    @classmethod
    def tree(cls, id_):
        return cls._designer_config_text('TerrainTree', id_, 'nameId')

class WikiTextEngine(TextEngine):
    @staticmethod
    def text(text_id, *arg, **kwargs):
        return load_text(config.wiki_language).get(text_id)

    @classmethod
    def item(cls, id_):
        # FIXME: disambiguation
        name = cls._designer_config_text('ItemPrototype', id_, 'nameId')
        if id_ >= 80000000:
            return name + ' (Book)'
        if id_ >= 70000000:
            return name + ' (Style)'
        return name

text = TextEngine()
wiki = WikiTextEngine()
