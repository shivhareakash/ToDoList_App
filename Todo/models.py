from django.db import models

# Create your models here.


class TodoDB(models.Model):
    item_text = models.CharField(max_length=100)
    date_added = models.DateTimeField()

    def __str__(self):
        return(self.item_text)