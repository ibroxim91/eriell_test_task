from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import UserApiView, StudentAvgApiView, GroupAvgApiView

app_name = "api"
urlpatterns = [
    
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('users', UserApiView.as_view(), name='users'),
    path('student/<int:student_id>/avg', StudentAvgApiView.as_view(), name='avg_student'),
    path('group/<int:group_id>/avg', GroupAvgApiView.as_view(), name='avg_group'),
    
]
