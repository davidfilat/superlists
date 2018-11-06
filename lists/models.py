from django.db import models


# Create your models here.
class List(models.Model):
    id = models.AutoField(primary_key=True)


class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
