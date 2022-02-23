from asgiref.sync import async_to_sync
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, get_object_or_404, ListAPIView
from chat import serializers
from chat.models import ChatGroup, Member
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chat.permissions import NotAlreadyMember
from django.shortcuts import reverse
from channels.layers import get_channel_layer


def _notify_leave_join(group_code, username, action_type):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_code,
        {
            'type': 'chat_activity',
            'message': {
                'type': action_type,
                'username': username
            }
        }
    )


def _notify_group_deleted(group_code):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_code,
        {
            'type': 'chat_activity',
            'message': {'type': 'deleted'}
        }
    )


class ChatCreateApiView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChatGroupSerializer

    def perform_create(self, serializer):
        user = self.request.user
        chat_group = serializer.save(admin=user)
        Member.objects.create(user_id=user.id, group_id=chat_group.id)


class EnterChatApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        chat_group = get_object_or_404(ChatGroup, code=kwargs['group_code'])
        user = request.user
        if Member.objects.filter(group_id=chat_group.id, user_id=user.id).exists():
            serializer = serializers.ChatGroupSerializer(chat_group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'join_chat': reverse('join_chat', args=[chat_group.code])},
            status=status.HTTP_307_TEMPORARY_REDIRECT
        )


class JoinChatApiView(APIView):
    permission_classes = [IsAuthenticated, NotAlreadyMember]

    def get(self, request, **kwargs):
        chat_group = get_object_or_404(ChatGroup, code=kwargs['group_code'])
        self.check_object_permissions(request, chat_group)
        user = request.user
        Member.objects.create(user_id=user.id, group_id=chat_group.id)
        _notify_leave_join(chat_group.code, user.username, 'join')
        serializer = serializers.ChatGroupSerializer(chat_group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LeaveChatApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        chat_group = get_object_or_404(ChatGroup, code=kwargs['group_code'])
        user = request.user
        if user == chat_group.admin:
            chat_group.delete()
            _notify_group_deleted(chat_group.code)
        else:
            get_object_or_404(Member, group_id=chat_group.id, user_id=user.id).delete()
            _notify_leave_join(chat_group.code, user.username, 'leave')
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserMembershipsListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.MemberSerializer

    def get_queryset(self):
        return self.request.user.memberships.all()
