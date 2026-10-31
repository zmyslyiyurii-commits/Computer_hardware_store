"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from store.views import (
    CategoryProductsView,
    add_to_cart_view,
    cart_view,
    checkout_view,
    favorites_view,
    HomeView,
    LoginView,
    order_success_view,
    ProductDetailView,
    ProfileView,
    RegisterView,
    toggle_favorite_view,
    update_cart_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    # ID категорії визначає, товари якої категорії показати в каталозі.
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart/update/<int:product_id>/', update_cart_view, name='update_cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('order/complete/', order_success_view, name='order_success'),
    path('favorites/', favorites_view, name='favorites'),
    path('favorites/toggle/<int:product_id>/', toggle_favorite_view, name='toggle_favorite'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
