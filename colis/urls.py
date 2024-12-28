

from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name=""),
    path('register',views.register, name="register"),
    path('login' ,views.login, name="login"),
   



]


from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  
    path('register/', views.register, name='register'),  
    path('login/', views.login, name='login'),  
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),  
    path('logout' ,views.logout, name="logout"),
    path('new_colis',views.create_colis,name='new_colis'),#Create
    path('update_colis/<int:pk>/', views.update_colis, name='update_colis'), #modification
    path('delete_colis/<int:pk>/', views.delete_colis, name='delete_colis'), #suppression
    
     path('account',views.view_account,name='view_account'),#view profile
     path('update_account',views.update_profile,name='update_profile'),#view profile
     path('profile/delete/' ,views.delete_profile, name='delete_profile'),#delete profile
     
     path('accept/<int:pk>/', views.accept_colis, name='accept'),#colis livré
     path('refuse/<int:pk>/', views.refuse_colis, name='refuse'),#colis annulé

    path('user_coli/<int:pk>',views.user_view_colis,name='user_coli'),#view one colis
    path('dashboard',views.dashboard,name='dashboard'),# admin dashboard/Read
    path('coli/<int:pk>',views.view_colis,name='coli'),#view one colis(admin)

       path('admin-view/profiles/', views.admin_view_profiles, name='admin_view_profiles'),
    path('profiles/delete/<str:username>/', views.admin_delete_user, name='admin_delete_user'),
]
