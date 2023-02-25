from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from dj_rest_auth.serializers import TokenSerializer

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,  # email default required değildi, onu değiştirdik, artık zorunlu alan
        validators=[UniqueValidator(queryset=User.objects.all())]  # email uniq olsun, değilse validation error dönsün onun için ekledik ve yukarıda import ettik (UniqueValidator)
        )
    password = serializers.CharField(
        write_only = True,  # write_only sadece POST, PUT için kullan, GET(yani read) yapılırsa kullanma
        required = True,
        validators = [validate_password],
        style = {"input_type" : "password"}
    )
    password2 = serializers.CharField(
        write_only = True,
        required = True,
        style = {"input_type" : "password"}
    )
    
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
        ]
    
    #! Object level validation
    def validate(self, data):  # data gelen objenin tamamı yani user instance ı
        if data["password"] !=data["password2"]:
            raise serializers.ValidationError(
                {"message": "Password fields didn't match!"}
            )
        return data
    
    #! Creating User
    #? ModelSerializer kullanınca create metodu yazmaya gerek yok aslında fakat, User model içinde olmayan bir field 
    #? (password2) kullandığımız için creat metodunu override etmek gerekli;
    def create(self, validated_data):
        password = validated_data.get("password")
        validated_data.pop("password2")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        return user

class UserTokenSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email"
        )

class CustomTokenSerializer(TokenSerializer):

    user = UserTokenSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ("key", "user")


#* login/logout ---> dj-rest-auth

