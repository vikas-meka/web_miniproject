from django.db import models

class teacher(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    course1  = models.CharField(max_length=150)
    credits  = models.IntegerField(blank=True,null=True)
    
    def __str__ (self):
        return self.username
    

class marks(models.Model):
    roll_no = models.CharField(max_length=150)
    course = models.CharField(max_length=150)
    ct1 = models.IntegerField(blank=True,null=True)
    ct2 = models.IntegerField(blank=True,null=True)
    end = models.IntegerField(blank=True,null=True)
    internals = models.IntegerField(blank=True,null=True)
    total = models.IntegerField(blank=True,null=True)
    grade = models.IntegerField(blank=True,null=True)
    score = models.CharField(max_length=1,blank=True,null=True)

    # def __str__ (self):
    #     return self.roll_no

    def __str__(self):
     template = '{0.roll_no} {0.course}'
     return template.format(self)

class course(models.Model):
    key = models.CharField(max_length=255,blank=True,null=True)
    course = models.CharField(max_length=255,blank=True,null=True)

class grade(models.Model):
    roll_no = models.CharField(max_length=150,blank=True,null=True)
    cgpa = models.CharField(max_length=4,blank=True,null=True)   

    
    def __str__ (self):
        return self.roll_no
      


