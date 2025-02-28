from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# from ..models import Question, Answer
from django.utils import timezone
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
# from ..forms import QuestionForm, AnswerForm

# 리스트
def index(request):
   
    return render(request, 'project4/index.html')

