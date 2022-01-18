from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from products.form import ProductForm, CategoryForm
from products.models import ProductModel


class ProductTemplateView(TemplateView):
    template_name = 'admin_index.html'


class ProductCreateView(CreateView):
    template_name = 'admin_products.html'
    form_class = ProductForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(reverse('menu:create'))

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['category'] = self.request.user.category.order_by('-pk')
        context['products'] = self.request.user.restaurant.order_by('-pk')
        return context


class AdminProductsListView(ListView):
    template_name = 'admin_list.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        qs = ProductModel.objects.all()

        if q:
            return qs.filter(name_icontains=q).order_by('-pk')
        else:
            return qs.filter(user=self.request.user).order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.request.user.category.order_by('-pk')
        context['products'] = self.request.user.products.order_by('-pk')

        return context


def ProductDelete(request):
    cat = request.POST.getlist('option')
    for i in cat:
        ProductModel.objects.get(id=i).delete()
        return HttpResponseRedirect(reverse('products:list'))


class ProductUpdateView(UpdateView):
    template_name = 'admin_list.html'
    form_class = ProductForm
    model = ProductModel

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(self.request.GET.get('next'))


class CategoryListView(ListView):
    template_name = 'admin_category.html'
    paginate_by = 5

    def get_queryset(self):
        return ProductModel.objects.order_by('-pk')


def CategoryDelete(request):
    cat = request.POST.getlist('option')
    for i in cat:
        ProductModel.objects.get(id=i).delete()
        return HttpResponseRedirect(reverse('products:category'))


class CategoryCreateView(CreateView):
    template_name = 'admin_category.html'
    form_class = CategoryForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(reverse('products:category'))





# def products_list(request):
#     products = ['a', 'b', 'c']
#     context = {
#         'products': products
#     }
#     return render(request, 'admin_index.html', context)
