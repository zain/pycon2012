from django.contrib.gis.db import models

class Block(models.Model):
    poly = models.PolygonField()

    objects = models.GeoManager()

    def __unicode__(self):
        return "Block #%s" % self.id


class Water(models.Model):
    poly = models.PolygonField()

    objects = models.GeoManager()
