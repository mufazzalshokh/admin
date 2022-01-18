from django import forms

from products.models import ColorModel, ProductModel, CategoryModel


class ProductForm(forms.ModelForm):
    # description = forms.CharField(CKEditorUploadingWidget())
    class Meta:
        model = ProductModel
        exclude = ['created_at', 'user', 'real_price']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        exclude = ['updated_at', 'created_at', 'user']


class ColorModelForm(forms.ModelForm):
    class Meta:
        model = ColorModel
        fields = '__all__'
        widgets = {
            'code': forms.TextInput(attrs={
                'type': 'color'
            })
        }
