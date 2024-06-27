from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    salary = models.IntegerField()
    expedition_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name