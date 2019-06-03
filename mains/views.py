from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from .serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response  import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
import jwt
from datetime import datetime
from django.http import Http404

class UserList(APIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username = username)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, username):
        user = self.get_object(username)
        if user.check_password(request.data['password']):
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token), 'username': user.username, 'nickname': user.first_name }, status=status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, username):
        user = self.get_object(username)
        if user.check_password(request.data['password']):
            user.set_password(request.data['new_password'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)   

class ProfileDetail(APIView):
    
    def get(self, request, username):
        user = User.objects.get(username = username)
        profile = Profile.objects.get(user = user)
        return Response({'weight': profile.weight})

    def patch(self, request, username):
        user = User.objects.get(username = username)
        profile = Profile.objects.get(user = user)
        serializer = ProfileSerializer(profile, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
class UserNick(APIView):
    def get(self, name,pk):
        try:
            user = User.objects.get(pk = pk)
        except User.DoesNotExist:
            return Response({'nickname': '알수없음'}, status = status.HTTP_404_NOT_FOUND)
        return Response({'nickname': user.first_name}, status = status.HTTP_200_OK)

class TipViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def list(self, request):
        queryset = Tip.objects.all()
        l = []
        for n in range(0, len(queryset)):
            l.append({ 'id': queryset[n].id, 'user': queryset[n].user.first_name, 'content': queryset[n].content, 'date': queryset[n].date})
        return Response(l)

    def create(self, request):
        token = request.META['HTTP_AUTHORIZATION'].split()
        token = jwt.decode(token[1], verify=False)
        data = {'content': request.data['content'], 'user': token['user_id']}
        serializer = TipSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # def destory(self, request, pk=None):
    #     try:
    #         tip = Tip.objects.get(pk = pk)
    #     except Scrap.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     tip.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class WaterList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, year, month):
        token = request.META['HTTP_AUTHORIZATION'].split()
        token = jwt.decode(token[1], verify=False)
        date = year+'-'+month+'-'
        waters = Water.objects.filter(user_id = token['user_id'], date__iregex = date+r'[0-9][0-9]')
        waters_data = []
        for n in range(0, len(waters)):
            waters_data.append({
                'date' : waters[n].date.day,
                'liters' : waters[n].liters,
                'titration_liters' : waters[n].titration_liters,
                'success' : waters[n].success 
            })
        return Response(waters_data)
    

class WaterDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, user):
        dt = datetime.now()
        date = dt.strftime('%Y-%m-%d')
        try:
            return Water.objects.get(date = date, user=user)
        except Water.DoesNotExist:
            userobject = User.objects.get(pk = user)
            return Water.objects.create(user=userobject, titration_liters = int(userobject.profile.weight)*33)
        except Water.MultipleObjectsReturned:
            return Water.objects.filter(user = user).order_by('id').first()
        
    def get(self, request):
        token = request.META['HTTP_AUTHORIZATION'].split()
        token = jwt.decode(token[1], verify=False)
        water = self.get_object(token['user_id'])
        serializer = WaterSerializer(water)
        return Response(serializer.data)

    def patch(self, request):
        token = request.META['HTTP_AUTHORIZATION'].split()
        token = jwt.decode(token[1], verify=False)
        water = self.get_object(token['user_id'])
        data = { 'liters' : request.data['liters']}
        if water.titration_liters <= int(request.data['liters']):
            data['success'] = True
        serializer = WaterSerializer(water, data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScrapViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,) 

    def list(self, request):
        token = request.META['HTTP_AUTHORIZATION'].split()
        token = jwt.decode(token[1], verify=False)
        queryset = Scrap.objects.filter(user=token['user_id'])
        serializer = ScrapSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        token = request.META['HTTP_AUTHORIZATION'].split()
        token = jwt.decode(token[1], verify=False)
        scrap = Scrap.objects.create(user = User.objects.get(pk = token['user_id']), tip=Tip.objects.get(pk = request.data['tip']))
        serializer = ScrapSerializer(scrap)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            scrap = Scrap.objects.get(pk = pk)
        except Scrap.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        scrap.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)