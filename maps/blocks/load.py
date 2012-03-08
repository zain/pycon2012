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
    ct = 1
    
    for b in Block.objects.all():
        if Water.objects.filter(poly__intersects=b.poly).count():
            b.delete()
        
        if ct % 1000 == 0: print ct
        ct += 1
