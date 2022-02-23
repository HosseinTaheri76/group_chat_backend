from rest_framework import serializers
from chat.models import ChatGroup, Member, Message


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ('author', 'text')
        read_only_fields = ('author', 'text')


class MemberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Member
        fields = ('user', 'group_code', 'group_name')
        read_only_fields = ('user', 'group_code', 'group_name')


class ChatGroupSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, required=False)
    members = MemberSerializer(many=True, required=False)
    admin = serializers.StringRelatedField()

    class Meta:
        model = ChatGroup
        fields = ('admin', 'name', 'code', 'messages', 'members')
        read_only_fields = ('admin', 'code', 'messages', 'members')
