
from django.shortcuts import render, redirect
from .models import Slide, TestQuestion, TestResult
import random

# Widok strony g³ównej
def home(request):
    return render(request, 'main/home.html')

# Widok slajdów
def slides_view(request):
    slides = Slide.objects.all()
    return render(request, 'main/slides.html', {'slides': slides})

# Widok rozpoczêcia testu
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

# Widok zapisu odpowiedzi i przejœcia do nastêpnego pytania
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
