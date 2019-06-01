from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse

#class AdministratorViewSet(viewsets.ModelViewSet):

def homepage(request):
    return render(request, 'dist/index.html')
