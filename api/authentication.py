
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTAllowInactiveAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Permite usuarios inactivos al obtener el user desde el token.
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_id = validated_token.get("user_id")

        if not user_id:
            return None

        try:
            user = User.objects.get(id=user_id)
            return user  # aquí no revisamos is_active
        except User.DoesNotExist:
            return None
