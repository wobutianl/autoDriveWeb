from django.urls import path

from . import views
from . import views_api

urlpatterns = [
    path('', views.index, name='index'),
    path('/api/updateapp/<int:pid>/<str:lon>/<str:lat>/<int:tasktype>/<int:taskstatus>', views_api.updateApp, name="updateApp"),
    path('/api/canceltask/<int:pid>', views_api.cancelTask, name="cancelTask"),
    path('/api/starttask/<int:pid>/<str:startlon>/<str:startlat>/<str:endlon>/<str:endlat>', views_api.startTask, name="startTask"),
    path('/api/parktask/<int:pid>/<int:carNum>', views_api.parkTask, name = "parkTask"),

    path('/api/launchtask/<int:pid>/<int:carNum>', views_api.launchTask, name = "launchTask"),
    path('/api/registertask/<int:pid>/<str:password>', views_api.registerTask, name = "registerTask"),
    path('/api/logintask/<int:pid>/<str:password>', views_api.loginTask, name = "loginTask"),
    path('/api/parkinfo/<int:pid>', views_api.parkInfo, name = "parkInfo"),
    path('/api/unstartinfo/<int:pid>', views_api.unstartInfo, name = "unstartInfo"),
    path('/api/vehicleinfo/<int:pid>/<int:carNum>', views_api.vehicleInfo, name = "vehicleInfo"),
    path('/api/vehicleidinfo/<int:pid>', views_api.vehicleIdInfo, name = "vehicleIdInfo"),
    path('/api/comformmsg/<int:pid>', views_api.comformMsg, name = "comformMsg"),
    path('/api/vehicleupdate/', views_api.updateVehicle, name = "updateVehicle"),
]