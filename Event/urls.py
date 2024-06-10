from django.urls import path
from .views import qrVerifier, qrGenerator, storeGuest, startVerification, stopVerification, homepage

urlpatterns = [path('QR/verifier/', qrVerifier),
               path('QR/generator/', qrGenerator),
               path('guest/store/', storeGuest),
               path('verification/start/', startVerification),
               path('verification/stop/', stopVerification),
               path('', homepage)
               ]
