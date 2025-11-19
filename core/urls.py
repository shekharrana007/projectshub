from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('project/<int:pk>/join/', views.project_join, name='project_join'),
    # comments
    path('project/<int:pk>/comment/', views.add_comment, name='add_comment'),

    # auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', views.profile_view, name='profile'),
]
