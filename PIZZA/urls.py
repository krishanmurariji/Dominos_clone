from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from PIZZA.views import *
from django.urls import reverse
urlpatterns = [
    path('',home, name = 'base'),
    path('login/', login_page, name ='login'),
    path('register/',register_page, name="register" ),
    path('add-cart/<pizza_uid>/', add_cart, name="add_cart"),
    path('cart/', cart, name ='cart'),
    path('remove_cart_items/<cart_items_uid>/', remove_cart_items, name ='remove_cart_items'),
    path('orders/', orders, name ='orders'),
    path('success/', success, name ='success'),
    
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()