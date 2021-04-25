from django.shortcuts import get_object_or_404
from django.db.models import DecimalField, ExpressionWrapper, F, Sum, PositiveIntegerField
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .serializers import WarehouseStocksSerializer
from .models import WarehouseStocks

# Create your views here.

class WarehouseStocksView(APIView):
    cost_field = ExpressionWrapper(F("price") * F("amount"),
                                   output_field=DecimalField(max_digits=8, decimal_places=2))

    def get(self, request):
        queryset_with_cost_field = WarehouseStocks.objects.annotate(cost=self.cost_field)
        warehouse_stocks = list(queryset_with_cost_field.values())
        return Response({"resources": warehouse_stocks, "total_count": len(warehouse_stocks)})

    def post(self, request):
        serializer = WarehouseStocksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_stock = WarehouseStocks.objects.create(**serializer.validated_data)
        return Response(model_to_dict(new_stock, exclude=['id']))

    def put(self, request):
        serializer = WarehouseStocksSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        params = serializer.validated_data
        stock = get_object_or_404(WarehouseStocks, pk=params.pop('id'))
        stock.__dict__.update(**params)
        stock.save()
        return Response()

    def delete(self, request):
        _id = request.query_params['id']
        stock = get_object_or_404(WarehouseStocks, pk=_id)
        stock.delete()
        return Response()

def index(request):
    return HttpResponse("<h1>200 OK</h1>")

def total_cost(request):
    sum_with_default = Coalesce(Sum(WarehouseStocksView.cost_field), 0, output_field=PositiveIntegerField())
    _total_cost = WarehouseStocks.objects.aggregate(total_cost=sum_with_default)
    return JsonResponse(_total_cost)


