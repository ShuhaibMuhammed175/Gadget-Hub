import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .form import user_creation
from .models import Category, Product, Cart, Wishlist, Order, OrderDetail, Review

def check(request):
    pass

def home(request):
    all_products = Product.objects.all()

    return render(request, 'app/index.html',
                  {
                      'products': all_products
                  })


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=name, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('/')
            else:
                messages.warning(request, 'Invalid username or password')
                return redirect('login')
    return render(request, 'app/login.html')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logged out successfully')
        return redirect('/')


def register(request):
    form = user_creation()
    if request.method == 'POST':
        form = user_creation(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Successfull You can login now')
            return redirect('login')
    return render(request, 'app/register.html',
                  {
                      'form': form
                  })


def category(request):
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'app/category.html', context)


def category_products(request, category):
    if Category.objects.filter(name=category):
        products = Product.objects.filter(category__name=category)
        context = {
            'product_category': category,
            'products': products
        }
        print(context['products'])
        return render(request, 'app/category_products.html', context)

    else:
        messages.warning(request, 'No such category found')
        return redirect('category')


def fetch_product(request, product_id, product_category):
    if Category.objects.get(name=product_category):
        if Product.objects.get(id=product_id):
            product = Product.objects.get(id=product_id)
            print(product)
            review = Review.objects.filter(product=product)
            print(review)
            order = None
            if request.user.is_authenticated:
                order = Order.objects.filter(user=request.user, products=product_id, status='delivered')
                print(order)
            context = {
                'product': product,
                'review': review,
                'order': order
            }
            return render(request, 'app/product_details.html', context)
        else:
            messages.error(request, 'No such product found')
    else:
        messages.error(request, 'No such product found')
    return redirect('category')


@login_required(login_url='login')
def view_wish_list(request):
    if request.user.is_authenticated:
        wish_list = Wishlist.objects.filter(user=request.user)
        return render(request, 'app/wishlist.html', {
            'wish_list_products': wish_list
        })
    else:
        return redirect('/')


@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, status='cart')
        cart_total = 0
        for cart_item in cart:
            cart_total += cart_item.total_price()
        return render(request, 'app/cart.html',
                      {
                          'cart_items': cart,
                          'cart_total': cart_total
                      })
    else:
        return redirect('/')


@login_required(login_url='login')
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_id = data['pdt_id']
            quantity = data['product_qty']
            print(product_id)
            product = Product.objects.get(id=product_id)
            print(product)
            if product:
                if Cart.objects.filter(user=request.user.id, product=product_id, status='cart'):

                    return JsonResponse({'status': 'Already in Cart'}, status=200)
                else:
                    if product.quantity >= quantity:
                        Cart.objects.create(user_id=request.user.id, product_id=product_id, quantity=quantity,
                                            status='cart')
                        product.quantity -= quantity
                        product.save()
                        return JsonResponse({'status': 'Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Out of stock'}, status=200)
        else:
            return JsonResponse({'status': 'Login required'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)


@login_required(login_url='login')
def remove_from_cart(request, product_id):
    cart_product = Cart.objects.filter(user=request.user, product=product_id)
    product = Product.objects.get(id=product_id)
    product.quantity += 1
    product.save()
    cart_product.delete()
    return redirect('cart')


@login_required(login_url='login')
def wishlist(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_id = data['pdt_id']
            product = Product.objects.get(id=product_id)
            if product:
                if Wishlist.objects.filter(user=request.user, product_id=product_id):
                    return JsonResponse({'status': 'Already in wishlist'}, status=200)
                else:
                    Wishlist.objects.create(user=request.user, product_id=product_id)
                    return JsonResponse({'status': 'Added successfully'})
        else:
            return JsonResponse({'status': 'Login Required'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)


@login_required(login_url='login')
def remove_wish_list(request, product_id):
    wish_list_product = Wishlist.objects.filter(user=request.user, product=product_id)
    wish_list_product.delete()
    return redirect('view_wish_list')


def item_search(request):
    search = request.GET['search']
    all_products = Product.objects.filter(name__icontains=search)
    context = {
        'all_products': all_products,
        'search': search
    }
    return render(request, 'app/search_results/home_search.html', context)


@login_required(login_url='login')
def cart_item_search(request):
    search = request.GET['search']
    all_products = Cart.objects.filter(product__name__icontains=search, status='cart')
    context = {
        'all_products': all_products,
    }
    return render(request, 'app/search_results/cart_search.html', context)


@login_required(login_url='login')
def wish_list_item_search(request):
    search = request.GET['search']
    all_products = Wishlist.objects.filter(product__name__icontains=search)
    context = {
        'all_products': all_products,
    }
    return render(request, 'app/search_results/wishlist_search.html', context)


def category_search(request):
    search = request.GET['search']
    all_products = Category.objects.filter(name__icontains=search)
    context = {
        'all_products': all_products,
    }
    return render(request, 'app/search_results/category_search.html', context)


def category_products_search(request, category_name):
    search = request.GET['search']
    all_products = Product.objects.filter(name__icontains=search, category=category_name)
    print(all_products)
    context = {
        'all_products': all_products,
        'product_category': category_name
    }
    return render(request, 'app/search_results/category_products_search.html', context)


@login_required(login_url='login')
def checkout_page(request):
    products = Cart.objects.filter(user=request.user, status='cart')
    sub_total = 0
    sub_qty = 0
    for i in products:
        sub_total += i.total_price()
    for i in products:
        sub_qty += i.quantity
    context = {
        'products': products,
        'sub_total': sub_total,
        'sub_qty': sub_qty
    }
    return render(request, 'app/checkout.html', context)


@login_required(login_url='login')
def add_to_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        product_ids = data.get('product_ids')
        total_quantity = data.get('quantities')
        user = request.user

        if product_ids is None or total_quantity is None:
            response_data = {'message': 'Invalid data in the request'}
            return JsonResponse(response_data, status=400)

        order = Order(user=user, total_price=0)
        order.save()

        for product_id, quantity in zip(product_ids, total_quantity):
            product = get_object_or_404(Product, id=product_id)
            cart = Cart.objects.get(user=user, product=product, status='cart')
            cart.status = 'ordered'
            cart.save()

            order_detail = OrderDetail(user=user, order=order, product=product, quantity=quantity,
                                       price=product.new_price)
            order_detail.save()
            order.products.add(product)
            order.total_price += order_detail.subtotal()
            order.save()
        messages.success(request, 'Order placed successfully')
        response_data = {'message': 'Order updated successfully'}
        return JsonResponse(response_data)

    else:
        response_data = {'message': 'Invalid request method'}
        return JsonResponse(response_data, status=400)


def order_view(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        print(orders)
        context = {'orders': orders}
        return render(request, 'app/orders.html', context)
