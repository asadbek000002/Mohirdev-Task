from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone

from intake.models import Advertisement
from intake.serializers import LeadSerializer, AdvertisementSerializer
from intake.tasks import attorney_email_task
from intake.throttle import LeadCreateThrottle


class LeadCreateApiView(APIView):
    """
       **Eslatma:** Ma’lumotlar `form-data` formatida yuborilishi kerak.

       Yangi Etakchi yaratish uchun POST usuli.
       Ushbu yakuniy nuqta umumiy foydalanuvchilarga yetakchi formani yuborish imkonini beradi.
       Muvaffaqiyatli topshirilgandan so'ng, advokatlarga elektron pochta xabari yuboriladi.
    """
    throttle_classes = [LeadCreateThrottle]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LeadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            lead = serializer.save()
            attorney_email_task.delay(lead.id)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActiveAdvertisementListView(ListAPIView):
    """
    reklamalarni qaytaradi

    GET /api/ads/
    Faqat hozir aktiv bo‘lgan reklamalarni qaytaradi
    """
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        today = timezone.now().date()
        return Advertisement.objects.filter(
            is_active=True,
            start_date__lte=today,
            end_date__gte=today
        )
