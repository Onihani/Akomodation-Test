from django.urls import path
from . import views

urlpatterns = [
path('signup/', views.signup, name='signup'),
path('login/', views.user_login, name='login_user'),
path('logout/', views.log_out, name='logout'),
#path('deleted/', views.deleted, name='deleted'),
path('dashboard/', views.dashboard, name='dashboard'),
path('read/', views.read, name='read'),
#path('logout/', views.log_out, name='logout'),
path('create/', views.create,  name='create'),
path('update/<int:pk>/', views.Update.as_view(), name='update'),
path('delete/', views.delete_obj, name='delete'),
path('update_user/<int:pk>/', views.UpdateUser.as_view(), name='update_user'),
path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
path("message/", views.message, name='message'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
path('password_reset_done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
path('password_reset_complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
path('info_changed/', views.info, name='info'),

# path('change_password/', views.PasswordChangeView.as_view(), name='change'),

path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
]
