from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
   
    path("dashboard",dashboard,name="dashboard"),
    path("signup",signup_,name="signup"),
    path("login",login_,name="login"),
    path("logout",logout_,name="logout"),
    path("change_password",change_password,name="change_password"),
    path("forgot_password",forgot_password,name="forgot_password"),
    path("change_password_link/<str:email>/<int:token>",change_password_link,name="change_password_link"),
    path("userhome",userhome,name="userhome"),
    path("usertemplate",usertemplate,name="usertemplate"),
    path("useravatar",useravatar,name="useravatar"),
    path("uservideo",uservideo,name="uservideo"),
    path("pricing",pricing,name="pricing"),
    path("checkout",checkout,name="checkout"),
    path("success",success_payment,name="success"),
    path("cancelsubscription",cancel_subscription,name="cancelsubscription"),
    path("paypalpayment",paypal_payment,name="paypalpayment"),
    path("paypal-return",paypal_return,name="paypal-return"),
    path("paypal-cancel",paypal_cancel,name="paypal-cancel"),
    path("heygentemplate",heygen_template,name="heygentemplate"),
    path("imageurl",image_url,name="imageurl"),
    path("talkingphoto",talking_photo,name="talkingphoto"),
    path("createvideo",create_video,name="createvideo"),
    path("uploadaudio",upload_audio,name="uploadaudio"),
]