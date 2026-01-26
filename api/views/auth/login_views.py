from api.views.auth import serializers
# from django.contrib.auth.models import User
from ies.models import User, InvitationToken
from rest_framework.response import Response
from rest_framework import permissions, views, status
from api.mixins import CreateRetrieveMix


class UserLoginAPIView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        from rest_framework.exceptions import ParseError
        from rest_framework.authtoken.models import Token
        # from circles.views import activate_invitation, invitation_search
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        email = serializer.data.get('email', None)
        username = serializer.data.get('username', None)
        password = serializer.data.get('password', None)
        # invitation_key = serializer.data.get('key', False)

        if email:
            user_query = User.objects.filter(email=email)
        elif username:
            user_query = User.objects.filter(username=username)
        else:
            raise ParseError(
                detail="Please enter username or email to login.")

        if user_query.count() == 1:
            user_obj = user_query.first()
        else:
            raise ParseError(detail="This username/email is not valid.")
        if not user_obj.check_password(password):
            raise ParseError(detail="Invalid credentials.")
        if not user_obj.is_active:
            raise ParseError(detail="User not active.")

        auth_token = getattr(user_obj, "auth_token", None)
        if not auth_token:
            user_obj.auth_token, is_created = Token.objects\
                .get_or_create(user=user_obj)

        user_serializer = serializers.UserDataSerializer(
            user_obj, context={"request": request})

        return Response(user_serializer.data, status=status.HTTP_200_OK)
        # get_serializer = serializers.UserDataSerializer
        # data = get_serializer(user_obj, context={'request': request}).data
        # return Response(data, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = serializers.UserDataSerializer(
                user, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response()


class InvitationTokenView(views.APIView):
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, **kwargs):
        from django.utils import timezone
        from ies.models import InvitationToken
        from rest_framework.exceptions import PermissionDenied
        token_key = request.query_params.get("token")
        invitation_token = InvitationToken.objects\
            .filter(key=token_key, member__isnull=True).first()
        if not invitation_token:
            raise PermissionDenied

        user = User()
        user.institution = invitation_token.institution
        user.change_password = True

        email = request.data.get("email")
        same_email_member = User.objects.filter(email=email).first()
        if same_email_member:
            return Response(
                {"errors": {
                    "email": [
                        "Ya existe un usuario registrado con este email."]}},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(
            user, data=request.data, context={'request': request})
        if serializer.is_valid():
            final_user = serializer.save()
            invitation_token.user = final_user
            invitation_token.used_at = timezone.now()
            invitation_token.save()
            user_serializer = serializers.UserProfileSerializer(
                final_user, context={'request': request})
            return Response(user_serializer.data)

        return Response({"errors": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class CheckingViewSet(CreateRetrieveMix):
    queryset = InvitationToken.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.InvitationTokenSerializer

    def retrieve(self, request, *args, **kwargs):
        from django.utils import timezone

        invitation_token = self.get_object()
        if invitation_token.user or invitation_token.used_at:
            return Response(
                {"detail": "La invitación ya ha sido utilizada."},
                status=status.HTTP_400_BAD_REQUEST)
        if not invitation_token.viewed_at:
            invitation_token.viewed_at = timezone.now()
            invitation_token.save()
        serializer = self.serializer_class(invitation_token)
        return Response(serializer.data)
