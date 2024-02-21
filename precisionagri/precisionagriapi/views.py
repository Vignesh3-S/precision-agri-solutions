from .serializer import AgriSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from precisionagri.models import Agriculture,ApiUser,User
from precisionagri.prediction import cropprediction
from django.utils.http import  urlsafe_base64_decode
from django.utils.encoding import force_str

class CropApi(APIView):
    def post(self,request,token,email):
        get_token = token
        try:
            dec_email=urlsafe_base64_decode(force_str(email)).decode()
            user = User.objects.get(email=dec_email)
            apiuser=ApiUser.objects.get(user=user.id)
        except:
            return Response({"error":"Invalid User"},status=status.HTTP_400_BAD_REQUEST)
        if apiuser.apikey == get_token:
            nit = request.POST['nitrogen']
            pho = request.POST['phosphorus']
            pot = request.POST['potassium']
            temp = request.POST['temperature']
            humidity = request.POST['humidity']
            ph = request.POST['ph']
            rain = request.POST['rainfall']
            try:
                store = Agriculture.objects.get(Nitrogen = nit, Phosphorous = pho, Potassium = pot, Temperature = temp, Humidity = humidity, PH = ph, Rainfall = rain)
                crop = store.Crop_Label
                serialize_store= AgriSerializer(store)
                return Response({"value":serialize_store.data,'crop':crop},status=status.HTTP_200_OK)
            except:
                result = cropprediction([nit,pho,pot,temp,humidity,ph,rain])
                crop = Agriculture.objects.create(user = user ,Nitrogen = nit, Phosphorous = pho, Potassium = pot, Temperature = temp, Humidity = humidity, PH = ph, Rainfall = rain, Crop_Label = result)
                crop.save()
                return Response({'crop':result,'n':nit,'p':pho,'k':pot,'t':temp,'h':humidity,'ph':ph,'r':rain},status=status.HTTP_200_OK)
        else:
            return Response({"error":"Invalid Token"},status=status.HTTP_400_BAD_REQUEST)