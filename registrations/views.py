from django.http import JsonResponse
from .models import Product
from .dynamodb_helpers import get_product, get_claims_for_product

def create_product(request):
    if request.method == 'POST':
        product = Product(
            user=request.user,
            serial_number=request.POST.get('serial_number'),
            purchase_date=request.POST.get('purchase_date'),
            warranty_period=request.POST.get('warranty_period'),
            product_name=request.POST.get('product_name'),
            description=request.POST.get('description')
        )
        product.save()
        return JsonResponse({'status': 'Product created successfully'})

def view_product(request, serial_number):
    product = get_product(serial_number)
    return JsonResponse(product)

def delete_product(request, serial_number):
    product = get_product(serial_number)
    if product:
        table.delete_item(Key={'PK': product['PK'], 'SK': product['SK']})
        return JsonResponse({'status': 'Product deleted successfully'})
    return JsonResponse({'error': 'Product not found'}, status=404)
