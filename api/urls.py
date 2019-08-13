from django.urls import path
from api import views

urlpatterns = [
    path('countdown/', views.CountdownList.as_view()),
    path('countdown/<int:countdown_id>/', views.CountdownDetail.as_view()),
    path('countdown-event/', views.CountdownEventList.as_view()),
    path('countdown-event/<int:event_id>/', views.hello_world),
]