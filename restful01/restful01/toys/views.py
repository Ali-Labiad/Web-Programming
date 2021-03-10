from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from toys.models import Toy
from toys.serializers import ToySerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response 

# Create your views here.
'''
class JSONResponse(HttpResponse):
    def __init__(self,data,**kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse , self).__init__(content,**kwargs)
'''
@api_view(['GET' ,'POST'])
def toy_list(request):
    if request.method == 'GET':
        toys = Toy.objects.all()
        toys_serializer = ToySerializer(toys, many=True)
        return Response(toys_serializer.data)
    
    elif request.method == 'POST':
        toy_serializer = ToySerializer(data=request.data)
        if toy_serializer.is_valid:
            toys_serializer.save()
            return Response(toys_serializer.data,status=status.HTTP_201_CREATED)
        return Response(toy_serializer.errors , status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE']) 
def toy_detail(request, pk):     
    
    try:        
        toy = Toy.objects.get(pk=pk)     
    except Toy.DoesNotExist:         
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)      

    if request.method == 'GET':         
        toy_serializer = ToySerializer(toy)         
        return Response(toy_serializer.data)

    elif request.method == 'PUT':         
        toy_serializer = ToySerializer(toy, data=request.data)         
        if toy_serializer.is_valid():             
            toy_serializer.save()             
            return Response(toy_serializer.data)         
        return Response(toy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)      

    elif request.method == 'DELETE':         
        toy.delete()         
        return HttpResponse(status=status.HTTP_204_NO_CONTENT) 

    
    