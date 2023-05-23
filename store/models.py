from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=50)
    total_mark = models.PositiveIntegerField()
    grade = models.CharField(max_length=5)