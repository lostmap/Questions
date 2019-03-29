from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hot/', views.hot, name='hot'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('up/<int:quest_id>/', views.up, name='up'),
    path('down/<int:quest_id>/', views.down, name='down'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('question/<int:quest_id>/', views.question, name='question_id'),
    path('profile/<str:profile_name>/', views.profile, name='profile_name'),
    path('tag/<str:tag_name>/', views.question_tag, name='question_tag'),
    path('ask/', views.ask, name='ask_page'),
     

] + static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)