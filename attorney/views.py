from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from attorney.serializers import CustomLoginSerializer, LeadsListSerializer, LeadStatusUpdateSerializer
from intake.models import Lead
from intake.tasks import lead_email_task


class CustomLoginView(APIView):
    """
       POST /login/
        Shaxsiy kirish nuqtasi.

       Kirish uchun foydalanuvchi `username` va `password` yuboradi.
       Muvaffaqiyatli autentifikatsiya qilinganda token yoki foydalanuvchi ma'lumotlari qaytariladi.
    """

    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.db.models import Q


class LeadsListApiView(APIView):
    """
       GET /leads/
       Barcha lead'larni ro‘yxatini olish uchun endpoint.

       Query parameters:
       - `status` (optional): Lead status bo‘yicha filterlash (`PENDING` yoki `REACHED_OUT`)
       - `email` (optional): Email bo‘yicha qidirish (to‘liq yoki qisman)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        status_filter = request.query_params.get('status')
        email_query = request.query_params.get('email')

        leads = Lead.objects.all()

        if status_filter in [Lead.LeadStatus.PENDING, Lead.LeadStatus.REACHED_OUT]:
            leads = leads.filter(status=status_filter)

        if email_query:
            leads = leads.filter(email__icontains=email_query.strip())

        serializer = LeadsListSerializer(leads, many=True)
        return Response(serializer.data)


class LeadStatusUpdateAPIView(APIView):
    """
        PATCH /leads/<id>/
        Lead status'ini `REACHED_OUT` qilib belgilaydi.

        Faqat autentifikatsiyadan o‘tgan foydalanuvchilar foydalanishi mumkin.
        Agar lead allaqachon `REACHED_OUT` bo‘lsa, xatolik qaytariladi (HTTP_400_BAD_REQUEST).

    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)

        if lead.status == Lead.LeadStatus.REACHED_OUT:
            return Response(
                {"detail": "Lead already marked as reached out."},
                status=status.HTTP_400_BAD_REQUEST
            )

        lead.status = Lead.LeadStatus.REACHED_OUT

        lead.save()
        lead_email_task.delay(lead.id, request.user.get_full_name() or request.user.username)
        serializer = LeadStatusUpdateSerializer(lead)
        return Response(serializer.data, status=status.HTTP_200_OK)
