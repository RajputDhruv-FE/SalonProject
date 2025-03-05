from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.IndexView, name="IndexView"),
    path('Login', views.Login, name="Login"),
    path('AdminDashboard', views.AdminDashboard, name="AdminDashboard"),
    path('ForgetPassword',views.ForgetPassword,name="ForgetPassword"),
    path('reset_password/<str:token>',views.reset_password,name="reset_password"),

    path("UserTrans", views.UserTrans, name="UserTrans"),
    

    path("AreaTrans", views.AreaTrans, name="AreaTrans"),
    path("AreaTrans/<int:id>", views.AreaTrans, name="AreaTrans"),
    path("AreaList", views.AreaList, name="AreaList"),

    #user urls 
    path('UserProfile', views.UserProfile, name="UserProfile"),
    path('BookinTransaction/<int:id>', views.BookinTransaction, name="BookinTransaction"),
    path('BookingHistory', views.BookingHistory, name="BookingHistory"),
    path('BookingHistory/<int:id>', views.cancel_appointment, name="cancel_appointment"),
    path('Editprofile', views.Editprofile, name="Editprofile"),

    #service urls 
    path("ServiceTrans", views.ServiceTrans, name="ServiceTrans"),
    path("ServiceTrans/<int:id>",views.ServiceTrans, name="ServiceTrans"),
    path("ServiceList", views.ServiceList, name="ServiceList"),
    path("SelectServices", views.SelectServices, name="SelectServices"),
    

    # city urls
    path("CityTrans", views.CityTrans, name="CityTrans"),
    path("CityList", views.CityList, name="CityList"),
    path("CityTrans/<int:id>",views.CityTrans, name="CityTrans"),

    


    # owner urls
    path("UpdateSalonStatus/<int:id>",views.UpdateSalonStatus, name="UpdateSalonStatus"),
    path("SalonOwnerDashboard",views.SalonOwnerDashboard, name="SalonOwnerDashboard"),
    path("OwnerProfile",views.OwnerProfile, name="OwnerProfile"),
    path("SalonTrans",views.SalonTrans, name="SalonTrans"),
    path("SalonDetails/<int:id>",views.SalonDetails, name="SalonDetails"),
    path("upload_images",views.upload_images, name="upload_images"),
    path("ShowSlots/<int:id>",views.ShowSlots, name="ShowSlots"),
    path("accept_appointment/<int:id>",views.accept_appointment, name="accept_appointment"),
    path("Editsalon/<int:salon_id>",views.Editsalon, name="Editsalon"),

    



    #logout route
    path("Logout",views.Logout, name="Logout"),
    path("ChangePassword",views.ChangePassword, name="ChangePassword"),
    path("HandleChangePassword",views.HandleChangePassword, name="HandleChangePassword"),

    # path("CityTable", views.CityListTrans, name="CityTable"),
    # path("CityTrans/<int:id>",views.CityTrans, name="CityTrans"),
    #  path("CityDelete/<int:id>",views.CityDelect, name="CityDelete"),

    # path("AreaTable", views.AreaListTrans, name="AreaTable"),
 

]
