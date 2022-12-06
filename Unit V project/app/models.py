from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BountyPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    target_name = models.CharField(max_length=20)
    description = models.TextField()
    bounty = models.IntegerField()
    WANTED = (
        ("Dead", "Dead"),
        ("Alive", "Alive"),
        ("Either", "Either"),
    )
    dead_or_alive = models.CharField(max_length=6, choices=WANTED)
    completed = models.BooleanField()

class Hunter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bountiesaccepted = models.ManyToManyField(BountyPost, related_name='accept_bounty', blank=True)
    total_money = models.IntegerField(null=True, blank=True)

def creating(user, tar, des, bou, doa, com):
    x = BountyPost(user=user, target_name=tar, description=des, bounty=bou, dead_or_alive=doa, completed=com)
    x.save()
    return x