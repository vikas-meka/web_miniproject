from django.contrib import admin
from home.models import teacher, marks, course, grade, student_details, admin_details, student_password

admin.site.register(teacher)
admin.site.register(marks)
admin.site.register(course)
admin.site.register(grade)
admin.site.register(student_details)
admin.site.register(admin_details)
admin.site.register(student_password)


