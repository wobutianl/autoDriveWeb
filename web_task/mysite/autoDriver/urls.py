from django.urls import path

from . import views
from . import views_api, views_vehicle

urlpatterns = [
    path('', views.index, name='index'),
    path('api/app/update/<int:pid>/<str:lon>/<str:lat>/<int:tasktype>/<int:taskstatus>', views_api.update, name="updateApp"),
    path('api/app/cancel/<int:pid>', views_api.cancel, name="appCancel"),
    path('api/app/reserve/<int:pid>/<str:startlon>/<str:startlat>/<str:endlon>/<str:endlat>', views_api.reserve, name="appReserve"),
    path('api/app/parktask/<int:pid>/<int:carNum>', views_api.park, name = "appPark"),
    path('api/app/run/<int:pid>/', views_api.run, name = "appRun"),

    path('api/app/launch/<int:pid>/<int:carNum>', views_api.launch, name = "appLaunch"),
    path('api/app/register/<int:pid>/<str:password>', views_api.register, name = "appRegister"),
    path('api/app/userlogin/<int:pid>/<str:password>', views_api.userLogin, name = "userLogin"),
    path('api/app/adminlogin/<int:pid>/<str:password>', views_api.adminLogin, name = "adminLogin"),
    path('api/app/parkinfo/<int:pid>', views_api.parkInfo, name = "parkInfo"),
    path('api/app/unstartinfo/<int:pid>', views_api.unstartInfo, name = "unstartInfo"),
    path('api/app/vehicleinfo/<int:pid>/<int:carNum>', views_api.vehicleInfo, name = "vehicleInfo"),
    path('api/app/vehiclelist/<int:pid>', views_api.vehicleList, name = "vehicleList"),
    path('api/app/taskquery/<int:pid>', views_api.taskQuery, name = "comformMsg"),

    ##############  vehicle #######
    path('api/vehicle/update/<str:carnum>/<int:vehicletype>/<int:available>/<str:lon>/<str:lat>/<int:havetask>/<str:battery>/<str:estimatetime>/<str:odometry>', views_vehicle.update, name = "updateVehicle"),
    path('api/vehicle/gettask/<str:carnum>/<int:vehicletype>/', views_vehicle.getTask, name = "vehicleGetTask"),
    path('api/vehicle/begin/<str:carnum>/<int:vehicletype>/', views_vehicle.begin, name = "vehicleBegin"),
    path('api/vehicle/run/<str:carnum>/<int:vehicletype>/', views_vehicle.run, name = "vehicleRun"),
    path('api/vehicle/arrival/<str:carnum>/<int:vehicletype>/', views_vehicle.arrival, name = "vehicleArrival"),
]