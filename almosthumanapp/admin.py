from django.contrib import admin
from .models import User, Stripe_subscription
# Register your models here.

admin.site.register(User)
admin.site.register(Stripe_subscription)