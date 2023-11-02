from django.db import models

class teacher(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    course1  = models.CharField(max_length=150)
    credits  = models.IntegerField(blank=True,null=True)
    year  = models.CharField(max_length=2,blank=True,null=True)
    branch  = models.CharField(max_length=4,blank=True,null=True)
    name = models.CharField(max_length=150,blank=True,null=True)

    
    def __str__ (self):
        return self.username
    

class marks(models.Model):
    roll_no = models.CharField(max_length=150)
    course = models.CharField(max_length=150)
    year  = models.CharField(max_length=2,blank=True,null=True)
    branch  = models.CharField(max_length=4,blank=True,null=True)    
    ct1 = models.IntegerField(blank=True,null=True)
    ct2 = models.IntegerField(blank=True,null=True)
    end = models.IntegerField(blank=True,null=True)
    internals = models.IntegerField(blank=True,null=True)
    total = models.IntegerField(blank=True,null=True)
    grade = models.IntegerField(blank=True,null=True)
    score = models.CharField(max_length=1,blank=True,null=True)

    def __str__(self):
     template = '{0.roll_no} {0.course} {0.year} {0.branch}'
     return template.format(self)
    
class student_details(models.Model):
    roll_no = models.CharField(max_length=150,blank=True,null=True)
    name = models.CharField(max_length=150,blank=True,null=True)
    year  = models.CharField(max_length=2,blank=True,null=True)
    branch  = models.CharField(max_length=4,blank=True,null=True)
    password  = models.CharField(max_length=15,blank=True,null=True)

    def __str__ (self):
        return self.roll_no
            
class course(models.Model):
    key = models.CharField(max_length=255,blank=True,null=True)
    course = models.CharField(max_length=255,blank=True,null=True)

class grade(models.Model):
    roll_no = models.CharField(max_length=150,blank=True,null=True)
    cgpa = models.CharField(max_length=4,blank=True,null=True)   

    
    def __str__ (self):
        return self.roll_no

class admin_details(models.Model):
    username = models.CharField(max_length=150,blank=True,null=True)
    password = models.CharField(max_length=150,blank=True,null=True)

    def __str__ (self):
        return self.username
    


