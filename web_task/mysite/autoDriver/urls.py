from django.urls import path

from . import views
from . import views_api, views_vehicle, view_api_app, view_api_vehicle

urlpatterns = [
    path('', views.index, name='index'),
    path('/api/app/update/<int:pid>/<str:lon>/<str:lat>/<int:tasktype>/<int:taskstatus>', views_api.update, name="updateApp"),
    path('/api/app/cancel/<int:pid>', views_api.cancel, name="appCancel"),
    path('/api/app/reserve/<int:pid>/<str:startlon>/<str:startlat>/<str:endlon>/<str:endlat>', views_api.reserve, name="appReserve"),
    path('/api/app/parktask/<int:pid>/<int:carNum>', views_api.park, name = "appPark"),
    path('/api/app/run/<int:pid>/', views_api.run, name = "appRun"),

    path('/api/app/launch/<int:pid>/<int:carNum>', views_api.launch, name = "appLaunch"),
    #path('/api/app/register/<int:pid>/<str:password>', views_api.register, name = "appRegister"),
    path('/api/app/userlogin/<int:pid>/<str:password>', views_api.userLogin, name = "userLogin"),
    path('/api/app/adminlogin/<int:pid>/<str:password>', views_api.adminLogin, name = "adminLogin"),
    path('/api/app/parkinfo/<int:pid>', views_api.parkInfo, name = "parkInfo"),
    path('/api/app/unstartinfo/<int:pid>', views_api.unstartInfo, name = "unstartInfo"),
    path('/api/app/vehicleinfo/<int:pid>/<int:carNum>', views_api.vehicleInfo, name = "vehicleInfo"),
    path('/api/app/vehiclelist/<int:pid>', views_api.vehicleList, name = "vehicleList"),
    path('/api/app/taskquery/<int:pid>', views_api.taskQuery, name = "comformMsg"),

    path('/api/app/register/', view_api_app.register, name = "appRegister"),
    path('/api/app/update/', view_api_app.update, name="updateApp"),
    path('/api/app/cancel/', view_api_app.cancel, name="appCancel"),
    path('/api/app/reserve/', view_api_app.reserve, name="appReserve"),
    path('/api/app/parktask/', view_api_app.park, name = "appPark"),
    path('/api/app/run/', view_api_app.run, name = "appRun"),
    path('/api/app/paid/', view_api_app.paid, name = "paid"),

    path('/api/app/launch/', view_api_app.launch, name = "appLaunch"),
    path('/api/app/userlogin/', view_api_app.userLogin, name = "userLogin"),
    path('/api/app/adminlogin/', view_api_app.adminLogin, name = "adminLogin"),
    path('/api/app/parkinfo/', view_api_app.parkInfo, name = "parkInfo"),
    path('/api/app/unstartinfo/', view_api_app.unstartInfo, name = "unstartInfo"),
    path('/api/app/vehicleinfo/', view_api_app.vehicleInfo, name = "vehicleInfo"),
    path('/api/app/vehiclelist/', view_api_app.vehicleList, name = "vehicleList"),
    path('/api/app/taskquery/', view_api_app.taskQuery, name = "comformMsg"),

    ##############  vehicle #######
    path('/api/vehicle/update/<str:carnum>/<int:vehicletype>/<int:available>/<str:lon>/<str:lat>/<int:havetask>/<str:battery>/<str:estimatetime>/<str:odometry>', views_vehicle.update, name = "updateVehicle"),
    path('/api/vehicle/gettask/<str:carnum>/<int:vehicletype>/', views_vehicle.getTask, name = "vehicleGetTask"),
    path('/api/vehicle/begin/<str:carnum>/<int:vehicletype>/', views_vehicle.begin, name = "vehicleBegin"),
    path('/api/vehicle/run/<str:carnum>/<int:vehicletype>/', views_vehicle.run, name = "vehicleRun"),
    path('/api/vehicle/arrival/<str:carnum>/<int:vehicletype>/', views_vehicle.arrival, name = "vehicleArrival"),


    path('/api/vehicle/update/', view_api_vehicle.update, name = "updateVehicle"),
    path('/api/vehicle/gettask/', view_api_vehicle.getTask, name = "vehicleGetTask"),
    path('/api/vehicle/begin/', view_api_vehicle.begin, name = "vehicleBegin"),
    path('/api/vehicle/run/', view_api_vehicle.run, name = "vehicleRun"),
    path('/api/vehicle/arrival/', view_api_vehicle.arrival, name = "vehicleArrival"),
    path('/api/vehicle/cancel/', view_api_vehicle.cancel, name = "vehicleCancel"),


    ################################   ajax   ###########################
    path('/ajax_dict/<str:car_num>/', views.ajax_dict, name='ajax-dict'),
]