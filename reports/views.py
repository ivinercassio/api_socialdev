from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para a entidade REPORT
    """
    queryset = Report.objects.all().order_by('-date_report')
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'], url_path='post')
    def by_post(self, request, pk=None):
        """
        GET /api/reports/:id/post
        Retorna todas as denúncias associadas ao Post (:id)
        """
        post_reports = Report.objects.filter(post_id=pk).order_by('-date_report')
        serializer = self.get_serializer(post_reports, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='comment')
    def by_comment(self, request, pk=None):
        """
        GET /api/reports/:id/comment
        Retorna todas as denúncias associadas ao Comentário (:id)
        """
        comment_reports = Report.objects.filter(comment_id=pk).order_by('-date_report')
        serializer = self.get_serializer(comment_reports, many=True)
        return Response(serializer.data)