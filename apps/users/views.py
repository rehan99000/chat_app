from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import User
from apps.users.permissions import IsAdmin
from apps.users.serializers import (
    CreateUserSerializer,
    CustomTokenObtainPairSerializer,
    GetUserSerializer,
    UpdatePasswordSerializer,
    UpdateProfileSerializer,
)
from apps.utils.views.base import BaseViewset, ResponseInfo


class UserViewSet(BaseViewset):
    """
    API endpoints that allows users to be viewed.
    """
    queryset = User.objects.all()
    action_serializers = {
        'default': GetUserSerializer,
        'create': CreateUserSerializer,
        'update': CreateUserSerializer,
        'partial_update': CreateUserSerializer,
        'get_me': GetUserSerializer,
        'update_password': UpdatePasswordSerializer,
        'update_profile': UpdateProfileSerializer,
    }
    action_permissions = {
        'default': [IsAuthenticated, IsAdmin],
        'list': [IsAuthenticated],
        'create': [IsAuthenticated],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
        'get_me': [IsAuthenticated],
        'update_password': [IsAuthenticated],
        'update_profile': [IsAuthenticated],
    }
    filter_backends = [SearchFilter]
    search_param = 'search'
    search_fields = [
        'first_name', 'last_name', 'email'
    ]
    ordering_fields = ['first_name', 'last_name',
                       'email', 'role', 'date_joined']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Setting password.
        user = User.objects.create(**serializer.validated_data)
        if serializer.validated_data['is_default_calculator']:
            User.objects.exclude(pk=user.id).update(
                is_default_calculator=False)

        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data=ResponseInfo().format_response(
                data={}, message='Created', status_code=status.HTTP_201_CREATED,
            )
        )

    def partial_update(self, request, *args, **kwargs):
        id = kwargs['pk']

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        super().partial_update(request, args, kwargs)
        if serializer.validated_data.get('is_default_calculator'):
            User.objects.exclude(pk=id).update(is_default_calculator=False)

        # Updating password.
        if serializer.data.get('password'):
            user = User.objects.get(id=id)
            user.set_password(serializer.data['password'])
            user.save()

        return Response(
            status=status.HTTP_200_OK,
            data=ResponseInfo().format_response(
                data={}, message='User Updated', status_code=status.HTTP_200_OK,
            )
        )

    @action(detail=False, url_path='me', methods=['get'])
    def get_me(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, many=False)

        return Response(
            status=status.HTTP_200_OK,
            data=ResponseInfo().format_response(
                data=serializer.data, message='Me',
                status_code=status.HTTP_200_OK,
            )
        )

    @action(detail=False, url_path='update-profile', methods=['patch'])
    def update_profile(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Updating password.
        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')
        if old_password and new_password:
            user = request.user
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
            else:
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data=ResponseInfo().format_response(
                        data={}, message='Passowrd incorrect',
                        status_code=status.HTTP_403_FORBIDDEN,
                    )
                )

        update_res = User.objects.filter(id=request.user.id).update(
            first_name=serializer.validated_data.get('first_name'),
            last_name=serializer.validated_data.get('last_name')
        )

        return Response(
            status=status.HTTP_200_OK,
            data=ResponseInfo().format_response(
                data={'affected': update_res}, message='Profile Updated',
                status_code=status.HTTP_200_OK,
            )
        )

    @action(detail=False, url_path='update-password', methods=['patch'])
    def update_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        user = request.user

        if not user.check_password(old_password):
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=ResponseInfo().format_response(
                    data={}, message='Passowrd incorrect',
                    status_code=status.HTTP_403_FORBIDDEN,
                )
            )

        user.set_password(new_password)
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data=ResponseInfo().format_response(
                data={}, message='Passowrd Updated',
                status_code=status.HTTP_200_OK,
            )
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
