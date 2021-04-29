from django.db import models

# Create your models here.

class Specialty(models.Model):
    name =  models.CharField(max_length=30)


    def __str__(self):
        return self.name

class Corp(models.Model):
    name = models.CharField(max_length=60)
    code = models.IntegerField()   


    def __str__(self):
        return self.name

class Access(models.Model):
    name = models.CharField(max_length=60)
    code = models.IntegerField()   
    

    def __str__(self):
        return self.name

class Exclusion(models.Model):
    name = models.TextField()
    code = models.IntegerField()


    def __str__(self):
        return self.name

class DAT(models.Model):
    name = models.CharField()   


    def __str__(self):
        return self.name




class Teachers(models.Model):
    first_name = models.CharField(max_length=30)
    first_last_name = models.CharField(max_length=30)
    second_last_name = models.CharField(max_length=30)
    dni = models.CharField(max_length=10)
    l_inte = models.BooleanField()
    language_test = models.BooleanField()
    admitted = models.BooleanField()

    specialty = models.ForeignKey('Specialty',on_delete=models.SET_NULL)
    corp = models.ForeignKey('Corp',on_delete=models.SET_NULL)
    access = models.ForeignKey('Access',on_delete=models.SET_NULL)
    exclusion = models.ForeignKey('Exclusion',on_delete=models.SET_NULL)
    dat = models.ForeignKey('DAT',on_delete=models.SET_NULL)


    def __str__(self):
        return self.first_name + ' ' + self.first_last_name + ' ' + self.second_last_name    