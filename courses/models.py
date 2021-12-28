from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Course(models.Model):
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_author")
    imageUrl = models.CharField(max_length=500, blank=True, null=True)
    videoUrl = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class Module(models.Model):
    title = models.CharField(max_length=1000)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_module")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="module_author")

    def __str__(self):
        return f"{self.title}"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
        }


class Lesson(models.Model):
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=5000, blank=True)
    videoUrl = models.CharField(max_length=500, blank=True, null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="module_lesson")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_lesson")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lesson_author", default="1")

    def __str__(self):
        return f"{self.title}"
    

class Enrolled(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrolled_user")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrolled_course")
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user}, course: {self.course}"


class DoneLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="done_user")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="done_lesson")

    def __str__(self):
        return f"User: {self.user}, lesson: {self.lesson}"