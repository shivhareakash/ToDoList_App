from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class TodoDB(models.Model):
    item_text = models.CharField(max_length=100)
    date_added = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return(self.item_text)