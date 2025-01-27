import os

# Tworzenie projektu Django i aplikacji
os.system("django-admin startproject educational_app")
os.chdir("educational_app")
os.system("python manage.py startapp main")

# Konfiguracja pliku settings.py dla aplikacji 'main'
settings_path = "educational_app/settings.py"
with open(settings_path, "a") as settings_file:
    settings_file.write("\nINSTALLED_APPS += ['main']\n")

print("Projekt Django i aplikacja main zostały utworzone.")

# Implementacja modeli w aplikacji main
models_code = """
from django.db import models

class Slide(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slide_type = models.CharField(max_length=50, choices=[('text', 'Text'), ('image', 'Image'), ('math', 'Math'), ('simulation', 'Simulation')])
    image_path = models.CharField(max_length=255, blank=True, null=True)

class TestQuestion(models.Model):
    question = models.TextField()
    image_path = models.CharField(max_length=255, blank=True, null=True)
    options = models.JSONField()
    correct_answer = models.CharField(max_length=10)

class TestResult(models.Model):
    student_name = models.CharField(max_length=255)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
"""

with open("main/models.py", "w") as models_file:
    models_file.write(models_code)

print("Modele zostały dodane do aplikacji main.")

# Implementacja widoków
views_code = """
from django.shortcuts import render, redirect
from .models import Slide, TestQuestion, TestResult
import random

# Widok strony głównej
def home(request):
    return render(request, 'main/home.html')

# Widok slajdów
def slides_view(request):
    slides = Slide.objects.all()
    return render(request, 'main/slides.html', {'slides': slides})

# Widok rozpoczęcia testu
def start_test(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        questions = list(TestQuestion.objects.all().order_by('?')[:10])
        request.session['questions'] = [
            {'id': q.id, 'question': q.question, 'options': q.options, 'image_path': q.image_path} for q in questions
        ]
        request.session['score'] = 0
        request.session['current_question'] = 0
        request.session['student_name'] = student_name
        return redirect('test_question')
    return render(request, 'main/start_test.html')

# Widok pytania testowego
def test_question(request):
    current_question = request.session.get('current_question', 0)
    questions = request.session.get('questions', [])

    if current_question >= len(questions):
        return redirect('test_result')

    question = questions[current_question]
    return render(request, 'main/test_question.html', {'question': question})

# Widok zapisu odpowiedzi i przejścia do następnego pytania
def submit_answer(request):
    if request.method == 'POST':
        selected_option = request.POST.get('option')
        current_question = request.session.get('current_question', 0)
        questions = request.session.get('questions', [])
        score = request.session.get('score', 0)

        correct_answer = TestQuestion.objects.get(id=questions[current_question]['id']).correct_answer
        if selected_option == correct_answer:
            score += 1
        
        request.session['score'] = score
        request.session['current_question'] = current_question + 1
        return redirect('test_question')

# Widok wyniku testu
def test_result(request):
    score = request.session.get('score', 0)
    student_name = request.session.get('student_name', 'Unknown')

    TestResult.objects.create(student_name=student_name, score=score)
    return render(request, 'main/test_result.html', {'score': score, 'student_name': student_name})
"""

with open("main/views.py", "w") as views_file:
    views_file.write(views_code)

print("Widoki zostały zaimplementowane.")

# Implementacja routingu
urls_code = """
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('slides/', views.slides_view, name='slides_view'),
    path('test/start/', views.start_test, name='start_test'),
    path('test/question/', views.test_question, name='test_question'),
    path('test/submit/', views.submit_answer, name='submit_answer'),
    path('test/result/', views.test_result, name='test_result'),
]
"""

with open("educational_app/urls.py", "w") as urls_file:
    urls_file.write(urls_code)

print("Routing został zaimplementowany.")

# Dodanie stylizowanych szablonów HTML
os.makedirs("templates/main", exist_ok=True)

home_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Strona główna</title>
    <link rel='stylesheet' href='/static/style.css'>
</head>
<body>
    <h1>Witamy w aplikacji dydaktycznej</h1>
    <nav>
        <a href="/slides/">Przeglądaj slajdy</a> |
        <a href="/test/start/">Rozpocznij test</a>
    </nav>
</body>
</html>
"""

slides_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Slajdy</title>
    <link rel='stylesheet' href='/static/style.css'>
</head>
<body>
    <h1>Slajdy</h1>
    <ul>
        {% for slide in slides %}
        <li>{{ slide.title }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

start_test_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Rozpocznij test</title>
    <link rel='stylesheet' href='/static/style.css'>
</head>
<body>
    <h1>Rozpocznij test</h1>
    <form method="post">
        {% csrf_token %}
        <label for="student_name">Podaj swoje imię i nazwisko:</label>
        <input type="text" name="student_name" id="student_name" required>
        <button type="submit">Rozpocznij</button>
    </form>
</body>
</html>
"""

test_question_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Pytanie testowe</title>
    <link rel='stylesheet' href='/static/style.css'>
</head>
<body>
    <h1>Pytanie testowe</h1>
    <p>{{ question.question }}</p>
    <form method="post" action="/test/submit/">
        {% csrf_token %}
        {% for key, option in question.options.items %}
        <label>
            <input type="radio" name="option" value="{{ key }}" required> {{ option }}
        </label><br>
        {% endfor %}
        <button type="submit">Zatwierdź odpowiedź</button>
    </form>
</body>
</html>
"""

test_result_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Wynik testu</title>
    <link rel='stylesheet' href='/static/style.css'>
</head>
<body>
    <h1>Twój wynik</h1>
    <p>Imię i nazwisko: {{ student_name }}</p>
    <p>Wynik: {{ score }}</p>
    <a href="/">Powrót do strony głównej</a>
</body>
</html>
"""

with open("templates/main/home.html", "w") as file:
    file.write(home_html)

with open("templates/main/slides.html", "w") as file:
    file.write(slides_html)

with open("templates/main/start_test.html", "w") as file:
    file.write(start_test_html)

with open("templates/main/test_question.html", "w") as file:
    file.write(test_question_html)

with open("templates/main/test_result.html", "w") as file:
    file.write(test_result_html)

print("Szablony HTML zostały dodane.")

# Dodanie pliku stylów CSS
os.makedirs("static", exist_ok=True)
css_code = """
body {
    font-family: Arial, sans-serif;
    margin: 20px;
    padding: 20px;
    background-color: #f4f4f9;
}

h1 {
    color: #333;
}

nav a {
    margin: 0 10px;
    text-decoration: none;
    color: #007bff;
}

nav a:hover {
    text-decoration: underline;
}

form {
    margin-top: 20px;
}

button {
    background-color: #007bff;
    color: #fff;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}
"""

with open("static/style.css", "w") as css_file:
    css_file.write(css_code)

print("Stylizacja CSS została dodana.")