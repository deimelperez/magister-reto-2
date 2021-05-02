from django.db import models

# Create your models here.

class Specialty(models.Model):
    name =  models.TextField(unique=True)


    def __str__(self):
        return self.name

class Corp(models.Model):
    name = models.CharField(max_length=60,unique=True)
    code = models.IntegerField(unique=True)   


    def __str__(self):
        return self.name

class Access(models.Model):
    code = models.CharField(max_length=6,unique=True) 
    

    def __str__(self):
        return self.code

class Exclusion(models.Model):
    name = models.TextField(unique=True)
    code = models.IntegerField(unique=True)


    def __str__(self):
        return self.name

class DAT(models.Model):
    name = models.TextField(unique=True)


    def __str__(self):
        return self.name




class Teacher(models.Model):
    first_name = models.CharField(max_length=40)
    first_last_name = models.CharField(max_length=50)
    second_last_name = models.CharField(max_length=50)
    dni = models.CharField(max_length=15)
    l_inte = models.CharField(max_length=10)
    language_test = models.CharField(max_length=10)
    admitted = models.BooleanField()

    specialty = models.ForeignKey('Specialty',on_delete=models.DO_NOTHING,blank=True,null=True)
    corp = models.ForeignKey('Corp',on_delete=models.DO_NOTHING,blank=True,null=True)
    access = models.ForeignKey('Access',on_delete=models.DO_NOTHING,blank=True,null=True)
    exclusion = models.ManyToManyField('Exclusion',blank=True)
    dat = models.ForeignKey('DAT',on_delete=models.DO_NOTHING,blank=True,null=True)


    def __str__(self):
        return self.first_name + ' ' + self.first_last_name + ' ' + self.second_last_name    