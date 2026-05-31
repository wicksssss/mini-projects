from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category, Brand
from django.http import Http404


class StockCheckMixin:
    def dispatch(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs.get('slug'))
        if not product.is_available():
            raise Http404("Product is not available")
        return super().dispatch(request, *args, **kwargs)


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True, stock__gt=0)
        category_slug = self.request.GET.get('category')
        brand_slug = self.request.GET.get('brand')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        sort = self.request.GET.get('sort')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if brand_slug:
            queryset = queryset.filter(brand__slug=brand_slug)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        sort_map = {
            'price_asc': 'price',
            'price_desc': '-price',
            'new': '-created_at',
        }
        if sort in sort_map:
            queryset = queryset.order_by(sort_map[sort])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['brands'] = Brand.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(pk=self.object.pk)[:4]
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(is_active=True)
    