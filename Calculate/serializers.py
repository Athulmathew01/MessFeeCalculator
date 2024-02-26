from rest_framework import serializers
from .models import Expenses

class ExpensesSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format='%Y-%m-%d')

    
    class Meta:
        model = Expenses
        fields = '__all__'  


