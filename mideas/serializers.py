from rest_framework import serializers
from .models import Midea

class MideaSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    
    # Declaramos o campo file explicitamente como ImageField 
    # para o Swagger renderizar o input de upload
    file = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Midea
        fields = ['id', 'owner', 'owner_username', 'post', 'image_profile', 'file', 'link']
        read_only_fields = ['id', 'owner']

    def validate(self, attrs):
        # 1. Validação entre 'post' e 'image_profile'
        post = attrs.get('post', getattr(self.instance, 'post', None))
        image_profile = attrs.get('image_profile', getattr(self.instance, 'image_profile', False))

        has_post = post is not None
        has_profile = bool(image_profile)

        if has_post == has_profile:  # Ambas True ou ambas False
            raise serializers.ValidationError({
                "non_field_errors": "A mídia deve ser associada a um Post OU marcada como Foto de Perfil (image_profile=True), nunca ambos ou nenhum."
            })

        # 2. Validação entre 'file' e 'link'
        file = attrs.get('file', getattr(self.instance, 'file', None))
        link = attrs.get('link', getattr(self.instance, 'link', None))

        has_file = file is not None and file != ""
        has_link = link is not None and link != ""

        if has_file == has_link:  # Ambas preenchidas ou ambas vazias
            raise serializers.ValidationError({
                "non_field_errors": "Forneça exatamente uma fonte de mídia: um arquivo (file) OU um link externo (link)."
            })

        return attrs