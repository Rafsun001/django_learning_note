from rest_framework import serializers
from .models import *

class RecipesSerializer(serializers.ModelSerializer):
    #email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = recipes
        fields = ("user","title","caterogy","description", "datetime")
        read_only_field =  ("user", "datetime")

class RecipesSerializer(serializers.ModelSerializer):
    #email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = recipes
        fields = ("user","title","caterogy","description", "datetime")
        read_only_field =  ("user", "datetime")

        
class IngredientSerializer(serializers.ModelSerializer):
    #email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = ingredient
        fields = ("recipie_id","ingredient_name","ammount","vitamin_contain")
        read_only_field =  ("recipie_id")
        
class InstructionSerializer(serializers.ModelSerializer):
    #email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = instruction
        fields = ("recipie_id","note")
        read_only_field =  ("recipie_id")


class ChefNoteSerializer(serializers.ModelSerializer):
    #email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = chefNote
        fields = ("recipie_id","note")
        read_only_field =  ("recipie_id")