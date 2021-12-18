from django.db import models
from django.db.models.deletion import CASCADE


class Region(models.Model):
    region_name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.region_name
    
class Constituency(models.Model):
    constituency_name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=CASCADE)
    def __str__(self) -> str:
        return self.constituency_name

    
class PollingStation(models.Model):
    polling_station_name = models.CharField(max_length=100)
    member_of = models.ForeignKey(Constituency, on_delete=CASCADE)
    
    def __str__(self) -> str:
        
        return "{} ".format(self.polling_station_name)
    
class Tag(models.Model):
    name = models.ForeignKey(PollingStation, on_delete=CASCADE)
    def __str__(self):
        return "{}".format(self.name)
    
class PoliticalParty(models.Model):
    name = models.CharField(max_length=100)
    polling_station = models.ForeignKey(Region,on_delete=CASCADE)
    constituency_name = models.ForeignKey(Constituency,on_delete=CASCADE)
    tag = models.ManyToManyField(Tag)
    def __str__(self) -> str:
        return "{} ".format(self.name)