from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import User, Stripe_subscription
from .helpers import send_forget_password_mail
import uuid
from django.utils.crypto import get_random_string
import requests

import stripe
from almosthumanproject import settings
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.views.decorators.csrf import csrf_exempt
import json

from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse

"""user register"""
def signup_(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')
        conpassword = request.POST.get('conpassword')
        user = User.objects.filter(email=email).exists()
        if user == False:
            if password == conpassword:
                enc_password = make_password(password)
                if role == 'admin':
                    user_obj = User(username=username,email=email,role=role,password=enc_password,is_staff=True)
                    user_obj.save()
                else:
                    user_obj = User(username=username,email=email,role=role,password=enc_password)
                    user_obj.save()   
                return HttpResponse("successfully")
            else:
                return HttpResponse("Your password and confirmation password do not match.")
        else:
            return HttpResponse("Your email is already exists")
    return render(request,'register.html')



"""user login"""
def login_(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return HttpResponse("successfully")
        else:
            return HttpResponse("Incorrect email or password")
    elif request.user.is_anonymous:
        return render(request,'login.html')
    else:        
        return redirect("/dashboard")
       
    


"""logout """
def logout_(request):
    auth.logout(request)
    return redirect('/login')


"""change password"""
@login_required
def change_password(request):
    if request.method == "POST":
        password = request.POST.get('password')
        conpassword = request.POST.get('conpassword')
        if password == conpassword:
            user = User.objects.get(email=request.user.email)
            user.set_password(password)
            user.save()
            return HttpResponse("successfully")
        return HttpResponse("Your password and confirmation password do not match.")
    return render(request, "change_password.html")


    

"""forgot password to email link"""
def forgot_password(request):    
    if request.method=='POST':
        email=request.POST.get('email')
        if not User.objects.filter(email=email).first():
            return HttpResponse("1")
        token=get_random_string(length=6, allowed_chars='0123456789')
        request.session['token'] = token
        send_forget_password_mail(email,token)    
        return HttpResponse("2")
    return render(request, "forgotpassword.html")


"""forgot password to email link"""
def change_password_link(request,email,token):  
    token2 = request.session['token']
    
    if request.method == "POST":
        password = request.POST.get('password')
        conpassword = request.POST.get('conpassword')
        if int(token) == int(token2):
            if password == conpassword:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                request.session['token']=0
                msg="password changed successfully"
                return render(request, "login.html", {'msg':msg})
            msg="Your password and confirmation password do not match."   
            return render(request, "change_password2.html", {'msg':msg})
        
        return HttpResponse("invalid link")
    return render(request, "change_password2.html")
    
           
    
"""dashboard""" 
@login_required
def dashboard(request):
    admin = User.objects.get(email=request.user.email).is_staff
    if admin == True:
        return render(request,"admindashboard.html")
    else:
        return render(request,"userdashboard.html")
        

def userhome(request):
    return render(request,"home.html")    

def usertemplate(request):
    url = "https://api.heygen.com/v1/avatar.list"
    headers = {
        "accept": "application/json",
        "x-api-key": "ZTljZDM0MmVlMDVhNDAyZTk5Zjk1OTg3ZDNkMTBhMDktMTY4Mjk0MjUwMg=="
    }

    response = requests.get(url, headers=headers)

    print(response.status_code)
    data=response.json()
    print(data['data']['avatars'][0]['avatar_states'][0]['normal_preview'])
    j=0
    template=[]
    for i in data['data']['avatars']:
        for j in i['avatar_states']:
            template1=j['video_url']['grey']
            template.append(template1)
    print(template)  
  
    return render(request,"template.html",{'template':template})  

def useravatar(request):
    url = "https://api.heygen.com/v1/avatar.list"
    headers = {
        "accept": "application/json",
        "x-api-key": "ZTljZDM0MmVlMDVhNDAyZTk5Zjk1OTg3ZDNkMTBhMDktMTY4Mjk0MjUwMg=="
    }

    response = requests.get(url, headers=headers)
    data=response.json()
    print("--------------------------",data)
    avatar=[]
    for i in data['data']['avatars']:
        for j in i['avatar_states']:
            avatar1=j['normal_preview']
            avatar.append(avatar1)
    print(avatar)  

    return render(request,"avatar.html",{'avatar':avatar})       

def uservideo(request):
    return render(request,"video.html")    

def pricing(request):
    return render(request,"pricing.html")




def checkout(request):
    if request.method == 'POST':
        sub = request.POST.get("subscription")
        if sub == "1":

            # Create a new checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                        {
                            'price': settings.STRIPE_PRICE_ID_1,
                            'quantity': 1,
                        },
                    ],

                mode='subscription',
                success_url='http://127.0.0.1:8000/success',
                cancel_url='https://example.com/cancel',
                billing_address_collection=None
            )

            # Redirect the user to the Stripe checkout page
            return redirect(session.url)
        
        elif sub == "2":
            # Create a new checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                        {
                            'price': settings.STRIPE_PRICE_ID_2,
                            'quantity': 1,
                        },
                    ],

                mode='subscription',
                success_url='http://127.0.0.1:8000/success',
                cancel_url='https://example.com/cancel',
                billing_address_collection=None
            )

            # Redirect the user to the Stripe checkout page
            return redirect(session.url)
        
        else:
            # Create a new checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                        {
                            'price': settings.STRIPE_PRICE_ID_3,
                            'quantity': 1,
                        },
                    ],

                mode='subscription',
                success_url='http://127.0.0.1:8000/success',
                cancel_url='https://example.com/cancel',
                billing_address_collection=None
            )
            
                
            # Redirect the user to the Stripe checkout page
            return redirect(session.url)
            

    return render(request, 'checkout.html')




