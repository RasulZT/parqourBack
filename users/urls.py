from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import TelegramAuthView, UsersByRoleView

urlpatterns = [
    path("tgregister/", TelegramAuthView.as_view(), name="telegram_auth"),
    path("find/", UsersByRoleView.as_view(), name="telegram_auth"),

    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),# логин по username + password (если нужно)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # обновить access
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
