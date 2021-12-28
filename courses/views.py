from django.core.checks import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import json
import re

from .models import User, Course, Module, Lesson, Enrolled, DoneLesson

def embed_url(video_url):
        regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"

        return re.sub(regex, r"https://www.youtube.com/embed/\1",video_url)

def index(request):
    courses = Course.objects.all()

    return render(request, "courses/index.html", {
        "courses": courses
    })


def course(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return render(request, "courses/error.html", {
        "message": "ERROR 404: Page does not exist!"
    })

    # Get the course modules
    modules = Module.objects.filter(course=course_id)

    # Get the course lessons
    lessons = Lesson.objects.filter(course=course_id)

    if course.videoUrl == "":
        course.videoUrl = None

    # Change url's video to embed url
    if course.videoUrl != None:
        course.videoUrl = embed_url(course.videoUrl)


    for lesson in lessons:
            try:
                lesson.videoUrl = embed_url(lesson.videoUrl)
            except:
                lesson.videoUrl = None

    # Set the default values
    enrolled = False
    progress = "0"
    btn_innerHtml = "Enroll"
    btn_disabled = "btn-danger"

    if request.user.is_authenticated: 

        # Check if the user is enrolled
        try:
            enroll = Enrolled.objects.get(course=course_id, user=request.user)
            enrolled = True
            btn_innerHtml = "Enrolled"
            btn_disabled = "btn-success disabled"
        except Enrolled.DoesNotExist:
            enrolled = False
            btn_innerHtml = "Enroll"
            btn_disabled = "btn-danger"

        # Get the course progress
        progress = progress_course(request.user, course.id)    

        # Get the done lessons by the user
        done_lessons = DoneLesson.objects.filter(lesson__in=lessons, user=request.user)

        # Check if the all lessons are done for the menu
        for l in lessons:
            if [done_lesson for done_lesson in done_lessons if done_lesson.lesson == l]:
                l.done = True
            else:
                l.done = False

        # Check if the module is done by the user and add to its module
        for module in modules:
            done_mod = done_module(request.user, module.id)
            module.done = done_mod

    # Add lessons to its module
    for module in modules:
        filtered_lessons = [lesson for lesson in lessons if lesson.module == module]
        module.lessons = filtered_lessons

    # Add modules to its course
    course.modules = modules
    
    return render(request, "courses/course.html", {
        "course": course,        
        "enrolled": enrolled,
        "progress": progress,
        "btn_innerHtml": btn_innerHtml,
        "btn_disabled": btn_disabled

    })
    

def modules_api(request, course_id):
    try:
        courses = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return JsonResponse({"error": "Invalid path."}, status=400)

    modules = Module.objects.filter(course=course_id)

    # Return modules in chronologial order
    modules = modules.order_by("title").all()

    return JsonResponse([module.serialize() for module in modules], safe=False)


@login_required(login_url='/login')
def lesson(request, lesson_id):
    try:
        lesson = Lesson.objects.get(pk=lesson_id)
    except Lesson.DoesNotExist:
        return render(request, "courses/error.html", {
        "message": "ERROR 404: Page does not exist!"
    })
    
    # if the user is not enrolled, the user is routed to the course page
    try:
        enroll = Enrolled.objects.get(course=lesson.course, user=request.user)
    except Enrolled.DoesNotExist:
        return HttpResponseRedirect(reverse("course", args=(lesson.course.id,)))

    if lesson.videoUrl == "":
        lesson.videoUrl = None

    # Change url's video to embed url
    try:
        lesson.videoUrl = embed_url(lesson.videoUrl)
    except:
        lesson.videoUrl = None

    # Get the modules
    modules = Module.objects.filter(course=lesson.course)

    # Get the course's lessons
    lessons = Lesson.objects.filter(course=lesson.course)

    # Get the done lessons by the user
    done_lessons = DoneLesson.objects.filter(lesson__in=lessons, user=request.user)

    # Check if the lesson is done for the lesson page
    if [done_lesson for done_lesson in done_lessons if done_lesson.lesson == lesson]:
        lesson.done = True
    else:
        lesson.done = False
   
    # Check if the all lessons are done for the menu
    for l in lessons:
        if [done_lesson for done_lesson in done_lessons if done_lesson.lesson == l]:
            l.done = True
        else:
            l.done = False
                     
    # Add lessons to its module
    for module in modules:
        filtered_lessons = [lesson for lesson in lessons if lesson.module == module]
        module.lessons = filtered_lessons

    # Get the course progress
    progress = progress_course(request.user, lesson.course.id)

    # Check if the module is done by the user and add to its module
    for module in modules:
        done_mod = done_module(request.user, module.id)
        module.done = done_mod

    return render(request, "courses/lesson.html", {
        "lesson": lesson,
        "modules": modules,
        "progress": progress,
        "done_lessons": done_lessons
    })


@login_required
def enroll(request):
    if request.method == "POST":
        user = request.user
        course_id = request.POST["course_id"]

        course = Course.objects.get(pk=course_id)

        # if the user is not enrolled, the user is routed to the course page
        try:
            enroll = Enrolled.objects.get(course=course, user=user)
            return HttpResponseRedirect(reverse("course", args=(course_id,)))
        except Enrolled.DoesNotExist:
            enroll = Enrolled(user=user, course=course)
            enroll.save()
            return HttpResponseRedirect(reverse("course", args=(course_id,)))
    

@login_required
def cancel_enroll(request):
    if request.method == "POST":
        user = request.user
        course_id = request.POST["course_id"]

        course = Course.objects.get(pk=course_id)
        
        # if the user is not enrolled, the user is routed to the course page
        try:
            enroll = Enrolled.objects.get(course=course, user=user)
            enroll.delete()
            return HttpResponseRedirect(reverse("course", args=(course_id,)))
        except Enrolled.DoesNotExist:
            return HttpResponseRedirect(reverse("course", args=(course_id,)))
    

@login_required(login_url='/login')
def my_courses(request):
    try:
        enrolls = Enrolled.objects.filter(user=request.user)       
    except Enrolled.DoesNotExist:
        message = "You don't have courses"

    courses = []
    for enroll in enrolls:
        courses.append(Course.objects.get(pk=enroll.course.id))

    return render(request, "courses/mycourses.html", {
        "courses": courses
    })


@login_required
def done_lesson(request):
    if request.method == "PUT":
        user = request.user
        data = json.loads(request.body)
        lesson_id = data.get("lesson", "")
        lesson = Lesson.objects.get(pk=lesson_id)
              
        try:
            # if the lesson user is done, the lesson is delete
            done_lesson = DoneLesson.objects.get(lesson=lesson, user=user)
            done_lesson.delete()
            done_mod = done_module(user, lesson.module.id)
            progress = progress_course(user, lesson.course.id)
            return JsonResponse({ 
                "lesson_done": "False", 
                "done_module": done_mod, 
                "module_id": lesson.module.id,
                "progress_course": progress
                }, status=200)
        except DoneLesson.DoesNotExist:
            # if its not, the lesson is registered as done
            done_lesson = DoneLesson(user=user, lesson=lesson)
            done_lesson.save()
            done_mod = done_module(user, lesson.module.id)
            progress = progress_course(user, lesson.course.id)
            return JsonResponse({ 
                "lesson_done": "True", 
                "done_module": done_mod, 
                "module_id": lesson.module.id,
                "progress_course": progress
                }, status=200)    
        
    # It must be via PUT
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)


