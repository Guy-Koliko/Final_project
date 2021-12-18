from django.db import models

# Create your models here.

class VoteConfirm(models.Model):
    vote_confirm = models.CharField(max_length=200)
    
    
    def __str__(self) -> str:
        return "{} ".format(self.vote_confirm)
        