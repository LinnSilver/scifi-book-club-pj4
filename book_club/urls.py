from django.urls import path
from . import views
from .views import logoutView
from .views import ManagerView
from .views import manager
from .views import LoginView
from .views import handler404, handler500, handler403, handler405


urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('manager/', ManagerView.as_view(), name='manager'),
    path('manager/', manager, name='manager'),
    path('login/', LoginView.as_view(), name='login'),

]

handler404 = 'book_klub.views.handler404'
handler500 = 'book_klub.views.handler500'
handler403 = 'book_klub.views.handler403'
handler405 = 'book_klub.views.handler405'
