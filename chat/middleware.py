from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_dict = parse_qs(scope['query_string'].decode('utf-8'))
        user = AnonymousUser()
        if 'token' in query_dict:
            user = await self.get_user(query_dict['token'][0])
        scope['user'] = user
        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        try:
            return Token.objects.get(key__exact=token).user
        except Token.DoesNotExist:
            return AnonymousUser()
