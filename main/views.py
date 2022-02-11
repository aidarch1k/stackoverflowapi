# from django.shortcuts import render
#
# # Create your views here.
# from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
#
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthorPermission
from .models import *
from .serializers import ProblemaSerializer, ReplySerializer, CommentSerializer


#
class PermissionMixin:
    def get_permissions(self):
        if self.action in['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission]
        elif self.action == 'create':
            permissions = [IsAuthenticated]
        else:
            permissions = []
        return [permission() for permission in permissions]
class ProblemViewSet(PermissionMixin,ModelViewSet):
    queryset = Problema.objects.all()
    serializer_class = ProblemaSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(detail=False, methods=['get'])
    def search(self,request):
        query = request.query_params.get('q')
        queryset = self.get_queryset().filter(Q(title__icontains=query) | Q(description__icontains=query))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)



class ReplyViewSet(PermissionMixin,ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context
    @action(detail=True, methods=['get'])
    def like(self,request,pk):
        user = request.user
        reply = get_object_or_404(Reply, pk=pk)
        if user.is_authenticated:
            if user in reply.likes.all():
                reply.likes.remove(user)
                message='UnLiked'
            else:
                reply.likes.add(user)
                message = 'Liked'
        context = {'Status': message}
        return Response(context, status=200)



class CommentViewSet(PermissionMixin,ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
# class ProductDetailView(RetrieveAPIView):
#     queryset = Problema.objects.all()
#     serializer_class = ProblemaSerializer
#
# class ProblemCreateView(CreateAPIView):
#     queryset = Problema.objects.all()
#     serializer_class = ProblemaSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
# class ProblemaUpdateView(UpdateAPIView):
#     queryset = Problema.objects.all()
#     serializer_class = ProblemaSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
# class ProblemaDeleteView(DestroyAPIView):
#     queryset = Problema.objects.all()
#     serializer_class = ProblemaSerializer
#
