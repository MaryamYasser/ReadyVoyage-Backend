from rest_framework import serializers

from .models import Account

class AccountSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'username',
                  'password', 'date_of_birth', 'date_created','photo')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)



