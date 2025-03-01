from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from ecommerce.forms import CustomerModelForm, ProductModelForm
from ecommerce.models import Product, ProductAttribute, Customer


# Create your views here.


def index(request):
    search_query = request.GET.get('q', '')
    products = Product.objects.all().order_by('id')
    product_attributes = ProductAttribute.objects.filter()
    if search_query:
        products = products.filter(name__icontains=search_query)
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'products': products,
    }
    return render(request, 'ecommerce/product-list.html', context=context)


def grid(request):
    return render(request, 'ecommerce/product-grid.html')


def product_detail(request, pk):
    products = Product.objects.all().filter(pk=pk)

    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
        'produuucts': products,
    }
    return render(request, 'ecommerce/product-details.html', context)


def customers(request):
    search_query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', '')

    if filter_type == 'filter':
        customers = Customer.objects.all().order_by('name')
    else:
        customers = Customer.objects.all().order_by('-id')

    if search_query:
        customers = customers.filter(name__icontains=search_query)
    context = {
        'customers': customers
    }
    return render(request, 'ecommerce/customers.html', context=context)


def customers_detail(request, pk):
    customers = get_object_or_404(Customer, pk=pk)
    cUstomers = Customer.objects.all().filter(pk=pk)
    context = {
        'customers': customers,
        'cUstomers': cUstomers,
    }

    return render(request, 'ecommerce/customer-details.html', context=context)


def customer_create(request):
    form = CustomerModelForm()
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')
    else:
        form = CustomerModelForm()
    context = {
        'form': form,
    }
    return render(request, 'ecommerce/creat.html', context=context)


def product_create(request):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductModelForm()
    context = {
        'form': form,
    }

    return render(request, 'ecommerce/create_product.html', context=context)


from django.views.generic import ListView, View, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy


class ProductListView(ListView):
    model = Product
    template_name = 'ecommerce/product-list.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        queryset = Product.objects.all().order_by('id')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_attributes'] = ProductAttribute.objects.all()
        return context


class Grid(View):
    template_name = 'ecommerce/product-grid.html'
    def get(self, request):
        return render(request, self.template_name)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'ecommerce/product-details.html'
    context_object_name = 'product'  # HTML ichida product sifatida ishlatish uchun

    def get_context_data(self, **kwargs):
        """Qo‘shimcha ma’lumotlar qo‘shish."""
        context = super().get_context_data(**kwargs)
        context['produuucts'] = Product.objects.all()  # Barcha mahsulotlar
        return context

class CustomerListView(ListView):
    model = Customer
    template_name = 'ecommerce/customers.html'
    context_object_name = 'customers'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        filter_type = self.request.GET.get('filter', '')

        if filter_type == 'filter':
            customers = Customer.objects.all().order_by('name')
        else:
            customers = Customer.objects.all().order_by('-id')

        if search_query:
            customers = customers.filter(name__icontains=search_query)

        return customers


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'ecommerce/customer-details.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cUstomers'] = Customer.objects.all()
        return context


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerModelForm
    template_name = 'ecommerce/creat.html'
    success_url = reverse_lazy('ecommerce:customers')


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductModelForm
    template_name = 'ecommerce/creat.html'
    success_url = reverse_lazy('ecommerce:index')
