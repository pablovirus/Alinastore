from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Category, Product, ProductImages, Order, OrderProduct, Customer
from .forms import PedidoForm, CustomUserCreateForm, ContactForm
from .misc_scripts import parser, compose_order_email, compose_contact_email
import datetime

def index(request):
    return render(request, 'index.html')

def productos(request):
    categories = Category.objects.all().order_by('name')
    products = Product.objects.all().order_by('name')
    product_rows = parser(products, 3)
    context = {
        'categories' : categories,
        'product_rows' : product_rows,
    }
    return render(request, 'store/productos.html', context=context)

def categoria(request, slug):
    categories = Category.objects.all().order_by('name')
    products = Product.objects.filter(category__exact=slug).order_by('name')
    product_rows = parser(products, 3)
    context = {
        'categories' : categories,
        'product_rows' : product_rows,
    }
    return render(request, 'store/productos.html', context=context)

def detalle(request, slug):
    product = Product.objects.filter(slug__exact=slug).first()
    secondary_images = ProductImages.objects.filter(product__exact=product)
    if product.discount_price:
        discount_percentage = 100 - int(
            (product.discount_price / product.price) * 100)
    else:
        discount_percentage = 0
    context = {
        'product' : product,
        'discount_percentage' : discount_percentage,
        'secondary_images' : secondary_images,
    }
    return render(request, 'store/detalle.html', context=context)

def about(request):
    return render(request, 'store/about.html')

def contacto(request):
    try:
        customer = request.user.customer
    except: 
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.clean()
            mailbody = compose_contact_email(name=form.name,telephone=form.telephone,
                email=form.email, comment=form.comment,
            )
            send_mail(
                subject= f'Consluta de {form.name}:' + f'{form.subject}',
                message= mailbody,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.RECIPIENT_ADDRESS])
            return render(request, 'store/consultaok.html')
        else:
            form = ContactForm(request.POST)
            context = {'form' : form}
            return render(request, 'store/contacto.html', context)
    else:
        form = ContactForm(
            initial={'email': customer.email, 'name': customer.name,
            'telephone':customer.telephone}            
        )
        context = {'form' : form}
        return render(request, 'store/contacto.html', context)

def consultaok(request):
    return render(request, 'store/consultaok.html')

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    try:
        customer = request.user.customer
    except: 
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, order_created = Order.objects.get_or_create(
        customer=customer, ordered=False)
    order_item, item_created = OrderProduct.objects.get_or_create(
        item = product,
        order = order,
    )
    if not item_created:
        order_item.quantity += 1
        order_item.save()

    messages.info(request, '¡El producto se agrego al carrito!')

    return redirect('detalle', slug=slug)

def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    try:
        customer = request.user.customer
    except: 
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order_query = Order.objects.filter(customer=customer, ordered=False)
    if order_query.exists():
        order = order_query[0]
        if order.orderproduct_set.filter(item__slug=product.slug).exists():
            order_item, created = OrderProduct.objects.get_or_create(
                item = product,
            )
            order_item.delete()
            messages.info(request, 'El producto se quitó del carrito.')
        else:
            messages.info(request, 'Tu carrito no contiene este producto.')
    else:
        messages.info(request, 'Tu carrito está vacío.')
    return redirect('detalle', slug=slug)

def add_to_cart_from_product_list(request, slug):
    product = get_object_or_404(Product, slug=slug)
    try:
        customer = request.user.customer
    except: 
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, order_created = Order.objects.get_or_create(
        customer=customer, ordered=False)
    order_item, item_created = OrderProduct.objects.get_or_create(
        item = product,
        order = order,
    )
    if not item_created:
        order_item.quantity += 1
        order_item.save()

    messages.info(request, '¡El producto se agrego al carrito!')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def carrito(request):
    try:
        customer = request.user.customer
    except: 
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, ordered=False)
    order_products = order.orderproduct_set.all()
    price_n_quant = [(product.item.price, product.quantity) for product in order_products]
    total_cost = sum([tupl[0] * tupl[1] for tupl in price_n_quant])
 
    if request.method == 'GET':
        pedidoform = PedidoForm(
            initial={'email': customer.email, 'name': customer.name,
            'telephone':customer.telephone}
        )
        context = {
            'order_products' : order_products,
            'total_cost' : total_cost,
            'pedidoform' : pedidoform,
        }
        return render(request, 'store/cart.html', context=context)

    elif request.method == 'POST':
        pedidoform = PedidoForm(request.POST)
        if pedidoform.is_valid():
            pedidoform.clean()
            mailbody = compose_order_email(order=order, order_products=order_products,
                customer=customer,name=pedidoform.name,telephone=pedidoform.telephone,
                email=pedidoform.email, comment=pedidoform.comment, total_cost=total_cost
            )
            send_mail(
                subject= f'Orden {order.id} pedida por {customer}',
                message= mailbody,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.RECIPIENT_ADDRESS])
            order.ordered = True
            order.ordered_date = datetime.datetime.now()
            order.final_price = total_cost
            order.save()
            return redirect('pedidook')
        else:
            context = {
                'order_products' : order_products,
                'total_cost' : total_cost,
                'pedidoform' : pedidoform,
            }
        return render(request, 'store/cart.html', context=context)
    else:
        return render(request, 'store/cart.html', context=context)


def decrease_quantity(request, slug):
    product = get_object_or_404(Product, slug=slug)
    try:
        customer = request.user.customer
    except: 
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, ordered=False)
    if order.orderproduct_set.filter(item__slug=product.slug).exists():
        order_item, created = OrderProduct.objects.get_or_create(
            item = product,
            order = order,
        )
        order_item.quantity -= 1
        if order_item.quantity <= 0:
            order_item.delete()
        else:
            order_item.save()
        messages.info(request, 'La cantidad se redujo.')
    else:
        messages.info(request, 'Tu carrito no contiene este producto.')
    return redirect('carrito')

def increase_quantity(request, slug):
    product = get_object_or_404(Product, slug=slug)
    try:
        customer = request.user.customer
    except: 
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, ordered=False)
    if order.orderproduct_set.filter(item__slug=product.slug).exists():
        order_item, created = OrderProduct.objects.get_or_create(
            item = product,
            order = order,
        )
        order_item.quantity += 1
        order_item.save()
        messages.info(request, 'La cantidad se incrementó.')
    else:
        messages.info(request, 'Tu carrito no contiene este producto.')
    return redirect('carrito')

def pedido_ok(request):
    return render(request, 'store/pedidook.html')

def pedidos(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer,ordered=True)
    context = {
                'orders' : orders,
            }
    return render(request, 'store/pedidos.html', context)

def pedido_detalle(request, orderid): #TODO: Pedido Detalle??
    pass 


# Authentication and registration views 

def register(request):
    if request.method == 'POST':
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            customer = Customer.objects.create(
                user=user, email=user.email, name=user.username, 
                telephone=form.cleaned_data['telephone']
            )
            return redirect('index')
        else: 
            messages.error(
                request, "Algo salió mal, por favor verifica los datos proporcionados")
    form = CustomUserCreateForm()
    context = {
        'form' : form,
    }
    return render(request, 'registration/register.html', context)

class ContextLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

class ContextLogoutView(auth_views.LogoutView):
    template_name = 'registration/logout.html'
    next_page = reverse_lazy('index')

class ContextPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'

class ContextPasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class ContextPasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'

class ContextPasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


 