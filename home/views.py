from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from .models import course,mark,course_key,grade,student_detail,admin_detail,student_password,admin_key
from .forms import student_marks
from django.db import connection
from django.contrib import messages
import random
import pandas as pd

def index(request):

    return render(request, 'index.html')

def loginUser(request):

    name = None
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        test=course.objects.all()
        
        

        for i in test:
            if (i.username==username and i.password==password):
                  sub=i.course1
                  name=i.teacher

                  com=0
                  tot=0
                 
                  temp2=mark.objects.all()
                  for k in temp2 :
                      if(k.course==sub):
                          tot+=1
                            
                      if(k.course==sub) and (k.total is None) :
                          com+=1

                  com = tot-com                   
                  
                  temp=course_key.objects.all()
                  for j in temp:
                      if(j.key=="course"):
                          j.course=i.course1
                          j.total_marks=tot
                          j.entered_marks=com
                          j.name=i.teacher                                  
                          j.save()


                  context = { 'course': sub, 
                              'name' : name,
                              'total' : tot,
                              'entered' : com
                            }     

                  print(tot)
                  return render(request,'teacher.html', context)
        
        messages.error(request, "Incorrect credentials")
        return redirect('/login') 
    
    return render(request, 'login.html', {'name': name})

def faculty_dashbaord(request):

    temp=course_key.objects.all()
    for j in temp:
        if(j.key=="course"):
           sub= j.course
           name=j.name
           tot=j.total_marks
           com=j.entered_marks

           context = { 'course': sub, 
                              'name' : name,
                              'total' : tot,
                              'entered' : com
                            }
           
    return render(request,'faculty_dashboard.html', context)


def admin_dashbaord(request):
          
    temp=admin_key.objects.all()
    for j in temp:
           if(j.key=="admin"):
            name=j.name
            tot=j.total_courses
            com=j.entered_courses                                
            
    context = { 
       'name' : name,
       'total' : tot,
       'entered' : com
     }
           
    return render(request,'admin_dashboard.html', context)

       

def logoutUser(request):
    logout(request)
    return redirect("/login")

def admin_login(request):

    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        test=admin_detail.objects.all()

        for i in test:
            if (i.username==username and i.password==password):
                name=i.name

                tot=-1
                com=0
                key=0

                cou_obj=course.objects.all()
                mark_obj=mark.objects.all()
                for m in cou_obj:
                    for n in mark_obj:
                        if(m.course1==n.course):
                            if n.total is None:
                                key=1

                    tot+=1
                    if key==1:
                        com+=1

                com = tot-com


                temp=admin_key.objects.all()
                for j in temp:
                       if(j.key=="admin"): 
                        j.name=i.name
                        j.total_courses=tot
                        j.entered_courses=com                                 
                        j.save()

                context = { 
                   'name' : name,
                   'total' : tot,
                   'entered' : com
                 }        

                print(tot) 
                print(com)                 
                return render(request,'adm.html',context)
        
        messages.error(request, "Incorrect credentials")
        return redirect('/admin_login') 
    return render(request, 'admin_login.html')


def admin_logout(request):
    logout(request)
    return redirect("/admin_login") 

def teacher(request):

    return render(request, 'teacher.html')

def adm(request):

    return render(request, 'adm.html')



def markingman(request):
    
    course_obj = request.GET.get('course')

    temp=course_key.objects.all()
    for j in temp:
        if(j.key=="course"):
           sub= j.course
           name=j.name
           tot=j.total_marks
           com=j.entered_marks

           context = { 'course': sub, 
                              'name' : name,
                              'total' : tot,
                              'entered' : com
                            }
       
    if request.method=="POST":
        
        roll_no = request.POST.get('roll_number')
        ct1 = request.POST.get('CT1')
        ct2 = request.POST.get('CT2')
        end = request.POST.get('END')
        internals = request.POST.get('INTERNALS')
        
        temp=course_key.objects.all()
        for j in temp:
            if(j.key=="course"):
                sub=j.course

        test=mark.objects.all()
        for i in test:
            if (i.roll_no==roll_no and i.course==sub): 
                i.ct1=ct1
                i.ct2=ct2
                i.end=end
                i.internals=internals
                i.total=int(ct1)+int(ct2)+int(end)+int(internals)
                i.save()
                
                    
    return render(request, 'marking.html', context)



