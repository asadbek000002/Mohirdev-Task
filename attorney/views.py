from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
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


class CustomLogoutView(APIView):
    """
    POST /logout/
    Foydalanuvchi chiqishi.
    Refresh token black list qilinadi.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


class LeadsPagination(PageNumberPagination):
    page_size = 10


class LeadsListApiView(ListAPIView):
    """
         GET /leads/
         Barcha lead'larni ro‘yxatini olish uchun endpoint.

         Query parameters:
         - `status` (optional): Lead status bo‘yicha filterlash (`PENDING` yoki `REACHED_OUT`)
         - `email` (optional): Email bo‘yicha qidirish (to‘liq yoki qisman)
      """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LeadsListSerializer
    pagination_class = LeadsPagination

    def get_queryset(self):
        queryset = Lead.objects.all().order_by('-created_at')
        status_filter = self.request.query_params.get('status', '').upper()
        email_query = self.request.query_params.get('email')

        filters = Q()

        if status_filter in [Lead.LeadStatus.PENDING, Lead.LeadStatus.REACHED_OUT]:
            filters &= Q(status=status_filter)

        if email_query:
            filters &= Q(email__icontains=email_query.strip())

        queryset = queryset.filter(filters).order_by('-created_at')

        return queryset


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


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def lead_statistics(request):
    """
       Lead statistikasi:
       jami, qabul qilingan va kutayotganlar soni.
       Foydalanuvchi autentifikatsiyasi talab qilinadi.
    """
    total = Lead.objects.count()
    accepted = Lead.objects.filter(status=Lead.LeadStatus.REACHED_OUT).count()
    pending = Lead.objects.filter(status=Lead.LeadStatus.PENDING).count()
    return Response({
        "total_leads": total,
        "accepted_leads": accepted,
        "pending_leads": pending,
    })
