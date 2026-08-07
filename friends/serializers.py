from rest_framework import serializers
from django.db.models import Q
from .models import FriendRequest, Friend

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

class FriendRequestSerializer(serializers.ModelSerializer):
    user_one_username = serializers.ReadOnlyField(source='user_one.username')
    user_two_username = serializers.ReadOnlyField(source='user_two.username')

    class Meta:
        model = FriendRequest
        fields = [
            'id', 
            'user_one', 
            'user_one_username', 
            'user_two', 
            'user_two_username', 
            'date_request'
        ]
        read_only_fields = ['id', 'user_one', 'date_request']

    def validate_user_two(self, value):
        request = self.context.get('request')
        user_one = request.user

        # Regra 1: Não pode enviar solicitação para si mesmo
        if user_one == value:
            raise serializers.ValidationError("Você não pode enviar um convite de amizade para você mesmo.")

        # Regra 2: Não pode enviar solicitação se já forem amigos
        are_friends = Friend.objects.filter(
            (Q(friend_one=user_one) & Q(friend_two=value)) |
            (Q(friend_one=value) & Q(friend_two=user_one))
        ).exists()

        if are_friends:
            raise serializers.ValidationError("Você e este usuário já possuem uma amizade cadastrada.")

        # Regra 3: Não pode ter um pedido pendente duplicado
        existing_request = FriendRequest.objects.filter(
            (Q(user_one=user_one) & Q(user_two=value)) |
            (Q(user_one=value) & Q(user_two=user_one))
        ).exists()

        if existing_request:
            raise serializers.ValidationError("Já existe uma solicitação de amizade pendente entre vocês.")

        return value