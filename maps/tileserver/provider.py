from blocks.models import Block
from crime.models import Crime
from django.contrib.gis.geos import  Polygon
from PIL import Image, ImageDraw, ImageFilter
import ModestMaps


GREEN = (90, 75, 40)
RED = (0, 100, 40)
WHITE = "rgb(255, 255, 255)"
HEATMAP_MIN = 5
HEATMAP_MAX = 15


class CrimeHeatmapProvider:
    def __init__(self, layer, *args, **kwargs):
        self.layer = layer
        self.provider = ModestMaps.OpenStreetMap.Provider()

    def renderArea(self, width, height, srs, xmin, ymin, xmax, ymax, zoom):
        # first, figure out the bounding box of the tile we're rendering
        nw = self.layer.projection.projLocation(ModestMaps.Core.Point(xmin, ymin))
        se = self.layer.projection.projLocation(ModestMaps.Core.Point(xmax, ymax))
        max_lat = max(nw.lat, se.lat)
        min_lat = min(nw.lat, se.lat)
        max_lon = max(nw.lon, se.lon)
        min_lon = min(nw.lon, se.lon)
        
        bbox = Polygon.from_bbox((min_lon, min_lat, max_lon, max_lat))
        
        # this obj is used to translate between lat/lon and pixel space
        bound1 = ModestMaps.Geo.Location(min_lat, min_lon)
        bound2 = ModestMaps.Geo.Location(max_lat, max_lon)
        mmap = ModestMaps.mapByExtentZoom(self.provider, bound1, bound2, zoom)
        
        # start drawing each block
        pil_map = Image.new("RGBA", (width, height), (255,255,255, 0))
        pil_draw = ImageDraw.Draw(pil_map)

        for block in Block.objects.filter(poly__intersects=bbox):

            # shape
            locs = []
            for c in block.poly.coords[0]:
                pt = ModestMaps.Geo.Location(c[1], c[0])
                loc = mmap.locationPoint(pt)
                locs.append((loc.x, loc.y))
            
            # color
            count = Crime.objects.filter(pt__within=block.poly).count()

            if count <= HEATMAP_MIN:
                h, s, l = GREEN
            elif count >= HEATMAP_MAX:
                h, s, l = RED
            else:
                scale = float(count - HEATMAP_MIN) / float(HEATMAP_MAX - HEATMAP_MIN)
                
                # scale all channels linearly between START_COLOR and END_COLOR
                h, s, l = [int(scale*(end-start) + start) for start, end in zip(GREEN, RED)]

            block_color = "hsl(%s, %s%%, %s%%)" % (h, s, l)
            pil_draw.polygon(locs, fill=block_color)
        
        return pil_map
