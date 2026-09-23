from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Course, Question, Choice, Submission, Enrollment, Learner

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail.html'

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # Retrieve an existing enrollment or create a new one automatically
        enrollment = Enrollment.objects.filter(course=course).first()
        if not enrollment:
            learner = Learner.objects.first()
            if learner:
                enrollment = Enrollment.objects.create(user=learner.user, course=course)

        submission = Submission.objects.create(enrollment=enrollment)
        
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                choice = get_object_or_404(Choice, pk=int(value))
                submission.choices.add(choice)
        submission.save()
        
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    selected_choices = submission.choices.all()
    for choice in selected_choices:
        if choice.is_correct:
            total_score += 10
    
    context['course'] = course
    context['selected_ids'] = [choice.id for choice in selected_choices]
    context['grade'] = total_score
    return render(request, 'onlinecourse/exam_result.html', context)