from django.urls import include, path, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
router.register(r'tips', views.TipViewSet, basename = 'tip')
router.register(r'scraps', views.ScrapViewSet, basename = 'scrap')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += [
    path('waters/<str:year>/<str:month>/', views.WaterList.as_view()),
    path('waters/today/', views.WaterDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<str:username>/', views.UserDetail.as_view()),
    path('users/<int:pk>/nickname/', views.UserNick.as_view()),
    path('profiles/<str:username>/', views.ProfileDetail.as_view())
]