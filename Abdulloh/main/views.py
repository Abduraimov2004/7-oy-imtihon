from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Comment
from .book import Book
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def product_list(request):
    category = request.GET.get('category')
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all().order_by('-created_at')

    if category:
        products = products.filter(category__name=category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        )

    categories = Category.objects.all()

    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'min_price': min_price,
        'max_price': max_price
    })



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = product.comments.all()
    images = product.images.all()
    category_products = Product.objects.filter(category=product.category).exclude(id=product_id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        Comment.objects.create(product=product, user=request.user, text=comment_text)
        return redirect('product_detail', product_id=product_id)

    if not request.session.get(f'viewed_product_{product_id}', False):
        product.views += 1
        product.save()
        request.session[f'viewed_product_{product_id}'] = True

    return render(request, 'product.html', {
        'product': product,
        'comments': comments,
        'images': images,
        'category_products': category_products
    })


def add_comment(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        text = request.POST.get('text')
        rating = request.POST.get('rating')
        user = request.user

        Comment.objects.create(
            product=product,
            user=user,
            text=text,
            rating=rating
        )
        return redirect('product_detail', product_id=product.id)



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
            return redirect('product_list')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('account')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


@login_required
def account_view(request):
    return render(request, 'account.html')
