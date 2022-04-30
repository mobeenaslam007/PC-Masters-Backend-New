from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from ..serializers import ImageSerializer, ProductSerializer
from ..models import Product, ProductImage


@api_view(["GET"])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)

    data = []
    for product in products:

        images = ProductImage.objects.filter(product=product)
        image_serializer = ImageSerializer(images, many=True)
        images = ["http://localhost:8000"+x["images"]
                  for x in image_serializer.data]
        product_serializer = ProductSerializer(product, many=False)
        product_data = product_serializer.data
        product_data["image"] = (
            "http://localhost:8000"+product_data["image"]).split(sep=None) + images
        product_data["id"] = product_data["_id"]
        del product_data["_id"]
        product_data["title"] = product_data["name"]
        del product_data["name"]

        data.append(product_data)

    return Response(data)
