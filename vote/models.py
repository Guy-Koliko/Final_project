from django.db import models
from django.db.models.deletion import CASCADE


class Region(models.Model):
    region_name = models.CharField(max_length=100)
    region_code = models.CharField(max_length=10 , default = 0)
    
    def __str__(self) -> str:
        return self.region_name
    
class Constituency(models.Model):
    constituency_name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=CASCADE)
    constituency_code = models.CharField(max_length=10 ,default = 0)
    def __str__(self) -> str:
        return self.constituency_name

    
class PollingStation(models.Model):
    polling_station_name = models.CharField(max_length=100)
    member_of = models.ForeignKey(Constituency, on_delete=CASCADE)
    pollingstation_code = models.CharField(max_length=10 ,default = 0)
    
    def __str__(self) -> str:
        
        return "{} ".format(self.polling_station_name)
    
class Tag(models.Model):
    name = models.ForeignKey(PollingStation, on_delete=CASCADE)
    def __str__(self):
        return "{}".format(self.name)


class PoliticalParty(models.Model): #affiliated to PS amd C  
    name = models.CharField(max_length=100)
    polling_station = models.ForeignKey(Region,on_delete=CASCADE)
    constituency_name = models.ForeignKey(Constituency,on_delete=CASCADE)
    tag = models.ManyToManyField(Tag)
    def __str__(self) -> str:
        return "{} ".format(self.name)

class PoliticalPartyPSStats(models.Model): #polling station affiliated (summary of votes)
    name = models.CharField(max_length=100)
    polling_station = models.ForeignKey(PollingStation ,on_delete=CASCADE)
    def __str__(self) -> str:
        return "{} ".format(self.name)

class PoliticalPartyCStats(models.Model): #constituency affiliated (summary of votes )
    name = models.CharField(max_length=100)
    constituency_name = models.ForeignKey(Constituency,on_delete=CASCADE)
    def __str__(self) -> str:
        return "{} ".format(self.name)

class PoliticalPartyRStats(models.Model): #Region affiliated (summary of votes )
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region,on_delete=CASCADE)
    def __str__(self) -> str:
        return "{} ".format(self.name)