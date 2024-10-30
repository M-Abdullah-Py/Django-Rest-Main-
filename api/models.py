from django.db import models

# Create your models here.

class Student(models.Model):
    student_id = models.IntegerField()
    name = models.CharField(max_length=20)
    branch = models.CharField(max_length=50)

    def __str__(self):
        return self.name