from urllib import request
from rest_framework import status
from rest_framework.response import Response #render redirect
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from haberler.models import Makale,Gazeteci
from haberler.api.serializers import MakaleSerializer,GazeteciSerializer

class GazeteciListCreateAPIView(APIView):
    def get(self,requset):
        yazarlar = Gazeteci.objects.all()
        serializer = GazeteciSerializer(yazarlar,many=True)
        return Response(serializer.data)    
    def post(self,request):
        serializer = GazeteciSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.errors,serializer.data,status=status.HTTP_201_CREATED)#herşey tamamsa http 201 gönderiyoruz
        
        return Response(status=status.HTTP_400_BAD_REQUEST)



class MakaleListCreateAPIView(APIView):
    def get(self,requset):
        makaleler = Makale.objects.filter(aktif=True)#Nesnelerden olluşan bir sorgu kümesi var
        serializer = MakaleSerializer(makaleler,many=True)
        return Response(serializer.data)    
    def post(self,request):
        serializer = MakaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.errors,serializer.data,status=status.HTTP_201_CREATED)#herşey tamamsa http 201 gönderiyoruz
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

class MakaleDetailAPIView(APIView):
    def get_object(self,pk):
        makale_instance = get_object_or_404(Makale,pk=pk)
        return makale_instance
    def get(self,request,pk):
        makale = self.get_object(pk=pk)
        serializer = MakaleSerializer(makale)
        return Response(serializer.data)

    def put(self,requset,pk):
        makale = self.get_object(pk=pk)

        serializer = MakaleSerializer(makale,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    def delete(self,requset,pk):
        makale = self.get_object(pk=pk)
        makale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# Fonksiyonel Method
# @api_view(['GET','POST'])#Get yada Post şeklinde bir request bekliyoruz
# def makale_list_create_api_view(request):
#     if request.method == 'GET':
#         makaleler = Makale.objects.filter(aktif=True)#Nesnelerden olluşan bir sorgu kümesi var
#         serializer = MakaleSerializer(makaleler,many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = MakaleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)#herşey tamamsa http 201 gönderiyoruz
        
#         return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def makale_detail_api_view(request,pk):
    try:
        makale_instance = Makale.objects.get(pk=pk)
    except Makale.DoesNotExist:
        return Response({
            "errors":{
                "code":404,
                "message":f"Böyle bir id ({pk}) ile ilgili makale bulunamadı"
            }
        },
        status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = MakaleSerializer(makale_instance)
        return Response(serializer.data)    
    elif request.method == "PUT":
        serializer = MakaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == "DELETE":
        makale_instance.delete()
        return Response(
            {
                 "errors":{
                "code":404,
                "message":f"Böyle bir id ({pk}) ile ilgili makale bulunamadı"
                }
            },
            status=status.HTTP_204_NO_CONTENT
        )