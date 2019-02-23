from django.urls import path

from . import views
from . import views_api

urlpatterns = [
    # path('', views.index, name='index'),
    path('/api/updateapp/<int:pid>/<slug:lon>/<slug:lat>/<int:type>/<int:status>', views_api.updateApp, name="updateApp"),
    path('/api/setcanceltask/<int:pid>', views_api.setCancelTask, name="setCancelTask"),
]