import pandas as pd

def marking(request):

    temp=course_key.objects.all()
    for j in temp:
        if(j.key=="course"):
           sub= j.course
           name=j.name
           tot=j.total_marks
           com=j.entered_marks

           context = { 'course': sub, 
                              'name' : name,
                              'total' : tot,
                              'entered' : com
                            }

    temp=course_key.objects.all()
    for j in temp:
        if(j.key=="course"):
            sub=j.course    

    if request.method == "POST":
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            if excel_file.name.endswith('.xls') or excel_file.name.endswith('.xlsx'):
                
                df = pd.read_excel(excel_file)

                for index, row in df.iterrows():
                    roll_no = str(row['roll_number'])

                    ct1 = row['CT1']
                    ct2 = row['CT2']
                    end = row['END']
                    internals = row['INTERNALS']

                    
                    test=mark.objects.all()
                    for i in test:
                        if (i.roll_no==roll_no and i.course==sub): 
    
                            i.ct1=ct1
                            i.ct2=ct2
                            i.end=end
                            i.internals=internals
                            i.total=int(ct1)+int(ct2)+int(end)+int(internals)
                            i.save()
                    
            else:
                messages.error(request, 'Please upload a valid Excel file.')
        else:
            messages.error(request, 'No file uploaded.')
    
    return render(request, 'marking.html', context)



def admin(request):
    return render(request, 'adm.html')


