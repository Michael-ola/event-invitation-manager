from django.urls import path
from .views import qrVerifier, qrGenerator, storeGuest, startVerification, stopVerification, homepage, Authentication, storePassword, admin

urlpatterns = [path('QR/verifier/', qrVerifier),
               path('QR/generator/', qrGenerator),
               path('guest/store/', storeGuest),
               path('verification/start/', startVerification),
               path('verification/stop/', stopVerification),
               path('auth/', Authentication),
               path('password/store/', storePassword),
               path('admin/', admin),
               path('', homepage)
               ]
