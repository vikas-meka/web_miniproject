from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from .models import teacher,marks,course,grade,student_details,admin_details
from .forms import student_marks
from django.db import connection

def index(request):

    # if request.user.is_anonymous:
    #     return redirect("/login") 

    return render(request, 'index.html')

def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        test=teacher.objects.all()

        for i in test:
            if (i.username==username and i.password==password):
                  context = { 'course': i.course1,}
                  
                  temp=course.objects.all()
                  for j in temp:
                      if(j.key=="course"):
                          print('abc')
                          j.course=i.course1
                          print(j.course)
                          j.save()

                  return render(request,'teacher.html', context)
        

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")

def admin_login(request):

    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        test=admin_details.objects.all()

        for i in test:
            if (i.username==username and i.password==password):
                return render(request,'adm.html')

    return render(request, 'admin_login.html')


def admin_logout(request):
    logout(request)
    return redirect("/admin_login")            
    

def marking(request):

    if request.method=="POST":
        
        roll_no = request.POST.get('roll_number')
        ct1 = request.POST.get('CT1')
        ct2 = request.POST.get('CT2')
        end = request.POST.get('END')
        internals = request.POST.get('INTERNALS')
        
        temp=course.objects.all()
        for j in temp:
            if(j.key=="course"):
                sub=j.course

        test=marks.objects.all()
        for i in test:
            if (i.roll_no==roll_no and i.course==sub): 
                i.ct1=ct1
                i.ct2=ct2
                i.end=end
                i.internals=internals
                i.total=int(ct1)+int(ct2)+int(end)+int(internals)
                i.save()
                
                    
    return render(request, 'marking.html')

def admin(request):
    return render(request, 'adm.html')


def student(request):
    
    return render(request, 'student.html')


def calculate(request):
    print("abc")

    t1=teacher.objects.all()
    t2=marks.objects.all()
    t3=grade.objects.all()
    max=int(0)
    
    for i in t1:
         for j in t2:
             if(i.course1==j.course):
                if(j.total>max):
                  max=j.total 

         for j in t2:
             if(i.course1==j.course):
                 if(j.total>0.9*max):
                    j.grade=10
                    j.score='S'

                 elif(j.total>0.8*max):
                    j.grade=9
                    j.score='A'

                 elif(j.total>0.7*max):
                    j.grade=8
                    j.score='B'

                 elif(j.total>0.6*max):
                    j.grade=7
                    j.score='C' 

                 elif(j.total>0.5*max):
                    j.grade=6
                    j.score='D'

                 elif(j.total>0.3*max):
                    j.grade=5
                    j.score='E'

                 else:
                    j.grade=0
                    j.score='F' 

             j.save()     

    
  
    for i in t3:
        with connection.cursor() as cursor:
            cursor.execute("SELECT HOME_MARKS.ROLL_NO, SUM(HOME_TEACHER.CREDITS * HOME_MARKS.GRADE) / SUM(HOME_TEACHER.CREDITS) FROM HOME_MARKS LEFT JOIN HOME_TEACHER ON HOME_MARKS.COURSE = HOME_TEACHER.COURSE1 GROUP BY HOME_MARKS.ROLL_NO")
            query = cursor.fetchall()
            for each in query:
                if(i.roll_no==each[0]):
                    i.cgpa=each[1]
                    i.save()

def add_delete_student(request):
    return render(request, 'adddel_stu.html')             
                
def add_student(request):

    if request.method=="POST":

      rollno = request.POST.get('roll_number')
      year = request.POST.get('year')
      branch = request.POST.get('branch')
      name = request.POST.get('name')
      dob = request.POST.get('dob')

      t1=teacher.objects.all()
     
      for i in t1:
            if(i.year==year and i.branch==branch):
                marks_obj = marks(roll_no=rollno, course=i.course1)
                marks_obj.save()

      grade_obj = grade(roll_no=rollno)
      grade_obj.save()
      
      student_obj = student_details(roll_no=rollno, name=name, year=year, branch=branch, password=dob)
      student_obj.save()
    

    return render(request, 'adddel_stu.html')

def delete_student(request):

    if request.method=="POST":

      action = request.POST.get('value')
      rollno = request.POST.get('roll_number')

      t1=teacher.objects.all()
      t2=marks.objects.all()
      t3=grade.objects.all()
      t4=student_details.objects.all()
      

      for i in t2:
        if(rollno==i.roll_no):
            i.delete()

      for j in t3:
        if(rollno==j.roll_no):
            j.delete()
                   
      for k in t4:
        if(rollno==k.roll_no):
            k.delete()
                       
    return render(request, 'adddel_stu.html')

def add_delete_course(request):
    return render(request, 'adddel_cou.html') 

def add_course(request):
    if request.method == "POST":
        course = request.POST.get('course')
        password = request.POST.get('password')
        credits = int(request.POST.get('credits'))
        year = request.POST.get('year')
        branch = request.POST.get('branch')

        t1 = teacher.objects.all()
        t2 = marks.objects.all()
        t5 = student_details.objects.all()

        new_object = teacher(username=course, password=password, course1=course, credits=credits, year=year, branch=branch)
        new_object.save()

        for i in t5:
            if(i.year==year and i.branch==branch):
                marks_obj = marks(roll_no=i.roll_no, course=i.course)
                marks_obj.save()

    return render(request, 'adddel_cou.html')

def delete_course(request):
    if request.method == "POST":
        course = request.POST.get('course')

        t1 = teacher.objects.all()
        t2 = marks.objects.all()

        for i in t1:
            if i.course1 == course:
                i.delete()

        for j in t2:
            if j.course == course:
                j.delete()

    return render(request, 'adddel_cou.html')

def change_pwd(request):

    if request.method == "POST":
        username = request.POST.get('username')
        key = request.POST.get('key')
        password = request.POST.get('password')

        t1 = teacher.objects.all()
        t5 = student_details.objects.all()

        if(key=="student"):
            for i in t5:
                if(username==i.roll_no):
                    i.password=password
                    i.save()
            
        if(key=="course"):
            for i in t1:
                if(username==i.username):
                    i.password=password
                    i.save()            

    return render(request, 'change_password.html')        
                   




    
            

    
    

# def teacher(request):
#      return render(request, 'teacher.html')

# def tea_login(request):
#     if request.method=="POST":
                
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         for item in teacher.object.all:

#             if[item.username==username and item.password==password]:
#                 return redirect("/index")


#         '''user = authenticate(username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect("/")

#         else:
#             return render(request, 'login.html')'''

# def studentmarks(request):
     
#     f1=student_marks()
#     data={'form':f1}
