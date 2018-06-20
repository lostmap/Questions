from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.shortcuts import get_object_or_404
from django.db import models
 
"""
class UserManager(AbstractUserManager):
    def top_5(self):
        return self.all().order_by('-ranking')[:5]


class User(AbstractUser):
    objects = UserManager()
    upload = models.ImageField(upload_to="media", null=True, blank=True)
    ranking = models.IntegerField(default=0)

    class Meta:
        ordering = ['-ranking']
"""
class CustomUserManager(models.Manager):
    def top_5(self):
        return self.all().order_by('-ranking')[:5]

    def dublicate_entry(self, username):
        dublicate = True
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            dublicate = False
        return dublicate
    def get_profile(self, user):
        if not user.is_authenticated:
            return None
        return self.get(user=user)    

    def get_by_name(self, profile_name):
        return get_object_or_404(User, username=profile_name)

class CustomUser(models.Model):
    objects = CustomUserManager()
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    upload = models.ImageField(upload_to="media", null=True, blank=True, default="media/empty.gif")
    ranking = models.IntegerField(default=0)

    class Meta:
        ordering = ['-ranking']

    def __str__(self):
        return self.user.username

class TagManager(models.Manager):
    def popular(self):
        return self.filter(count__gt=0).order_by('-count')[:5]

class Tag(models.Model):
    objects = TagManager()
    name = models.CharField(unique=True, max_length=120)
    is_active = models.BooleanField(default=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
        
class QuestionManager(models.Manager):
    def new(self):
        return self.all().order_by('-date')

    def best(self):
        return self.all().order_by('-rathing', '-date')

    def get_by_quest(self, quest_id):
        return get_object_or_404(Question, id=quest_id)

    def get_by_tag(self, tag_name):
        tag = get_object_or_404(Tag, name=tag_name)
        return tag.question_set.all()

    def add_tag(self, question, tag_name):
        try:
            tag = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            tag = Tag(name=tag_name)
            tag.save()
        tag.count += 1;
        tag.save()
        question.tags.add(tag)
        question.save()
        return question

class Question(models.Model):
    objects = QuestionManager()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    tags = models.ManyToManyField(Tag, blank=True)
    rathing = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def answers_count(self):
        return self.answer_set.count()

class AnswerManager(models.Manager):
    def get_answers_to_quest(self, question):
        return question.answer_set.all()

class Answer(models.Model):
    objects = AnswerManager()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    is_active = models.BooleanField(default=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['date']
