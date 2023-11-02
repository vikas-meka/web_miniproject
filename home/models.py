from django.db import models

class teacher(models.Model):
    username = models.CharField(max_length=150,unique=True,blank=True,null=True)
    password = models.CharField(max_length=128,blank=True,null=True)
    course1  = models.CharField(max_length=150,primary_key=True)
    credits  = models.IntegerField(blank=True,null=True)
    year  = models.CharField(max_length=2,blank=True,null=True)
    branch  = models.CharField(max_length=4,blank=True,null=True)
    name = models.CharField(max_length=150,blank=True,null=True)

    
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

    def __str__(self):
     template = '{0.roll_no} {0.course}'
     return template.format(self)
    
class student_details(models.Model):
    roll_no = models.CharField(max_length=150,unique=True,primary_key=True)
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
    roll_no = models.CharField(max_length=150,blank=True,null=True,unique=True)
    cgpa = models.CharField(max_length=4,blank=True,null=True)   

    
    def __str__ (self):
        return self.roll_no

class admin_details(models.Model):
    username = models.CharField(max_length=150,blank=True,null=True)
    password = models.CharField(max_length=150,blank=True,null=True)    

    def __str__ (self):
        return self.username

class student_password(models.Model):
    username = models.CharField(max_length=150,blank=True,null=True)
    password = models.CharField(max_length=150,blank=True,null=True)    

    def __str__ (self):
        return self.username    


