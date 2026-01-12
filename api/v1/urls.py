from django.urls import include, path

app_name = 'v1'

urlpatterns = [
    path('', include(('api.v1.accounts.urls', 'accounts'), namespace='accounts')),
]