def done_module(user, module_id):

    # Get the module
    module = Module.objects.get(pk=module_id)
    
    # Get the module's lessons
    lessons = Lesson.objects.filter(module=module)

    # Get the done lessons by the user
    done_lessons = DoneLesson.objects.filter(lesson__in=lessons, user=user)

    # Check if the module is done by the user
    if len(lessons) == len(done_lessons) and len(lessons) > 0:
        done_module = True
    else:
        done_module = False
    
    return done_module


def progress_course(user, course_id):

    # Get the course
    course = Course.objects.get(pk=course_id)

    # Get the course's lessons
    lessons = Lesson.objects.filter(course=course)

    # Get the done lessons by the user
    done_lessons = DoneLesson.objects.filter(lesson__in=lessons, user=user)

    # Get the course progress
    try:
        total_lessons = len(lessons)
        total_done_lessons = len(done_lessons)
        progress = round((total_done_lessons/total_lessons)*100)
    except:
        progress = "0"

    return progress


@login_required
def adm_courses(request):

    # Make sure only superuser is allow to access this page
    if request.user.is_superuser == False:
        return render(request, "courses/error.html", {
        "message": "You don't have permission to access this page."
    })

    courses = Course.objects.filter(author=request.user)

    return render(request, "courses/adm/adm_courses.html", {
        "courses": courses
    })


