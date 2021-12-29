# Harvard CS50w - Final Project: Course Platform
#### Video Demo:  <https://youtu.be/4E-WjSSlQPk>


This project is a Course Platform with YouTube videos buit with Python, JavaScript, HTML and CSS. Frameworks: Django and Bootstrap.



## Distinctiveness and Complexity

My project is a Course Plataform with YouTube videos. The student can register on the website, enroll to a course and track his progress by marking as done in each lesson, there is a bar showing the student progress.

Only the superuser can create a new course, module and lesson, as well as edit or delete. The superuser can use Django Admin or the interface that I built to do this tasks.

There are 6 models for this project.

JavaScript is used to mark each lesson as done and update the done icon for the lesson, module if all the lessons for the model are done and update the course progress dynamically, without refreshing the page. For this I created an API route, to get the modules.

Another JavaScript funcition is on the New Lesson page, when you choose what course you want to create a new lesson, the module dropdown is populate with course's modules.

This application is mobile-responsive built with bootstrap.



## Models

There are 6 models:

1. `User` - An extension of Django's `AbstractUser` model. Stores the e-mails and usernames. 

2. `Course` -  Stores title, description, author, URL image e URL video.

3. `Module` - Stores title, course and author.

4. `Lesson` - Stores title, description, URL video, module, course and  author.

5. `Enrolled` - Stores user, course and datetime.

6. `DoneLesson` - Stores the user and lesson.

   

## Routes

### Index `/`

This page show all the courses created.

### Login `/login`

The user can log in with username and password.

### Logout `/logout`

It will log the user out and redirect to the index page.

### Register `/register`

The user can register entering username, email address, password and confirm password. 

### Password `/password`

The user can change their password.

### Course `/course/<int:course_id>`

This is a course page where the user can enroll to this course. If the user already enrolled, the course progress will appear. 

### Lesson `/lesson/<int:lesson_id> `

This page is visible only to the enrolled users. The user can mark if the lesson is done.

### Enroll `/enroll`

This route only works with the POST method. It's to enroll the user to the course selected.

### My courses `/mycourses`

This page is only visible for logged users and displays the enrolled courses by the users.

### Done `/done`

This route only works with the PUT method. It's to mark the user lesson as done.

### Cancel enroll `/cancel_enroll`

This route only works with the POST method. It's to cancel the enroll.

### Module API `/modules_api/<int:course_id>`

This route is to get the course modules.

### Admin courses `/adm/courses`

This page is only visible for superusers. Display a list of the users courses.  It's possible to edit or delete a course, if the user click on the name of the course, another page is openned with its modules. There is a link to create a new course, new module and new lesson.

### Admin courses `/adm/course/<int:course_id>`

This page is only visible for superusers. Display a list of the modules course. It's possible to edit or delete a module, if the user click on the name of the module, another page is openned with its lessons. There is a link to create a new course, new module and new lesson.

### Admin courses `/adm/course/module/<int:module_id>`

This page is only visible for superusers. Display a list of the lessons module. It's possible to edit or delete a lesson. There is a link to create a new course, new module and new lesson.

### New course `/adm/newcourse`

This page is only visible for superusers. If the method is GET, a page with a form will be displayed, if the method is POST, it will be created a new course.

### New module `/adm/newmodule `

This page is only visible for superusers. If the method is GET, a page with a form will be displayed, if the method is POST, it will be created a new module.

### New lesson `/adm/newlesson`

This page is only visible for superusers. If the method is GET, a page with a form will be displayed, if the method is POST, it will be created a new lesson.

### Edit course `/adm/edit/course/<int:course_id>`

This page is only visible for superusers. If the method is GET, a page with a form with the course informations will be displayed, if the method is POST, the course will be updated.

### Edit module `/adm/edit/module/<int:module_id>`

This page is only visible for superusers. If the method is GET, a page with a form with the module informations will be displayed, if the method is POST, the module will be updated.

### Edit lesson `/adm/edit/lesson/<int:lesson_id>`

This page is only visible for superusers. If the method is GET, a page with a form with the lesson informations will be displayed, if the method is POST, the lesson will be updated.

### Delete course `/adm/del_course`

This route only works with the POST method and for superusers. it's for delete the selected course.

### Delete module `/adm/del_module`

This route only works with the POST method and for superusers. it's for delete the selected module.

### Delete lesson `/adm/del_lesson`

This route only works with the POST method and for superusers. it's for delete the selected lesson.

### Django admin `/admin`

This page is only visible for superusers. It's possible to create, edit or delete any information.



## Files and directories 

- `course` - main application directory.
  - `static/course` contains all static content.
    - `media` contains 'no course picture' image.
    - `style.css` CSS file.
    - `courses.js` - all JavaScript script used in the project.
  - `templates/courses` contains all application templates.
    - `adm` - templates for admin section.
      - `adm_course.html` - template for admin course page.
      - `adm_courses.html` - template for admin courses page.
      - `adm_module.html` - template for admin module page.
      - `edit_course.html` - template for admin edit course page.
      - `edit_lesson.html` - template for admin edit lesson page.
      - `edit_module.html` - template for admin edit module page.
      - `new_course.html` - template for admin new course page.
      - `new_lesson.html` - template for admin new lesson page.
      - `new_module.html` - template for admin new module page.
    - `course.html` - template for course page..
    - `error.html` - template for error page.
    - `index.html` - template for Index page.
    - `layout.html` - base template for all templates extend it.
    - `lesson.html` - template for lesson page.
    - `login.html` - template for login page.
    - `mycourses.html` - template for my courses page.
    - `password.html` - template for change password page.
    - `register.html` - template for register student page.
  - `__init__.py` - generated by Django.
  - `admin.py` - used to determine models which will be used in the Django Admin Interface.
  - `apps.py` - generated by Django.
  - `models.py` defines the models used to add to and update the database using Django.
  - `tests.py` - generated by Django.
  - `urls.py` - defines all application URLs.
  - `views.py` - contains all application views.
- `coursesplataform` - project directory
  - `__init__.py`  - generated by Django
  - `asgi.py` - generated by Django
  - `settings.py` - generated by Django.
  - `urls.py` - contains project URLs.
  - `wsgi.py` - generated by Django
- `db.sqlite3` - database
- `manage.py` - generated by Django.
- `README.md` - informations about the project.
- `requirements.txt` - packages required in order for the application to run successfully.



## How to run the application

### Running the application

1. Copy the files.

2. You need Python and Django installed on your system. If not you will need to install them.

4. To run the web server:

   ```python
   python manage.py runserver 
   ```

5. Visit the website in your browser. 

   - Log in as superuser:

     ```
     username: admin
     password: admin
     ```

   - Register a new student on the website.

     
     
     
