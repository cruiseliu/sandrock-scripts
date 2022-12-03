from sandrock import *

def get_generator_group_items(group_id):
    group = DesignerConfig.GeneratorGroup[group_id]
    item_ids = set()
    for element in group['elements']:
        for id_weight in element['idWeights']:
            if id_weight['weight'] <= 0:
                continue
            generator = DesignerConfig.Generator_Item[id_weight['id']]
            if generator['randomType'] == 0 and generator['parameters'][0] <= 0:
                continue
            item_ids.add(generator['itemId'])
    return sorted(item_ids)
