from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Product
from helpers.dynamodb_helpers import get_item, put_item
from django.contrib import messages
from helpers.dynamodb_helpers import save_product
from django.shortcuts import render, redirect
from helpers.dynamodb_helpers import get_user_products
from helpers.dynamodb_helpers import delete_product_dynamodb
from helpers.dynamodb_helpers import save_product_with_file
from helpers.s3_helpers import upload_file
from boto3.dynamodb.conditions import Key
from warranty_lib.warranty import WarrantyValidator, WarrantyCoverageCalculator
from urllib.parse import unquote






@login_required
def create_product(request):
    # Extract product details from the form
    if request.method == 'POST':
        serial_number = request.POST.get('serial_number').strip()
        product_name = request.POST.get('product_name').strip()
        purchase_date = request.POST.get('purchase_date').strip()
        warranty_period = request.POST.get('warranty_period').strip()
        document = request.FILES.get('document')  # File upload
        
      # Validate form inputs
      
        if not serial_number or not product_name or not purchase_date or not warranty_period or not document:
            messages.error(request, "All fields including the document are required.")
            return redirect('create_product')

        try:
            # Upload file to S3
            
            file_key = f"warranty-documents/{serial_number}/{document.name}"
            file_url = upload_file(document, file_key)

            # Save product details in DynamoDB
            save_product_with_file(
                user_id=request.user.id,
                serial_number=serial_number,
                product_name=product_name,
                purchase_date=purchase_date,
                warranty_period=int(warranty_period),
                file_key=file_key  # Save file key in DynamoDB
            )

            messages.success(request, "Product registered successfully with the document.")
            return redirect('list_products')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('create_product')

    return render(request, 'registrations/create_product.html')
    
@login_required
def view_product(request, serial_number):
    
    # Fetch the product from the database using the serial number
    
    product = get_object_or_404(Product, serial_number=serial_number, user=request.user)
    return render(request, 'registrations/view_product.html', {'product': product})

@login_required
def list_products(request):
    """Displays all products registered by the logged-in user with warranty details."""
    try:
        # Fetch products for the logged-in user
        products = get_user_products(user_id=request.user.id)

        # # Add warranty information to each product
        for product in products:
            purchase_date = product.get("PurchaseDate")
            warranty_period = int(product.get("WarrantyPeriod", 0))

            # Use the WarrantyValidator and WarrantyCoverageCalculator from library
            validator = WarrantyValidator(purchase_date, warranty_period)
            calculator = WarrantyCoverageCalculator(purchase_date, warranty_period)

            product["is_under_warranty"] = validator.is_under_warranty()
            product["remaining_days"] = calculator.remaining_warranty()

        return render(request, "registrations/list_products.html", {"products": products})
    except Exception as e:
        return render(request, "registrations/list_products.html", {"error": str(e)})



@login_required
def delete_product(request, serial_number):
    
    try:
        # Delete the product using the helper function
        delete_product_dynamodb(user_id=request.user.id, serial_number=serial_number)
        messages.success(request, "Product deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the product: {str(e)}")
    
    # Redirect to the product list page after deletion
    return redirect('list_products')
    
    
@login_required
def delete_product_confirmation(request, serial_number):
    # Fetch the product details for confirmation
    from helpers.dynamodb_helpers import get_product
    print(f"Debug: Trying to fetch product USER#{request.user.id}, PRODUCT#{serial_number}")
    product = get_product(user_id=request.user.id, serial_number=serial_number)

    if not product:
        messages.error(request, "Product not found.")
        return redirect('list_products')  # Redirect to the product list if not found

    return render(request, 'registrations/delete_product_confirmation.html', {'product': product})
    
    def get_user_products(user_id):
        # Query DynamoDB for all products associated with the user
        try:
            response = table.query(
            KeyConditionExpression=Key('PK').eq(f"USER#{user_id}") &
                                   Key('SK').begins_with("PRODUCT#")
                                   )
            return response.get('Items', [])
        except Exception as e:
            print(f"Error retrieving products for user {user_id}: {e}")
        return []
        
