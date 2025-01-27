
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
