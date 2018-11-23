from django.db import models
from django.urls import reverse


# Create your models here.
class List(models.Model):
    id = models.AutoField(primary_key=True)

    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])


class Item(models.Model):
    class Meta:
        unique_together = ("list", "text")

    text = models.TextField(default="", blank=False)
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