@login_required
def adm_course(request, course_id):

    # Make sure only superuser is allow to access this page
    if request.user.is_superuser == False:
        return render(request, "courses/error.html", {
        "message": "You don't have permission to access this page."
    })

    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return render(request, "courses/error.html", {
        "message": "ERROR 404: Page does not exist!"
    })

    # Get the course modules
    modules = Module.objects.filter(course=course_id)

    return render(request, "courses/adm/adm_course.html", {
        "course": course,
        "modules": modules
    })


@login_required
def adm_module(request, module_id):

    # Make sure only superuser is allow to access this page
    if request.user.is_superuser == False:
        return render(request, "courses/error.html", {
        "message": "You don't have permission to access this page."
    })

    # Get the module
    try:
        module =  Module.objects.get(pk=module_id)
    except Module.DoesNotExist:
        return render(request, "courses/error.html", {
        "message": "ERROR 404: Page does not exist!"
    })

    # Get the lessons' module
    lessons = Lesson.objects.filter(module=module)

    return render(request, "courses/adm/adm_module.html", {
        "module": module,
        "lessons": lessons
    })


@login_required
def new_course(request):

    # Make sure only superuser is allow to access this page
    if request.user.is_superuser == False:
        return render(request, "courses/error.html", {
        "message": "You don't have permission to access this page."
    })

    if request.method == "POST":
        title = (request.POST["title"])
        description = (request.POST["description"])
        imageUrl = (request.POST["imageUrl"])
        videoUrl = (request.POST["videoUrl"])
        author = request.user

        courses = Course(title=title, description=description, imageUrl=imageUrl,  videoUrl=videoUrl, author=author)
        courses.save()
        return HttpResponseRedirect(reverse("adm_courses"))

    return render(request, "courses/adm/new_course.html")


@login_required
def new_module(request):

    # Make sure only superuser is allow to access this page
    if request.user.is_superuser == False:
        return render(request, "courses/error.html", {
        "message": "You don't have permission to access this page."
    })
    
    if request.method == "POST":
        title = (request.POST["title"])
        course = Course.objects.get(pk=int(request.POST["course"]))
        author = request.user

        # Create the new module
        module = Module(title=title, course=course,author=author)
        module.save()

        return HttpResponseRedirect(reverse("adm_course", args=(course.id,)))

    courses = Course.objects.all()

    return render(request, "courses/adm/new_module.html", {
        "courses": courses
    })


@login_required
def new_lesson(request):
    
    # Make sure only superuser is allow to access this page
    if request.user.is_superuser == False:
        return render(request, "courses/error.html", {
        "message": "You don't have permission to access this page."
    })

    if request.method == "POST":
        title = (request.POST["title"])
        description = (request.POST["description"])
        videoUrl = (request.POST["videoUrl"])
        author = request.user
        course = Course.objects.get(pk=int(request.POST["course"]))
        module = Module.objects.get(pk=int(request.POST["module"]))
        author = request.user

        # Create the new lesson
        lesson = Lesson(title=title, description=description, videoUrl=videoUrl, author=author, course=course, module=module)
        lesson.save()

        return HttpResponseRedirect(reverse("adm_module", args=(module.id,)))

    courses = Course.objects.all()
    return render(request, "courses/adm/new_lesson.html", {
        "courses": courses
    })


@login_required
def edit_course(request, course_id):
    # Make sure only superuser is allow to access this page
    if request.user.is_superuser == False:
        return render(request, "courses/error.html", {
        "message": "You don't have permission to access this page."
    })

    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return render(request, "courses/error.html", {
        "message": "ERROR 404: Page does not exist!"
    })

    if request.method == "POST":
        title = (request.POST["title"])
        description = (request.POST["description"])
        imageUrl = (request.POST["imageUrl"])
        videoUrl = (request.POST["videoUrl"])

        # Save the course changes
        course.title = title
        course.description = description
        course.imageUrl = imageUrl
        course.videoUrl = videoUrl
        course.save()
     
        return HttpResponseRedirect(reverse("adm_courses"))

    return render(request, "courses/adm/edit_course.html", {
        "course": course
    })

