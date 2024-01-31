from .serializer import AgriSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from precisionagri.models import Agriculture,ApiUser,User
from precisionagri.prediction import cropprediction
from rest_framework.renderers import TemplateHTMLRenderer
from django.utils.http import  urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib import messages

class CropApi(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'precisionagri/crop_form.html'
    def get(self,request,email,token):
        get_token = token
        try:
            dec_email=urlsafe_base64_decode(force_str(email)).decode()
            user = User.objects.get(email=dec_email)
            apiuser=ApiUser.objects.get(user=user.id)    
        except:
            return Response(messages.error(request,"Invalid User"),status=status.HTTP_400_BAD_REQUEST)
        if apiuser.apikey == get_token:
            serializer = AgriSerializer()
            return Response({'serializer': serializer},status=status.HTTP_200_OK)
        else:
            return Response(messages.error(request,"Invalid Token"),status=status.HTTP_400_BAD_REQUEST)
    def post(self,request,token,email):
        get_token = token
        try:
            dec_email=urlsafe_base64_decode(force_str(email)).decode()
            user = User.objects.get(email=dec_email)
            apiuser=ApiUser.objects.get(user=user.id)
        except:
            return Response(messages.error(request,"Invalid User"),status=status.HTTP_400_BAD_REQUEST)
        if apiuser.apikey == get_token:
            serializer = AgriSerializer(data = request.data)
            if serializer.is_valid():
                nit = serializer.data['Nitrogen']
                pho = serializer.data['Phosphorous']
                pot = serializer.data['Potassium']
                temp = serializer.data['Temperature']
                humidity = serializer.data['Humidity']
                ph = serializer.data['PH']
                rain = serializer.data['Rainfall']
                try:
                    store = Agriculture.objects.get(Nitrogen = nit, Phosphorous = pho, Potassium = pot, Temperature = temp, Humidity = humidity, PH = ph, Rainfall = rain)
                    crop = store.Crop_Label
                    return Response({'crop':crop},status=status.HTTP_200_OK)
                except:
                    result = cropprediction([nit,pho,pot,temp,humidity,ph,rain])
                    crop = Agriculture.objects.create(user = user ,Nitrogen = nit, Phosphorous = pho, Potassium = pot, Temperature = temp, Humidity = humidity, PH = ph, Rainfall = rain, Crop_Label = result)
                    crop.save()
                    return Response({'crop':result},status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(messages.error(request,"Invalid Token"),status=status.HTTP_400_BAD_REQUEST)