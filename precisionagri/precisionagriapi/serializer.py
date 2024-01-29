from rest_framework import serializers
from precisionagri.models import Agriculture


class AgriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agriculture
        exclude = ['user','Crop_Label','date']
    
    def validate_Nitrogen(self,value):
        if value > 0:
            return value
        else:
            raise serializers.ValidationError("Value must be greater than zero.") 
    def validate_Phosphorous(self,value):
        if value > 0:
            return value
        else:
            raise serializers.ValidationError("Value must be greater than zero.") 
    def validate_Potassium(self,value):
        if value > 0:
            return value
        else:
            raise serializers.ValidationError("Value must be greater than zero.") 
    def validate_Temperature(self,value):
        if value > 0:
            return value
        else:
            raise serializers.ValidationError("Value must be greater than zero.") 
    def validate_Humidity(self,value):
        if value > 0:
            return value
        else:
            raise serializers.ValidationError("Value must be greater than zero.") 
    def validate_PH(self,value):
        if value > 0:
            return value
        else:
            raise serializers.ValidationError("Value must be greater than zero.") 
    def validate_Rainfall(self,value):
        if value > 0:
            return value
        else:
            raise serializers.ValidationError("Value must be greater than zero.") 
    