@login_required
def edit_module(request, module_id):

    # Make sure only superuser is allow to access this page
    if request.user.is_superuser == False:
        return render(request, "courses/error.html", {
        "message": "You don't have permission to access this page."
    })

    # Get the module
    try:
        module =  Module.objects.get(pk=module_id)
    except Module.DoesNotExist:
        return render(request, "courses/error.html", {
        "message": "ERROR 404: Page does not exist!"
    })

    if request.method == "POST":
        title = (request.POST["title"])
        course = Course.objects.get(pk=int(request.POST["course"]))

        # Save the module changes
        module.title = title
        module.course = course
        module.save()
     
        return HttpResponseRedirect(reverse("adm_course", args=(course.id,)))

    courses = Course.objects.all()

    return render(request, "courses/adm/edit_module.html", {
        "courses": courses,
        "module": module
    })


@login_required
def edit_lesson(request, lesson_id):
    # Make sure only superuser is allow to access this page
    if request.user.is_superuser == False:
        return render(request, "courses/error.html", {
        "message": "You don't have permission to access this page."
    })

    # Get the module
    try:
        lesson = Lesson.objects.get(pk=lesson_id)
    except Lesson.DoesNotExist:
        return render(request, "courses/error.html", {
        "message": "ERROR 404: Page does not exist!"
    })

    if request.method == "POST":
        title = (request.POST["title"])
        description = (request.POST["description"])
        course = Course.objects.get(pk=int(request.POST["course"]))
        module = Module.objects.get(pk=int(request.POST["module"]))
        videoUrl = (request.POST["videoUrl"])

        # Save the course changes
        lesson.title = title
        lesson.description = description
        lesson.course = course
        lesson.module = module
        lesson.videoUrl = videoUrl
        lesson.save()

        return HttpResponseRedirect(reverse("adm_module", args=(lesson.module.id,)))

    courses = Course.objects.all()
    modules = Module.objects.filter(course=lesson.course)

    return render(request, "courses/adm/edit_lesson.html", {
        "courses": courses,
        "modules": modules,
        "lesson": lesson
    })


@login_required
def del_course(request):
     # Make sure only superuser is allow to access this route
    if request.user.is_superuser == False:
        return render(request, "courses/error.html", {
        "message": "You don't have permission to access this page."
    })

    if request.method == "POST":
        course = Course.objects.get(pk=int(request.POST["course_id"]))
        course.delete()

        return HttpResponseRedirect(reverse("adm_courses"))


@login_required
def del_module(request):
     # Make sure only superuser is allow to access this route
    if request.user.is_superuser == False:
        return render(request, "courses/error.html", {
        "message": "You don't have permission to access this page."
    })

    if request.method == "POST":
        module = Module.objects.get(pk=int(request.POST["module_id"]))
        course_id = module.course.id
        module.delete()

        return HttpResponseRedirect(reverse("adm_course", args=(course_id,)))


@login_required
def del_lesson(request):
     # Make sure only superuser is allow to access this route
    if request.user.is_superuser == False:
        return render(request, "courses/error.html", {
        "message": "You don't have permission to access this page."
    })

    if request.method == "POST":
        lesson = Lesson.objects.get(pk=int(request.POST["lesson_id"]))
        module_id = lesson.module.id
        lesson.delete()

        return HttpResponseRedirect(reverse("adm_module", args=(module_id,)))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "courses/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "courses/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "courses/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "courses/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "courses/register.html")


@login_required
def change_password(request):
    if request.method == "POST":

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "courses/password.html", {
                "message": "Passwords must match.",
                "alert": "danger"
            })

        # change the password
        user = User.objects.get(pk=request.user.id)
        user.set_password(password)
        user.save()
        login(request, user)
        return render(request, "courses/password.html", {
            "message": "Password changed.",
                "alert": "success"
        })
    
    return render(request, "courses/password.html")