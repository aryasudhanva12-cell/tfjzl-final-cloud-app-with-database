from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    pub_date = models.DateField(null=True)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Learner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    grade = models.IntegerField(default=5)

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        if all_answers == selected_correct and len(selected_ids) == all_answers:
            return True
        return False

    def __str__(self):
        return f"Question: {self.content}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice: {self.content}"

class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    time_submitted = models.DateTimeField(default=now)

    def __str__(self):
        return f"Submission by {self.enrollment.user.username} for {self.enrollment.course.name}"