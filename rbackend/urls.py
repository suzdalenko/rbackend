from django.urls import path, include

urlpatterns = [
    path('myapp/', include('myapp.myroutes')),
]
