from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        
        # Best Practice: Explicitly list fields instead of using '__all__'.
        # This prevents accidentally exposing fields you don't want the user to edit, like 'created_at'.
        fields = [
            'product_name',
            'description',
            'category',
            'suppliers',
            'stock_quantity',
            'expire_date'
        ]

        # Use the 'widgets' dictionary to assign attributes to form fields.
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Apple iPhone 15'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4, # Makes the text area a bit taller than the default
                'placeholder': 'Enter a detailed description of the product...'
            }),
            # 'form-select' is Bootstrap's class for dropdowns.
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'suppliers': forms.SelectMultiple(attrs={
                'class': 'form-select'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0' # Prevents entering negative numbers in the browser
            }),
            # Using 'type': 'date' activates the browser's native date picker UI.
            'expire_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        
        # (Optional but Recommended) Customize field labels
        labels = {
            'product_name': 'Product Name',
            'stock_quantity': 'Quantity in Stock',
            'expire_date': 'Expiry Date (if applicable)',
        }

        # (Optional but Recommended) Add help text below fields
        help_texts = {
            'suppliers': 'You can select multiple suppliers by holding Ctrl (or Cmd on Mac) and clicking.',
            'expire_date': 'Leave blank if the product does not expire.',
        }