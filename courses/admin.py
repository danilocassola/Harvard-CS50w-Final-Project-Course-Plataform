from django.contrib import admin

from .models import User, Course, Module, Lesson, Enrolled, DoneLesson

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
	list_display = ("title", "author")

class ModuleAdmin(admin.ModelAdmin):
	list_display = ("title", "course")

class LessonAdmin(admin.ModelAdmin):
	list_display = ("title", "module", "course")

class EnrolledAdmin(admin.ModelAdmin):
	list_display = ("user", "course", "date_enrolled")

class DoneLessonAdmin(admin.ModelAdmin):
	list_display = ("user", "lesson")

admin.site.register(User)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Enrolled, EnrolledAdmin),
admin.site.register(DoneLesson, DoneLessonAdmin)