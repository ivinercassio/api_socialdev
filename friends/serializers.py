from rest_framework import serializers
from django.db.models import Q
from .models import Friend

class FriendSerializer(serializers.ModelSerializer):
    friend_one_username = serializers.ReadOnlyField(source='friend_one.username')
    friend_two_username = serializers.ReadOnlyField(source='friend_two.username')

    class Meta:
        model = Friend
        fields = ['id', 'friend_one', 'friend_one_username', 'friend_two', 'friend_two_username', 'date_start']
        read_only_fields = ['id', 'friend_one', 'date_start']

    def validate(self, attrs):
        request_user = self.context['request'].user
        friend_two = attrs.get('friend_two')

        # 1. Não pode ser amigo de si mesmo
        if request_user == friend_two:
            raise serializers.ValidationError({
                "friend_two": "Você não pode adicionar a si mesmo como amigo."
            })

        # 2. Verificar se já existe amizade entre os dois (em qualquer sentido)
        if self.instance is None:  # Apenas na criação
            already_friends = Friend.objects.filter(
                (Q(friend_one=request_user) & Q(friend_two=friend_two)) |
                (Q(friend_one=friend_two) & Q(friend_two=request_user))
            ).exists()

            if already_friends:
                raise serializers.ValidationError({
                    "non_field_errors": "Já existe uma relação de amizade registrada entre esses usuários."
                })

        return attrs