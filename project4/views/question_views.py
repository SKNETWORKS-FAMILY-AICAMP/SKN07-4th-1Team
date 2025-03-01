from django.shortcuts import render, redirect
from ..forms import QuestionForm
from ..models import Question


def question_view(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.save()
            return redirect('project4:index')
    else:
        form = QuestionForm()
    return render(request, 'project4/main.html', {'form': form})
