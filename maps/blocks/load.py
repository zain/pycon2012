from django.contrib.gis.utils import LayerMapping
from blocks.models import Block, Water

block_mapping = {
    'poly' : 'POLYGON',
}

def blocks():
    lm = LayerMapping(Block, '../data/blocks/tl_2010_06075_tabblock10.shp', block_mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(silent=True)


water_mapping = {
    'poly': 'POLYGON'
}

def water():
    lm = LayerMapping(Water, '../data/water/tl_2009_06075_areawater.shp', water_mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(silent=True)


def clean():
    for w in Water.objects.all():
        Block.objects.filter(poly__intersects=w.poly).delete()
