from django.db import models
from django.db.models.deletion import CASCADE
from vote.models import Region,Constituency,PoliticalParty,PollingStation
import uuid
import random

# Create your models here.
ids = str(uuid.uuid4().fields[-1])[:5]
new_id = random.Random(int(ids)).randint(20,60)


# # To-d Create seperate party agent model registration 

# will use thisas ther default model for party agent and any other agent registrations
class UserRegistrations(models.Model):
    num = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    personal = ('ec','political')
    region = models.ForeignKey(Region,on_delete=CASCADE)
    consituenc = models.ForeignKey(Constituency,on_delete=CASCADE)
    party = models.ForeignKey(PoliticalParty,on_delete=CASCADE)
    pollingstation = models.ForeignKey(PollingStation,on_delete=CASCADE)
    # id = models.UUIDField( default=uuid.uuid4, editable=False,max_length=6)
    phone_number = models.CharField(max_length=10)
    user_code = models.CharField(max_length=30,default = 0)
    

    def __str__(self) -> str:
        return "First Name : {} Last Name : {}".format(self.first_name,self.last_name)
    
    
class EcOfficial(models.Model):
        num = models.AutoField(primary_key=True)
        first_name = models.CharField(max_length=50)
        last_name = models.CharField(max_length=50)
        region = models.ForeignKey(Region,on_delete=CASCADE)
        consituenc = models.ForeignKey(Constituency,on_delete=CASCADE)
        pollingstation = models.ForeignKey(PollingStation,on_delete=CASCADE)
        # id = models.UUIDField( default=uuid.uuid4, editable=False,max_length=6)
        phone_number = models.CharField(max_length=10)
        user_code = models.CharField(max_length=30 ,default = 0)
        

        def __str__(self) -> str:
            return "First Name : {} Last Name : {}".format(self.first_name,self.last_name)
       
    


       
    