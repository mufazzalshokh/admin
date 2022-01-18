from django.urls import path

from products.views import ProductTemplateView

app_name = 'products'

urlpatterns = [
    # path('', products_list)
    path('', ProductTemplateView.as_view())
]
