from django.urls import path
from .import views

urlpatterns = [
    path('dashboard',views.DashBoardView.as_view(),name='dashboard'),
    path('trainers-list/',views.TrainersListView.as_view(),name='trainers-list'),
    path('register-view/',views.TrainerRegistrationView.as_view(),name='register-view'),
    path('trainer-detail/<str:uuid>/',views.TrainerDetailView.as_view(),name='trainer-detail'),
    path('trainer-delete/<str:uuid>/',views.TrainerDeleteView.as_view(),name='trainer-delete'),
    path('trainer-update/<str:uuid>/',views.TrainerUpdateView.as_view(),name='trainer-update'),
    
]
