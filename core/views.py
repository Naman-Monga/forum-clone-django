from django.shortcuts import render, redirect
from . import models
from . import forms
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    questions = models.question.objects.all()
    questions = reversed(list(questions))
    form = forms.QuestionForm()
    if request.method == "POST":
        form = forms.QuestionForm(request.POST)
        if form.is_valid():
            categories = form.cleaned_data['categories']
            question = form.cleaned_data['text']
            quest = models.question(user = request.user,title = question)
            quest.save()
            quest.category.set(categories)
            quest.save()
            return redirect('home')
    context = {
        "questions":questions,
        'form':form,
    }
    return render(request, 'core/index.html', context)

def question_detail(request, pk):
    question = models.question.objects.filter(pk=pk)[0]
    answers = models.answer.objects.filter(question = question)
    myuser = models.UserProfile.objects.filter(user = request.user)[0]
    voted = myuser.check_q(question)
    voted_a = list()
    for a in answers:
        voted_a.append(myuser.check_a(a))
    answers = zip(answers, voted_a)
    context  = {
        'question':question,
        'answers':answers,
        'voted':voted,
    }

    if request.method == "POST":
        form = forms.SubmitAnswer(request.POST)
        if form.is_valid():
            answer_text = form.cleaned_data.get('text')
            answer_new = models.answer(question = question, text = answer_text, answerer = request.user)
            answer_new.save()
            return redirect(question)
        else:
            print('err!!!!')

    return render(request, 'core/question-detail.html', context)

def upvoter(request, pk):
    question = models.question.objects.filter(pk = pk)[0]
    myuser = models.UserProfile.objects.filter(user = request.user)[0]
    if not myuser.check_q(question):
        question.incrementUpvotes()
        myuser.ques_upvoted.add(question)       
    else:
        question.decrementUpvotes()        
        myuser.ques_upvoted.remove(question)
    myuser.save()
    question.save()
    return redirect(question.get_absolute_url())

def ansUpvoter(request, pk, pk2):
    answer = models.answer.objects.filter(pk = pk)[0]
    question = models.question.objects.filter(pk = pk2)[0]
    myuser = models.UserProfile.objects.filter(user = request.user)[0]
    if not myuser.check_a(answer):
        answer.incrementUpvotes()
        myuser.ans_upvoted.add(answer)       
    else:
        answer.decrementUpvotes()        
        myuser.ans_upvoted.remove(answer)
    myuser.save()
    answer.save()
    return redirect(question.get_absolute_url())