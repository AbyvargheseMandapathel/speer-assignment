from rest_framework import generics, permissions , status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import Note , CustomUser
from .serializers import NoteSerializer , SignUpSerializer , LoginSerializer
from rest_framework.authentication import TokenAuthentication


User = get_user_model()

class UserSignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})
    
class UserLoginView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        token , created = Token.objects.get_or_create(user=user)
        return Response({'token':token.key})
    
class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    search_fields = ['title', 'content']
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        return super().create(request, *args, **kwargs)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        return Response({"message": f"Note updated by user: {self.request.user.username}"}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        response = super().put(request, *args, **kwargs)
        return Response({"status": response.status_code, "info": f"Note with ID {kwargs['pk']} updated by user: {self.request.user.username}"})

    def perform_destroy(self, instance):
        instance.delete()
        return Response({"message": f"Note deleted by user: {self.request.user.username}"}, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({"status": response.status_code, "info": f"Note with ID {kwargs['pk']} deleted by user: {self.request.user.username}"})