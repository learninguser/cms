from django.urls import path, include
from blog import views

urlpatterns = [
    path('',views.HomeView.as_view(), name='home'),
    path('aboutus/',views.AboutUsView.as_view(), name='aboutus'),
    path('category/<int:id>',views.CategoryView.as_view(), name='category'),
    path('blog/<str:slug>',views.PostView.as_view(), name='blog'),
    path('createpost/',views.PostCreateView.as_view(), name='createpost'),
    path('editpost/<str:slug>',views.PostUpdateView.as_view(), name='editpost'),
    path('search/', views.search, name='search')
]