from sandrock import *

from xml.etree import ElementTree

class Bundle:
    def __init__(self, path):
        if Path(path).is_absolute():
            self.path = Path(path)
        else:
            self.path = config.assets_root / path

        manifest = read_json(self.path / 'manifest.json')
        self.assets = [Asset(self, asset_info) for asset_info in manifest['assets'] if not asset_info.get('fail')]
        self.scripts = {script['id']: script['name'] for script in manifest['scripts']}

    def __iter__(self):
        return iter(self.assets)

    @property
    def behaviours(self):
        return [asset for asset in self.assets if asset.type == 'MonoBehaviour']

class Asset:
    def __init__(self, bundle, info):
        self.bundle = bundle
        self.id = info['path_id']
        self.type = info['type']
        self.name = info.get('name')
        self._data = None

    @property
    def data(self):
        if self._data is None:
            if self.type == 'TextAsset':
                self._data = self.path.read_text()
            else:
                self._data = read_json(self.path)
        return self._data

    @property
    def path(self):
        if self.type == 'TextAsset':
            ext = 'txt'
        else:
            ext = 'json'
        if self.name:
            rel_path = f'{self.type}/{self.name} #{self.id}.{ext}'
        else:
            rel_path = f'{self.type}/{self.id}.{ext}'
        return self.bundle.path / rel_path

    @property
    def image_path(self):
        if self.name:
            rel_path = f'_image_/{self.name} #{self.id}.png'
        else:
            rel_path = f'_image_/{self.id}.png'
        return self.bundle.path / rel_path

    @property
    def script(self):
        assert self.type == 'MonoBehaviour'
        script_id = self.data['m_Script']['m_PathID']
        return self.bundle.scripts.get(script_id)

    @property
    def transform(self):
        assert self.type == 'GameObject'
        comp_ids = [comp['component']['m_PathID'] for comp in self.data['m_Component']]
        for asset in self.bundle.assets:
            if asset.type == 'Transform' and asset.id in comp_ids:
                return asset

    @property
    def components(self):
        assert self.type == 'GameObject'
        comp_ids = [comp['component']['m_PathID'] for comp in self.data['m_Component']]
        comps = []
        for asset in self.bundle.assets:
            if asset.id in comp_ids:
                comps.append(asset)
        return comps

    @property
    def game_object(self):
        obj_id = self.data['m_GameObject']['m_PathID']
        objs = []
        for asset in self.bundle.assets:
            if asset.type == 'GameObject' and asset.id == obj_id:
                for comp in asset.data['m_Component']:
                    comp_id = comp['component']['m_PathID']
                    if comp_id == self.id:
                        return asset
        raise ValueError(f'GameObject not found: {obj_id}')

    def read_xml(self):
        assert self.type == 'TextAsset'
        return ElementTree.fromstring(self.data)
