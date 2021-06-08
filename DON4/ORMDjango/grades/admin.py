from django.contrib import admin
from .models import Teacher, Student, Group, Course, Enrolment

# Register your models here.

admin.site.register(Teacher),

class StudentInline(admin.TabularInline):
    model = Student
    extra = 0

class GroupAdmin(admin.ModelAdmin):
    inlines = [StudentInline]

admin.site.register(Group, GroupAdmin),

class EnrolmentInline(admin.TabularInline):
    model = Enrolment
    extra = 0

class StudentAdmin(admin.ModelAdmin):
    list_display = ('group', 'serial_number', 'first_name', 'last_name')
    fields = ['serial_number', 'first_name', 'last_name', 'birth_date']

    inlines = [EnrolmentInline]

admin.site.register(Student, StudentAdmin),

class CourseAdmin(admin.ModelAdmin):
    list_display = ('short_form', 'wording')
    inlines = [EnrolmentInline]

admin.site.register(Course, CourseAdmin)
