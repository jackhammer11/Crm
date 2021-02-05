from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.home,name="home"),
    path('product/',views.products,name="product"),
    path('customer/',views.customer_page,name="customer"),
    path('order/',views.orders,name="order"),



    path('customer_info/<str:pk_test>',views.customer_info,name="customer_info"), 
    path('create_customer/',views.create_customer,name="create_customer"),

    path('add_product/',views.add_product,name="add_product"),
    path('update_product/<str:pk>/',views.updateProduct,name="updateproduct"),
    path('delete_product/<str:pk>/',views.deleteProduct,name="deleteproduct"),

    path('create_order/<str:pk>/',views.createOrder,name="create"),
    path('update_order/<str:pk>/',views.updateOrder,name="update"),
    path('delete_order/<str:pk>/',views.deleteOrder,name="delete"),

    path('signup/',views.signup,name="signup"),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),

    path('user/',views.userpage,name="user"),
    path('account/',views.accountSettings,name="account"),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="reset_password"),

    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),name = "password_reset_done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),name="password_reset_confirm"),

    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),name = "password_reset_complete"),
] 
