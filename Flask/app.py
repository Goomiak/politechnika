from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import random

app = Flask(__name__)

# Wczytanie konfiguracji aplikacji
def load_config():
    with open("json/config.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Wczytanie pytań testowych
def load_test_questions():
    with open("json/test.json", "r", encoding="utf-8") as f:
        return json.load(f)["questions"]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/slides/<module>')
def slides(module):
    config = load_config()
    slides = config.get("slides", {}).get(module, [])
    if not slides:
        return "Nie znaleziono slajdów dla tego modułu.", 404
    return render_template('slides.html', slides=slides, module=module)

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        # Obsługa odpowiedzi użytkownika
        answers = request.json
        questions = load_test_questions()
        score = 0

        for question, answer in answers.items():
            correct_answer = next(q for q in questions if q['question'] == question)['answer']
            if answer == correct_answer:
                score += 1

        return jsonify({"score": score, "total": len(questions)})

    # Losowanie pytań
    questions = random.sample(load_test_questions(), 10)
    return render_template('test.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import random
import os

app = Flask(__name__)

# Wczytanie konfiguracji aplikacji
def load_config():
    config_path = os.path.join("static", "json", "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Wczytanie pytań testowych
def load_test_questions():
    test_path = os.path.join("static", "json", "test.json")
    with open(test_path, "r", encoding="utf-8") as f:
        return json.load(f)["questions"]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/slides/<module>')
def slides(module):
    config = load_config()
    slides = config.get("slides", {}).get(module, [])
    if not slides:
        return "Nie znaleziono slajdów dla tego modułu.", 404
    return render_template('slides.html', slides=slides, module=module)

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        # Obsługa odpowiedzi użytkownika
        answers = request.json
        questions = load_test_questions()
        score = 0

        for question, answer in answers.items():
            correct_answer = next(q for q in questions if q['question'] == question)['answer']
            if answer == correct_answer:
                score += 1

        return jsonify({"score": score, "total": len(questions)})

    # Losowanie pytań
    questions = random.sample(load_test_questions(), 10)
    return render_template('test.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
