from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    post_title = serializers.ReadOnlyField(source='post.title')
    comment_text = serializers.ReadOnlyField(source='comment.text')

    class Meta:
        model = Report
        fields = ['id', 'post', 'post_title', 'comment', 'comment_text', 'reason', 'date_report']
        read_only_fields = ['id', 'date_report']

    def validate(self, attrs):
        # Captura os campos da requisição (ou da instância em caso de PATCH)
        post = attrs.get('post', getattr(self.instance, 'post', None))
        comment = attrs.get('comment', getattr(self.instance, 'comment', None))

        has_post = post is not None
        has_comment = comment is not None

        # Garante a exclusão mútua: ou tem Post, ou tem Comment (nunca ambos e nunca nenhum)
        if has_post == has_comment:
            raise serializers.ValidationError({
                "non_field_errors": "A denúncia (Report) deve estar associada a um Post OU a um Comentário, nunca a ambos ou a nenhum."
            })

        return attrs

    def validate_reason(self, value):
        # Valida se o reason não veio em branco
        if not value or not value.strip():
            raise serializers.ValidationError("O motivo da denúncia é obrigatório.")
        return value

    def update(self, instance, validated_data):
        # Remove o 'reason' dos dados validados caso ele seja enviado em um PUT/PATCH,
        validated_data.pop('reason', None)
        return super().update(instance, validated_data)