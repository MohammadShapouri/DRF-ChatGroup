from django.conf import settings
from django.db import close_old_connections
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from jwt import decode as jwt_decode
from channels.middleware import BaseMiddleware




@database_sync_to_async
def get_user(self, user_pk):
	user = None
	UserModel = get_user_model()
	user = UserModel.objects.get(pk=user_pk)
	return user or AnonymousUser()





class JWTAuthMiddleware(BaseMiddleware):
	"""
	If JWT authentication has the higest priority in authentication methods,
	call it inside all authentication methods.
	"""
	def __init__(self, inner):
		self.inner = inner


	async def __call__(self, scope, receive, send):
		close_old_connections()
		jwt_token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]

		try:
			UntypedToken(jwt_token)
		except (InvalidToken, TokenError) as error:
			return None
		else:
			decoded_data = jwt_decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
			if decoded_data.get('user_id', None) == None:
				raise Exception("user_id field is required in jwt structure.", "inappropriate_jwt")
				return self.inner(dict(scope, user=AnonymousUser()), receive, send)
			else:
				user = await get_user(decoded_data['user_id'])
				scope["user"] = user
				return self.inner(dict(scope, user=user), receive, send)
