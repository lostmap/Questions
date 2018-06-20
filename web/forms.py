from django.forms import ModelForm
from django import forms
from web.models import Question, QuestionManager, Tag, Answer, CustomUser, User
from django.core.exceptions import ValidationError
from django.contrib.auth import login as auth_login, authenticate
from re import sub 
import re
"""
class PrettyForm(forms.Form):
    error_css_class = 'is-invalid'
    #required_css_class = 'form-control' 

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        # adding css classes to widgets without define the fields:
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def as_pretty(self):
        return self._html_output(
            normal_row='<div class="form-group">%(label)s%(html_class_attr)s%(field)s%(help_text)s</div>',
            error_row ='%s',
            row_ender ='',
            help_text_html=' <small class="form-text text-muted">%s</small>',
            errors_on_separate_row=False)
"""
 
class QuestForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea,
                            help_text='Question body', label='Text',
                            label_suffix='', required=True)

    def save(self):
        answer = Answer(text=self.cleaned_data['text'],
                            question=self.question_answ,
                            author=self.quest_user,                
                            )
        answer.save()
        return answer

    def clean(self):
        cleaned_data = super(QuestForm, self).clean()
        text = cleaned_data.get('text')
    
        if not text:
            raise ValidationError('You have to write something!') 



class AskForm(forms.Form):
    title = forms.CharField(max_length=120, help_text='Topic',
                            label='Title', required=True)
    text = forms.CharField(widget=forms.Textarea,
                            help_text='Question body', label='Text', required=True)
    tags = forms.CharField(max_length=255, help_text='For instance: lost,big,Deuce',
                            label='Tags', required=False)

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        regexp = r'^[\w,]+$'
        if not re.match(regexp, tags):
            raise ValidationError("Incorrect symbols")
        return tags

    def save(self):
        question = Question(title=self.cleaned_data['title'],
                            text=self.cleaned_data['text'],
                            author=self.custom_user,
                            )
        question.save()

        tags = self.cleaned_data["tags"]
        
        for tag in tags.split(","):
            if tag is not None:
                Question.objects.add_tag(question=question, tag_name=tag)

        return question

    def clean(self):
        cleaned_data = super(AskForm, self).clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
    
        if not title and not text:
            raise ValidationError('You have to write something!') 


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", label_suffix='', 
                                max_length=35, widget=forms.TextInput, required=True)

    password = forms.CharField(label="Password", label_suffix='',
                                min_length=8, max_length=32,
                                widget=forms.PasswordInput, required=True)
    
    def save(self):
        return self.user

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            raise ValidationError('Incorrect username or password.')
        self.user = user 

class EditForm(forms.Form):
    first_name = forms.CharField(label="First name", label_suffix='', 
                                max_length=30, widget=forms.TextInput,
                                required=False)
    last_name = forms.CharField(label="Last name", label_suffix='', 
                                max_length=150, widget=forms.TextInput,
                                required=False)

    email = forms.EmailField(label="Email", label_suffix='',
                            widget=forms.EmailInput, required=True)

    upload = forms.ImageField(label="upload", widget=forms.FileInput, required=True)

    @staticmethod
    def load(profile):
        form = EditForm({
                        'first_name': profile.user.first_name,
                        'last_name' : profile.user.last_name,
                        'email' : profile.user.email,
                        'upload' : profile.upload,
                        'user': profile.user,
            })
        return form

    def clean_upload(self):
        upload = self.cleaned_data['upload']
        if not upload:
            raise ValidationError("Avatar is not loaded")
        return upload

    def save(self, profile):
        
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        profile.user.email = self.cleaned_data['email']

        profile.user.save()

        if self.cleaned_data['upload'] is not None:
            profile.upload = self.cleaned_data['upload']
        

        profile.save()

    def clean(self):
        cleaned_data = super(EditForm, self).clean()
        email = cleaned_data.get('email')
        upload = cleaned_data.get('upload')

        if not upload and not email:
            raise ValidationError('You have to write something!') 



class UserForm(forms.Form):
    username = forms.CharField(label="Username", label_suffix='', 
                                help_text= "Only English letters, "
                                "numbers, and @/./+/-/_", max_length=35,
                                widget=forms.TextInput(attrs={
                                'placeholder':'Pick a username',
                                }), required=True)

    email = forms.EmailField(label="Email", label_suffix='',
                            help_text="Enter your active email",
                            widget=forms.EmailInput(attrs={
                            'placeholder':'you@example.com',
                            }), required=True)

    password = forms.CharField(label="Password", label_suffix='',
                                help_text="Write password from 8 to 32",
                                min_length=8, max_length=32,
                                widget=forms.PasswordInput, required=True)

    password_repeat = forms.CharField(label="Confirm Password", label_suffix='',
                                help_text="Repeat your password",
                                min_length=8, max_length=32,
                                widget=forms.PasswordInput, required=True)

    first_name = forms.CharField(label="First name", label_suffix='', 
                                help_text= "Enter your first name", max_length=30,
                                widget=forms.TextInput(attrs={
                                'placeholder':'Billy',
                                }), required=False)
    last_name = forms.CharField(label="Last name", label_suffix='', 
                                help_text= "Enter your last name", max_length=150,
                                widget=forms.TextInput(attrs={
                                'placeholder':'Herrington',
                                }), required=False)

    upload = forms.ImageField(label="upload", help_text="Upload your profile picture",
                                widget=forms.FileInput, required=True)

    
    def clean_username(self):
        username = self.cleaned_data['username']
        regexp = r'^[\w.@+-]+$'
        if not re.match(regexp, username):
            raise ValidationError("Incorrect symbols")
        return username

    def clean_upload(self):
        upload = self.cleaned_data['upload']
        if not upload:
            raise ValidationError("Avatar is not loaded")
        return upload

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password'],
                                        first_name=self.cleaned_data['first_name'],
                                        last_name=self.cleaned_data['last_name'])
        custom_user = CustomUser(user=user, upload = self.cleaned_data['upload'])
        custom_user.save()
        return custom_user

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        upload = cleaned_data.get('upload')

        if not username and not email and not password and not password_repeat:
            raise ValidationError('You have to write something!') 
        if CustomUser.objects.dublicate_entry(username):
            raise ValidationError("User already exists")
        if password_repeat != password:
            raise ValidationError("Passwords are different")

"""
class UserForm(ModelForm):
    
    def clean_username(self):
        data = self.cleaned_data['username']
        if "*" in data:
            raise ValidationError("No")
        return data
    
    class Meta:
        model = User
        fields = ['username', 'password', 'upload']
        help_texts = {
            'upload': 'Upload your profile avatar'
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        upload = cleaned_data.get('upload')
        if not username or not password or not upload:
            raise ValidationError('There were problems creating your account!')"""