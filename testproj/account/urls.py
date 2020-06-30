from django.urls import path, include
from account.views import SignUpView, UserProfileView, UserProfileUpdateView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('profile/update/<int:pk>', UserProfileUpdateView.as_view(), name='update'),
    path('',include('django.contrib.auth.urls')),
]