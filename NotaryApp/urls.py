from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.Login, name='Login'),
    path('signup/', views.Signup, name='Signup'),
    path('loginaction/', views.LoginAction, name='LoginAction'),
    path('signupaction/', views.SignupAction, name='SignupAction'),
    path('addnotary/', views.AddNotary, name='AddNotary'),
    path('addnotaryaction/', views.AddNotaryAction, name='AddNotaryAction'),
    path('viewnotary/', views.ViewNotary, name='ViewNotary'),
    path('delete_notary/<int:doc_id>/', views.delete_notary, name='delete_notary'),
    path('logout/', views.LogoutAction, name='LogoutAction'),
    path('verify-document/', views.verify_document, name='verify_document'),
    path('verify-document-action/', views.verify_document_action, name='verify_document_action'),
] 