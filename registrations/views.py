from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from .dynamodb_helpers import get_product, get_claims_for_product, delete_product_dynamodb
from .s3_helpers import upload_document, get_document_url

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
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
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def view_product(request, serial_number):
    product = get_product(request.user.id, serial_number)
    if product:
        return JsonResponse(product)
    return JsonResponse({'error': 'Product not found'}, status=404)

@csrf_exempt
def delete_product(request, serial_number):
    product = get_product(request.user.id, serial_number)
    if product:
        delete_product_dynamodb(request.user.id, serial_number)
        return JsonResponse({'status': 'Product deleted successfully'})
    return JsonResponse({'error': 'Product not found'}, status=404)

@csrf_exempt
def upload_receipt(request):
    if request.method == 'POST' and 'receipt' in request.FILES:
        try:
            file = request.FILES['receipt']
            user_id = request.user.id
            serial_number = request.POST.get('serial_number')
            object_key = f"{user_id}/{serial_number}/{file.name}"

            # Upload the file to S3
            upload_document(file, 'warranty-documents', object_key)

            # Generate a presigned URL
            download_url = get_document_url('warranty-documents', object_key)
            return JsonResponse({'status': 'Document uploaded successfully', 'url': download_url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
