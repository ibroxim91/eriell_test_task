from django.urls import path
from .views import HomeView, GroupView, ScienceView, ScoreView
from .auth import LoginView, LogoutView

app_name = "main"

urlpatterns = [
    
    path('', HomeView.as_view(), name='home'),
    path('groups', GroupView.as_view(), name='home'),
    path('science', ScienceView.as_view(), name='science'),
    path('score', ScoreView.as_view(), name='score'),
    path('login', LoginView.as_view(), name='login'),
    path('logout',LogoutView.as_view(),  name = 'logout'),
    
]