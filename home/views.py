from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from .models import teacher,marks,course,grade
from .forms import student_marks
from django.db import connection

def index(request):

    if request.user.is_anonymous:
        return redirect("/login") 

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
             
                
def changepwd(request):
    print('abc')
             
            

    
    

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