@csrf_exempt
def webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object  # contains a stripe.PaymentIntent

        # Fulfill the order...

    elif event.type == 'payment_intent.payment_failed':
        payment_intent = event.data.object  # contains a stripe.PaymentIntent

        # Notify the customer that their payment failed...

    # ... handle other event types ...

    return HttpResponse(status=200)



def success_payment(request):
    a=stripe.Subscription.list(limit=1)
    print(a)
    user_id = request.user.id
    subscription_id = a.data[0].id
    price_id = a.data[0]["items"]["data"][0]["price"]["id"]
    
    subscription = Stripe_subscription(user_id_id=user_id,subscription_id=subscription_id,price_id=price_id)
    subscription.save()
    
    return HttpResponse("Payment successful.")



@csrf_exempt
def cancel_subscription(request):
    print(request.user.id)
    subscription_data = Stripe_subscription.objects.get(user_id_id = request.user.id)
    subscription_id = subscription_data.subscription_id

    try:
        subscription = stripe.Subscription.retrieve(subscription_id)
        subscription.delete()
        subscription_data.delete()
        
        # Update your database or take any other necessary action to reflect the subscription cancellation.
        return HttpResponse("Subscription cancelled successfully.")
    except stripe.error.InvalidRequestError as e:
        # handle any errors that occur during the cancellation process
        return HttpResponse("Error cancelling subscription: {}".format(str(e)))
    
    
    

@csrf_exempt
def paypal_payment(request):
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '20.00',
        'item_name': 'Product 1',
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("paypal-return")}',
        'cancel_return': f'http://{host}{reverse("paypal-cancel")}',
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'form':form}
    return render(request, "paypal.html", context)    


def paypal_return(request):
        messages.success(request, 'You have successfully made a payment!')
        return redirect('paypalpayment')
    
    
def paypal_cancel(request):
        messages.error(request, 'Your order has been canceled.')
        return redirect('paypalpayment')
    
    

def heygen_template(request):

    url = "https://api.heygen.com/v1/template.get?video_id=02548b8c42da4f259d24af69e5d318d7"

    headers = {
        "accept": "application/json",
        "x-api-key": "ZTljZDM0MmVlMDVhNDAyZTk5Zjk1OTg3ZDNkMTBhMDktMTY4Mjk0MjUwMg=="
    }

    response = requests.get(url, headers=headers)

    print(response.text)    
    return HttpResponse(response.text)



def image_url(request):

    url = "https://api.heygen.com/v1/upload_url.get"

    payload = {"content_type": "image/jpeg"}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": "ZTljZDM0MmVlMDVhNDAyZTk5Zjk1OTg3ZDNkMTBhMDktMTY4Mjk0MjUwMg=="
    }

    response = requests.get(url, json=payload, headers=headers)

    print(response.text)
    return HttpResponse(response.text)
    
    
 
def talking_photo(request):
     
    url = "https://api.heygen.com/v1/talking_photo.create"

    payload = {"storage_key": "prod/movio/url_upload/user_upload/f1cc0bb269cd4018aae0f2f5dcdf2285/ed316e45367a41a1bb8f76a2eab0e219.jpeg"}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": "ZTljZDM0MmVlMDVhNDAyZTk5Zjk1OTg3ZDNkMTBhMDktMTY4Mjk0MjUwMg=="
    }

    response = requests.get(url, json=payload, headers=headers)

    print(response.text)   
    return HttpResponse(response.text)
    
    
    
def create_video(request):

    url = "https://api.heygen.com/v1/video.generate"

    payload = {
        "background": "#ffffff",
        "ratio": "16:9",
        "test": False,
        "version": "v1alpha",
        "clips":[{
            "avatar_id":1661166377,
            "input_audio":" /movio/url_upload/user_upload/8694fc598eb043dbab1a09233743dd3b/081ebccc457442298c8d4cae1f32a849.mp3",
            "avatar_style": "normal",
            "offset": {
                "x": 0,
                "y": 0
            },
        "scale": 1,
    }],
        
        
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": "NjQzOWI0YTZjOWQyNGJmMWI1OTYwZjRjNzI3NDhjMTItMTY4MzgwNzI2Mg=="
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    return HttpResponse(response.text)
    
    
    

def upload_audio(request):
    url = "https://api.heygen.com/v1/upload_url.get"

    payload = {"content_type": "audio/mp3",}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": "NjQzOWI0YTZjOWQyNGJmMWI1OTYwZjRjNzI3NDhjMTItMTY4MzgwNzI2Mg=="
    }

    response = requests.get(url, json=payload, headers=headers)
    data=response.json()
    upload_url=data['data']['upload_url']
    
    # return HttpResponse(upload_url)
    
    
    # Set the upload URL and image file path
    audio_path = '/home/codenomad/Downloads/Hen.mp3'

    # Read the image file as binary data
    with open(audio_path, 'rb') as f:
        audio_data = f.read()
    response1=requests.put(upload_url,data=audio_data)
    return HttpResponse(response.text)