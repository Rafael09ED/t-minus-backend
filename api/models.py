from django.db import models
from django.utils import timezone
import string
import random

def generateKey(length=32):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(length))

class Countdown(models.Model):
    name = models.CharField(max_length=128)
    time = models.DateTimeField()
    key = models.CharField(max_length=64, default=generateKey)
    created_at = models.DateField(default=timezone.now)


class CountdownEvent(models.Model):
    name = models.CharField(max_length=128)
    countdown = models.ForeignKey('Countdown', on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    time = models.DateTimeField()
