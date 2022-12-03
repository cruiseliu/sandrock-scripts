from sandrock import *

import UnityPy
from UnityPy.classes.Object import NodeHelper

ignore_types = [
    'AnimationClip',
    'AnimationController',
    'Animator',
    'AnimatorController',
    'AssetBundle',
    'AudioListener',
    'Avatar',
    'AudioMixerController',
    'AudioMixerGroupController',
    'AudioMixerSnapshotController',
    'BoxCollider',
    'Camera',
    'CanvasRenderer',
    'CapsuleCollider',
    'ComputeShader',
    'Cubemap',
    'Font',
    'LODGroup',
    'Light',
    'LightProbeGroup',
    'LightProbes',
    'LightmapSettings',
    'LineRenderer',
    'Material',
    'Mesh',
    'MeshCollider',
    'MeshFilter',
    'MeshRenderer',
    'NavMeshSettings',
    'ParticleSystem',
    'ParticleSystemRenderer',
    'PlayableDirector',
    'PreloadData',
    'RectTransform',
    'ReflectionProbe',
    'RenderSettings',
    'Rigidbody',
    'Shader',
    'SkinnedMeshRenderer',
    'SphereCollider',
    'SpriteRenderer',
    'LightProbeGroup',
    'TerrainCollider',
    'Texture2DArray',
    'Texture3D',
    'VideoClip',
    'WindZone',
]

def unpack_dir(path):
    path = Path(path)
    if not path.is_absolute():
        path = config.streaming_assets_dir / path
    files = sorted(path.rglob('*'))
    for file in files:
        if file.is_dir():
            continue
        rel = file.relative_to(config.streaming_assets_dir)
        unpack_bundle(rel)

def unpack_bundle(path, part=None):
    path = Path(path)
    if path.is_absolute():
        src = path
        rel = path.relative_to(config.streaming_assets_dir)
    else:
        src = config.streaming_assets_dir / path
        rel = path
    dst = config.assets_root / rel
    assert src.exists(), src

    if (dst / 'manifest.json').exists():
        print('skip', rel)
        return
    else:
        print('unpack', rel)

    bundle = UnityPy.load(str(src))
    if part is None:
        objects = bundle.objects
    else:
        cur_part, total_parts = part.split('/')
        cur_part = int(cur_part)
        total_parts = int(total_parts)
        n = len(bundle.objects) // total_parts
        if cur_part == total_parts - 1:
            objects = bundle.objects[(cur_part * n):]
        else:
            objects = bundle.objects[(cur_part * n):(cur_part * n + n)]

    assets = []
    scripts = []

    for i, reader in enumerate(objects):
        info = {}
        assets.append(info)

        reader_info = {
            'type': getattr(getattr(reader, 'type', None), 'name', None),
            'file_id': getattr(reader, 'file_id', None),
            'path_id': getattr(reader, 'path_id', None),
            'name': getattr(reader, 'name', None),
            'container': getattr(reader, 'container', None),
        }
        _update_info(info, reader_info)

        try:
            obj = reader.read()
        except Exception as e:
            info['fail'] = True
            print(f'#  Failed to read [{i}] {rel}:', repr(e))
            continue

        try:
            obj_info = {
                'type': getattr(getattr(obj, 'type', None), 'name', None),
                'file_id': getattr(obj, 'file_id', None),
                'path_id': getattr(obj, 'path_id', None),
                'name': getattr(obj, 'name', None),
                'container': getattr(obj, 'container', None),
            }
        except Exception as e:
            info['fail'] = True
            print(f'#  Failed to read meta info [{i}] {rel}:', repr(e))
            continue

        _update_info(info, obj_info)

        if info.get('name'):
            file_name = info['name'].replace('/', '!') + ' #' + str(info['path_id'])
        else:
            file_name = str(info['path_id'])

        if info['type'] in ignore_types:
            continue

        elif info['type'] == 'MonoScript':
            tree = reader.read_typetree()
            script = {
                'id': info['path_id'],
                'name': tree.get('m_Name'),
                'class': tree.get('m_ClassName'),
                'namespace': tree.get('m_Namespace'),
            }
            scripts.append(script)

        elif info['type'] == 'TextAsset':
            dst_txt = dst / info['type'] / (file_name + '.txt')
            dst_txt.parent.mkdir(parents=True, exist_ok=True)
            dst_txt.write_bytes(obj.script)

        elif info['type'] in ['Sprite', 'Texture2D']:
            dst_img = dst / '_image_' / (file_name + '.png')
            dst_img.parent.mkdir(parents=True, exist_ok=True)
            try:
                obj.image.save(str(dst_img))
            except Exception as e:
                info['fail'] = True
                print(f'#   Failed to save image [{i}] {rel}:', repr(e))

        else:
            dst_obj = dst / info['type'] / (file_name + '.json')
            dst_obj.parent.mkdir(parents=True, exist_ok=True)
            try:
                tree = reader.read_typetree()
                text = json.dumps(tree, ensure_ascii=False, indent=4, default=_serialize)
                dst_obj.write_text(text)
            except Exception as e:
                info['fail'] = True
                print(f'#   Failed to save json [{i}] {rel}:', repr(e))
                print(info)
                print(file_name)

    manifest = {'assets': assets, 'scripts': scripts}
    if part is None:
        write_json(dst / 'manifest.json', manifest)
    else:
        write_json(dst / f'manifest-{cur_part}-{total_parts}.json', manifest)
        if cur_part == total_parts - 1:
            all_assets = []
            all_scripts = []
            for i in range(total_parts):
                part_manifest = read_json(dst / f'manifest-{i}-{total_parts}.json')
                all_assets += part_manifest['assets']
                all_scripts += part_manifest['scripts']
            full_manifest = {'assets': all_assets, 'scripts': all_scripts}
            write_json(dst / 'manifest.json', full_manifest)

def _update_info(old, new):
    for k, v in new.items():
        if v:
            if k in old:
                assert old[k] == v
            else:
                old[k] = v

def _serialize(obj):
    return f'<{type(obj).__module__}.{type(obj).__name__}>'
