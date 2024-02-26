# from django.db import models
from django.contrib.auth.models import User
from djongo import models

# Create your models here.

class Expenses(models.Model):
    """Expense model"""

    class Choice(models.TextChoices):
        Onetime = '60'
        Twotime = '110'
        Threetime = '150'

    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    date = models.DateField()
    choice = models.CharField(max_length=50,choices =Choice.choices,default = Choice.Threetime)
    deposit = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.choice

    def get_absolute_url(self):
        return reverse("calculate:base", kwargs={"pk": self.pk})

    