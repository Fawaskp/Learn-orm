from django.db import models
from django.db.models import CheckConstraint, Q

from django.db.models.signals import pre_save
from django.dispatch import receiver

class Subjects(models.Model):
    subject = models.CharField(max_length=50)
    created_ate = models.DateTimeField(auto_now_add=True,null=True)
    update_at = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name_plural = 'Subjects'

    def __str__(self) -> str:
        return self.subject
    

class Teachers(models.Model):
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subjects,on_delete=models.SET_NULL,null=True)
    
    def __str__(self) -> str:
            return str(self.name)
    
    class Meta:
        verbose_name_plural = 'Teachers'
    

class Class(models.Model):
    class_name = models.CharField(max_length=50)
    class_teacher = models.ForeignKey(Teachers,on_delete=models.SET_NULL,null=True)
    strength = models.IntegerField(default=0)

    class Meta:
        constraints=[
            CheckConstraint(check=Q(strength__gte=0) & Q(strength__lte=100), name='strength_range'),
        ]
        
        verbose_name_plural = 'Classes'

    def __str__(self) -> str:
        return self.class_name

class Custom_Manager(models.Manager):

    def retrieve_male(self):
        return self.filter(gender="male")


class Student(models.Model):

    GENDER_CHOICE = [
        ('male','Male'),
        ('female','Female'),
    ]

    name = models.CharField(max_length=50)
    class_name = models.ForeignKey(Class,on_delete=models.SET_NULL,null=True)
    dob = models.DateField(null=True,blank=True)
    roll_no = models.IntegerField(unique=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICE,default='Not defined')


    def __str__(self) -> str:
        return self.name

@receiver(pre_save,sender=Student)
def show_updations_of_student(sender,instance,**kwargs):
    previous = sender.objects.get(id=instance.id)
    print('Old = ',previous.roll_no)
    print('New = ',instance.roll_no)




class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

class Employee(Person):
    job_title = models.CharField(max_length=100)
    salary = models.IntegerField()