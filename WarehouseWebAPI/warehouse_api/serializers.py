from rest_framework import serializers

class WarehouseStocksSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1, required=False)
    title = serializers.CharField(max_length=40, allow_blank=False, required=True)
    amount = serializers.FloatField()
    unit = serializers.CharField(max_length=20, allow_blank=False, required=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    date = serializers.DateField()