def student(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        test = student_password.objects.all()
        key=1
        t3=grade.objects.all()
        for i in t3:
            if(i.roll_no==username):
                if i.cgpa is None:
                    key=0

        for i in test:
            if i.username == username and i.password == password:
                if(key==1):
                    rollno = username
                    t6 = student_detail.objects.get(roll_no=username)
                    t5 = grade.objects.get(roll_no=username)
                    t2 = mark.objects.filter(roll_no=username)
                    t1 = course.objects.all()
                        
                    context = {
                        'name': t6.name,
                        'rollno': rollno,
                        'year': t6.year,
                        'branch': t6.branch,
                        'cgpa': t5.cgpa,
                        'marks': t2,
                        'courses': t1
                    }
                
                    return render(request, 'student.html', context)
                
                else:
                    messages.error(request, "Results are not yet declared")
                    return redirect('/student')
            
            
        messages.error(request, "Incorrect credentials")
        return redirect('/student')
            
    return render(request, 'student_login.html')


def calculate(request):

    temp=admin_key.objects.all()
    for j in temp:
           if(j.key=="admin"):
            name=j.name
            tot=j.total_courses
            com=j.entered_courses                                
            
    context = { 
       'name' : name,
       'total' : tot,
       'entered' : com
     }
    

    t1 = course.objects.all()
    t2 = mark.objects.all()
    t3 = grade.objects.all()
    max_total = int(0)
    total = int(0)

    missing_course = None

    missing_courses = [] 

    for teacher_item in t1:
        for m in t2:
            if teacher_item.course1 == m.course:
                if m.total is not None:
                    
                    if m.total > total:
                        total = m.total

                    if m.total > 0.9 * total:
                        m.grade = 10
                        m.score = 'S'
                    elif m.total > 0.8 * total:
                        m.grade = 9
                        m.score = 'A'
                    elif m.total > 0.7 * total:
                        m.grade = 8
                        m.score = 'B'
                    elif m.total > 0.6 * total:
                        m.grade = 7
                        m.score = 'C'
                    elif m.total > 0.5 * total:
                        m.grade = 6
                        m.score = 'D'
                    elif m.total > 0.3 * total:
                        m.grade = 5
                        m.score = 'E'
                    else:
                        m.grade = 0
                        m.score = 'F'
                else:
                    missing_course = m.course  
                    if m.course not in missing_courses:
                        missing_courses.append(m.course)                  

                m.save()

    for i in t1:
        if(i.credits==0):
            for j in t2:
                if(j.course==i.course1):
                    if(j.score=="F"):
                        j.score="Unsatisfactory"
                        j.save()
                    else:
                        j.score="Satisfactory"
                        j.save()

    for teacher_item in t3:
         with connection.cursor() as cursor:
            cursor.execute("SELECT HOME_MARK.ROLL_NO, ROUND(CAST(SUM(HOME_COURSE.CREDITS * HOME_MARK.GRADE*1.0)AS FLOAT) / SUM(HOME_COURSE.CREDITS), 2) FROM HOME_MARK LEFT JOIN HOME_COURSE ON HOME_MARK.COURSE = HOME_COURSE.COURSE1 GROUP BY HOME_MARK.ROLL_NO")
            query = cursor.fetchall()
            for each in query:
                if(teacher_item.roll_no==each[0]):
                    teacher_item.cgpa=each[1]
                    teacher_item.save()

    for m in t2:
            if(m.score=="F" or m.score=="Unsatisfactory"):    
                for i in t3:
                    if(i.roll_no==m.roll_no):
                        i.cgpa="--"
                        i.save()                    

    if missing_courses:
        missing_courses_message = ", ".join(missing_courses)
        messages.error(request, f"The following courses should be filled first to calculate: {missing_courses_message}")
        return render(request, 'adm.html', context)
    else:
        messages.success(request, "Result successfully calculated")
        return render(request, 'adm.html', context)
    



def add_delete_student(request):

    temp=admin_key.objects.all()
    for j in temp:
           if(j.key=="admin"):
            name=j.name
            tot=j.total_courses
            com=j.entered_courses                                
            
    context = { 
       'name' : name,
       'total' : tot,
       'entered' : com
     }


    return render(request, 'adddel_stu.html',context)             
                
def add_studentman(request):

    temp=admin_key.objects.all()
    for j in temp:
           if(j.key=="admin"):
            name=j.name
            tot=j.total_courses
            com=j.entered_courses                                
            
    context = { 
       'name' : name,
       'total' : tot,
       'entered' : com
     }

    if request.method=="POST":

      rollno = request.POST.get('roll_number')
      year = request.POST.get('year')
      branch = request.POST.get('branch')
      name = request.POST.get('name')
      dob = request.POST.get('dob')

      t1=course.objects.all()
      t6=student_detail.objects.all()
      
      key=1
      for m in t6:
          if(m.roll_no==rollno):
             key=0 

      if(key==1): 
        for i in t1:
              if(i.year==year and i.branch==branch):
                  marks_obj = mark(roll_no=rollno, course=i.course1)
                  marks_obj.save()

        grade_obj = grade(roll_no=rollno)
        grade_obj.save()
      
        stu_pwd = student_password(username=rollno, password=dob)
        stu_pwd.save()

        student_obj = student_detail(roll_no=rollno, name=name, year=year, branch=branch, password=dob)
        student_obj.save()
        
        messages.error(request,"Student added successfully")
        return redirect('/add_student')  
      else:
          messages.error(request,"Student already exists")
          return redirect('/add_student')

    return render(request, 'adddel_stu.html',context)

def add_student(request):

    temp=admin_key.objects.all()
    for j in temp:
           if(j.key=="admin"):
            name=j.name
            tot=j.total_courses
            com=j.entered_courses                                
            
    context = { 
       'name' : name,
       'total' : tot,
       'entered' : com
     }


    if request.method == "POST":
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            if excel_file.name.endswith('.xls') or excel_file.name.endswith('.xlsx'):
                df = pd.read_excel(excel_file)

                for index, row in df.iterrows():
                    rollno = row['roll_number']
                    name = row['name']
                    year = row['year']
                    branch = row['branch']

                    t1 = course.objects.all()
                    t6 = student_detail.objects.all()

                    key = 1
                    for m in t6:
                        if m.roll_no == rollno:
                            key = 0 

                    if key == 1: 
                        for i in t1:
                            if i.year == year and i.branch == branch:
                                marks_obj = mark(roll_no=rollno, course=i.course1)
                                marks_obj.save()
                      
                        grade_obj = grade(roll_no=rollno)
                        grade_obj.save()
                        
                        stu_pwd = student_password(username=rollno, password=rollno)
                        stu_pwd.save()
                        
                        student_obj = student_detail(roll_no=rollno, name=name, year=year, branch=branch, password=rollno)
                        student_obj.save()
                    
                    else:
                        messages.error(request, "Student with roll number {} already exists".format(rollno))

                messages.error(request, "Students added successfully")
                return redirect('/add_student') 

            else:
                messages.error(request, 'Please upload a valid Excel file.')
        else:
            messages.error(request, 'No file uploaded.')

    return render(request, 'adddel_stu.html',context)



def delete_student(request):

    temp=admin_key.objects.all()
    for j in temp:
           if(j.key=="admin"):
            name=j.name
            tot=j.total_courses
            com=j.entered_courses                                
            
    context = { 
       'name' : name,
       'total' : tot,
       'entered' : com
     }



    key = 0
    if request.method == "POST":
        rollno = request.POST.get('roll_number')
        t1 = course.objects.all()
        t2 = mark.objects.all()
        t3 = grade.objects.all()
        t4 = student_detail.objects.all()
        t7 = student_password.objects.all()

        for i in t2:
            if rollno == i.roll_no:
                i.delete()
                key = 1  

        for j in t3:
            if rollno == j.roll_no:
                j.delete()

        for k in t4:
            if rollno == k.roll_no:
                k.delete()

        for l in t7:
            if rollno == l.username:
                l.delete()

        if key == 0:
            messages.error(request, "Student does not exist")
        else:
            messages.success(request, "Deleted Successfully")

        return redirect('/add_delete_student')

    return render(request, 'adddel_stu.html',context)

    
def add_delete_course(request):

    temp=admin_key.objects.all()
    for j in temp:
           if(j.key=="admin"):
            name=j.name
            tot=j.total_courses
            com=j.entered_courses                                
            
    context = { 
       'name' : name,
       'total' : tot,
       'entered' : com
     }
    return render(request, 'adddel_cou.html',context) 


def add_courseman(request):
    

    temp=admin_key.objects.all()
    for j in temp:
           if(j.key=="admin"):
            name=j.name
            tot=j.total_courses
            com=j.entered_courses                                
            
    context = { 
       'name' : name,
       'total' : tot,
       'entered' : com
     }

    if request.method == "POST":
        course_name = request.POST.get('course')
        password = request.POST.get('password')
        credits = request.POST.get('credits')
        year = request.POST.get('year')
        branch = request.POST.get('branch')
        name = request.POST.get('name')
        teacher = request.POST.get('teacher')

        t1 = course.objects.all()
        t2 = mark.objects.all() 
        t5 = student_detail.objects.all()

        key = 1
        for m in t1:
            if m.course1 == course_name:
                key = 0
                break 

        if key == 1:
            new_object = course(username=course_name, password=password, course1=course_name, credits=credits, year=year, branch=branch, name=name, teacher=teacher)
            new_object.save()
   
            for j in t5:
                if j.year == year and j.branch == branch:
                    marks_obj = mark(roll_no=j.roll_no, course=course_name)
                    marks_obj.save()

            messages.error(request,"Course added successfully")
            return redirect('/add_course')             
        else:
            messages.error(request, "Course already exists")
            return redirect('/add_course')
        
    return render(request, 'adddel_cou.html',context)

def add_course(request):

    temp=admin_key.objects.all()
    for j in temp:
           if(j.key=="admin"):
            name=j.name
            tot=j.total_courses
            com=j.entered_courses                                
            
    context = { 
       'name' : name,
       'total' : tot,
       'entered' : com
     }



    if request.method == "POST":
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            if excel_file.name.endswith('.xls') or excel_file.name.endswith('.xlsx'):
                df = pd.read_excel(excel_file)

                for index, row in df.iterrows():
                    course_name = row['code']
                    name = row['name']
                    credits = row['credits']
                    year = row['year']
                    branch = row['branch']
                    teacher = row['teacher'] 

                    t1 = course.objects.all()
                    t2 = mark.objects.all() 
                    t5 = student_detail.objects.all()
            
                    key = 1
                    for m in t1:
                        if m.course1 == course_name:
                            key = 0
                            break 
            
                    if key == 1:
                        new_object = course(username=course_name, password=course_name, course1=course_name, credits=credits, year=year, branch=branch, name=name, teacher=teacher)
                        new_object.save()
               
                        for j in t5:
                            if j.year == str(year) and j.branch == branch:
                                marks_obj = mark(roll_no=j.roll_no, course=course_name)
                                marks_obj.save()
                       
                    else:
                        messages.error(request, "Course {} already exists".format(course_name))

                return redirect('/add_course')

            else:
                messages.error(request, 'Please upload a valid Excel file.')
        else:
            messages.error(request, 'No file uploaded.')

    return render(request, 'adddel_cou.html',context)



def delete_course(request):

    temp=admin_key.objects.all()
    for j in temp:
           if(j.key=="admin"):
            name=j.name
            tot=j.total_courses
            com=j.entered_courses                                
            
    context = { 
       'name' : name,
       'total' : tot,
       'entered' : com
     }


    key = 0
    if request.method == "POST":
        course_name = request.POST.get('course')  

        t1 = course.objects.all()
        t2 = mark.objects.all()

        for i in t1:
            if i.course1 == course_name: 
                i.delete()
                key = 1

        for j in t2:
            if j.course == course_name: 
                j.delete()
        
        if key == 0:
            messages.error(request, "Course does not exist")
        else:
            messages.success(request, "Deleted Successfully")

        return redirect('/add_delete_course')
    
    return render(request, 'adddel_cou.html',context)


def change_pwd(request):

    temp=admin_key.objects.all()
    for j in temp:
           if(j.key=="admin"):
            name=j.name
            tot=j.total_courses
            com=j.entered_courses                                
            
    context = { 
       'name' : name,
       'total' : tot,
       'entered' : com
     }

    if request.method == "POST":
        username = request.POST.get('username')
        key = request.POST.get('key')
        password = request.POST.get('password')

        t1 = course.objects.all()
        t5 = student_detail.objects.all()

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

    return render(request, 'change_password.html',context)   

def random_function(request):
    t2=mark.objects.all()

    for i in t2:
        i.total = random.randint(25, 100)
        i.save()
    
    messages.success(request,"Random marks inserted") 
    return render(request, 'adm.html')


def clear(request):
    t2=mark.objects.all()
    t5=grade.objects.all()

    for i in t2:
        i.total = None
        i.grade = None
        i.score = None
        i.save()

    for j in t5:
        j.cgpa = None
        j.save()    
    
    messages.success(request,"Marks data removed")
    return render(request, 'adm.html')  

def exit_home(request):
      return render(request, 'index.html')


def exit_faculty(request):
     return render(request, 'teacher.html')

def teacher_logout(request):
      return render(request, 'teacher_login.html')

def mark_list(request):
    temp=course_key.objects.all()
    for j in temp:
        if(j.key=="course"):
            sub=j.course

    mark_obj = mark.objects.filter(course=sub)  
    context = {'marks' : mark_obj} 
    return render(request, 'mark_list.html', context)  


