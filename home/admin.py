from django.contrib import admin
from home.models import course, mark, course_key, grade, student_detail, admin_detail, student_password, admin_key

admin.site.register(course)
admin.site.register(mark)
admin.site.register(course_key)
admin.site.register(grade)
admin.site.register(student_detail)
admin.site.register(admin_detail)
admin.site.register(student_password)
admin.site.register(admin_key)


