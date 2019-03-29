from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from web.models import Question, QuestionManager, Tag, Answer, CustomUser
from django.http import HttpResponse
from web.forms import UserForm, LoginForm, EditForm, AskForm, QuestForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    users = CustomUser.objects.top_5()
    tags = Tag.objects.popular()
    questions_list = Question.objects.new()
    questions = Paginator(questions_list, 3).get_page(request.GET.get("page"))
    context = {
        "auth" : request.user,
        "users": users,
        "tags": tags,
        "questions": questions,
    }
    return render(request, "web/home.html", context)

def hot(request):
    users = CustomUser.objects.top_5()
    tags = Tag.objects.popular()
    questions_list = Question.objects.best()
    questions = Paginator(questions_list, 3).get_page(request.GET.get("page"))
    context = {
        "auth" : request.user,
        "users": users,
        "tags": tags,
        "questions": questions,
    }
    return render(request, "web/hot.html", context)    

def question(request, quest_id):
    users = CustomUser.objects.top_5()
    tags = Tag.objects.popular()
    question = Question.objects.get_by_quest(quest_id)
    answers = Answer.objects.get_answers_to_quest(question)
    if request.method == "POST":
        form = QuestForm(request.POST)
        form.quest_user = CustomUser.objects.get_profile(request.user)
        form.question_answ = question
        if form.is_valid():
            user = form.save()
            return redirect("question_id", quest_id)
    else:
        form = QuestForm()
    context = {
        "auth" : request.user,
        "form": form,
        "users": users,
        "tags": tags,
        "question": question,
        "answers": answers,
    }
    return render(request, "web/quest.html", context)
    
def question_tag(request, tag_name):
    users = CustomUser.objects.top_5()
    tags = Tag.objects.popular()
    questions_list = Question.objects.get_by_tag(tag_name)
    questions = Paginator(questions_list, 3).get_page(request.GET.get("page"))
    context = {
        "auth" : request.user,
        "users": users,
        "tag_name": tag_name,
        "tags": tags,
        "questions": questions,
    }
    return render(request, "web/tag.html", context)

@login_required(login_url='/login/')
def ask(request):
    users = CustomUser.objects.top_5()
    tags = Tag.objects.popular()
    if request.method == "POST":
        form = AskForm(request.POST)
        form.custom_user = CustomUser.objects.get_profile(request.user)
        if form.is_valid():
            user = form.save()
            return redirect("home")
    else:
        form = AskForm()
    context = {
        "auth" : request.user,
        "form": form,
        "users": users,
        "tags": tags,
    }
    return render(request, "web/ask.html", context)

def profile(request, profile_name):
    users = CustomUser.objects.top_5()
    tags = Tag.objects.popular()
    profile = CustomUser.objects.get_by_name(profile_name)
    questions = Question.objects.filter(author__user__username=profile_name)
    asked = questions.count()
    ranking = CustomUser.objects.get_ranking(profile_name)
    context = {
        "auth" : request.user,
        "users": users,
        "profile": profile,
        "tags": tags,
        "asked": asked,
        "ranking": ranking,
    }
    return render(request, "web/profile.html", context)

@login_required
def profile_edit(request):
    users = CustomUser.objects.top_5()
    tags = Tag.objects.popular()
    profile = CustomUser.objects.get_profile(request.user)
    if request.method == "POST":
        form = EditForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(profile)
            return redirect("profile_name", profile.user.username)
    else:
        form = EditForm.load(profile)
    context = {
        "auth" : request.user,
        "form": form,
        "users": users,
        "tags": tags,
    }
    return render(request, "web/profile_edit.html", context)

def register(request):
    users = CustomUser.objects.top_5()
    tags = Tag.objects.popular()
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect("home")
    else:
        form = UserForm()
    context = {
        "auth" : request.user,
        "form": form,
        "users": users,
        "tags": tags,
    }
    return render(request, "web/register.html", context)

def login(request):
    users = CustomUser.objects.top_5()
    tags = Tag.objects.popular()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
    else:
        form = LoginForm()
    context = {
        "auth" : request.user,
        "form": form,
        "users": users,
        "tags": tags,
    }
    return render(request, "web/login.html", context)

def logout(request):
    auth_logout(request)
    return redirect(request.GET.get('now','/'))

@login_required(login_url='/login/')
def up(request, quest_id):
    user = Question.objects.filter(id=quest_id)[0]
    user.rathing +=1
    user.save()
    return redirect(request.GET.get('now','/'))

@login_required(login_url='/login/')
def down(request, quest_id):
    user = Question.objects.filter(id=quest_id)[0]
    user.rathing -=1
    user.save()
    return redirect(request.GET.get('now','/'))
