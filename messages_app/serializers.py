from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    from_user_username = serializers.ReadOnlyField(source='from_user.username')
    to_user_username = serializers.ReadOnlyField(source='to_user.username')

    class Meta:
        model = Message
        fields = [
            'id', 'friend', 'from_user', 'from_user_username', 
            'to_user', 'to_user_username', 'text', 'date_published'
        ]
        read_only_fields = ['id', 'from_user', 'date_published']

    def validate(self, attrs):
        request_user = self.context['request'].user
        friend = attrs.get('friend')
        to_user = attrs.get('to_user')

        # 1. O usuário logado deve fazer parte da amizade indicada
        if friend.friend_one != request_user and friend.friend_two != request_user:
            raise serializers.ValidationError({
                "friend": "Você só pode enviar mensagens dentro de uma amizade da qual faz parte."
            })

        # 2. O destinatário deve pertencer à mesma amizade
        if to_user not in [friend.friend_one, friend.friend_two]:
            raise serializers.ValidationError({
                "to_user": "O destinatário informado não faz parte desta relação de amizade."
            })

        # 3. Não pode enviar mensagem para si mesmo
        if to_user == request_user:
            raise serializers.ValidationError({
                "to_user": "Você não pode enviar mensagens para si mesmo."
            })

        return attrs