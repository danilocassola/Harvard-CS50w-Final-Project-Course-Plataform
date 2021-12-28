from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("password", views.change_password, name="password"),
    path("course/<int:course_id>", views.course, name="course"),  
    path("lesson/<int:lesson_id>", views.lesson, name="lesson"),
    path("enroll", views.enroll, name="enroll"),
    path("mycourses", views.my_courses, name="mycourses"),
    path("done", views.done_lesson, name="done_lesson"),  
    path("cancel_enroll", views.cancel_enroll, name="cancel_enroll"),

    # API
    path("modules_api/<int:course_id>", views.modules_api, name="modules_api"),

    # Admin
    path("adm/courses", views.adm_courses, name="adm_courses"),
    path("adm/course/<int:course_id>", views.adm_course, name="adm_course"),
    path("adm/course/module/<int:module_id>", views.adm_module, name="adm_module"),
    path("adm/newcourse", views.new_course, name="newcourse"),
    path("adm/newmodule", views.new_module, name="newmodule"),
    path("adm/newlesson", views.new_lesson, name="newlesson"),
    path("adm/edit/course/<int:course_id>", views.edit_course, name="edit_course"),
    path("adm/edit/module/<int:module_id>", views.edit_module, name="edit_module"),
    path("adm/edit/lesson/<int:lesson_id>", views.edit_lesson, name="edit_lesson"),
    path("adm/del_course", views.del_course, name="del_course"),
    path("adm/del_module", views.del_module, name="del_module"),
    path("adm/del_lesson", views.del_lesson, name="del_lesson")
]