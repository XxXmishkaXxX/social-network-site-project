from channels.db import database_sync_to_async
from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from urllib.parse import parse_qs


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()
        query = parse_qs(scope['query_string'].decode('utf8'))
        if 'token' in query:
            try:
                token_key = query['token'][0]

                user = await self.get_user(token_key)
                
                scope['user'] = user
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token_key):
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return AnonymousUser()


def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
