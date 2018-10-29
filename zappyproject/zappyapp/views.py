from django.shortcuts import render,reverse
from django.contrib.auth.forms import UserCreationForm
from zappyapp.models import Product,Customer,Cart
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from zappyapp.forms import CustomerUpdate
from django.db.models import Q
# Create your views here.


def home(request):
    products=Product.objects.all()
    return render(request,'zappyapp/home.html',{'products':products})

def rte(request):
    products=Product.objects.filter(cat_choice='rte')
    return render(request,'zappyapp/rte.html',{'products':products})

def rtc(request):
    products=Product.objects.filter(cat_choice='rtc')
    return render(request,'zappyapp/rtc.html',{'products':products})


def registration(request):
    sform=UserCreationForm(request.POST or None)
    if sform.is_valid():
        new_user=sform.save()
        return HttpResponseRedirect(reverse('zappyapp:home'))

    return render(request,'zappyapp/registration.html',{'sform':sform})

@login_required
def profile(request):
    return render(request, 'zappyapp/profile.html')


@login_required
def cprofile(request):
    if request.method == 'POST':
        cu_form = CustomerUpdate(request.POST,request.FILES,instance=request.user.customer)
        if cu_form.is_valid():
            cu_form.save()
            return HttpResponseRedirect(reverse('zappyapp:profile'))
    else:
        cu_form = CustomerUpdate(request.POST,request.FILES,instance=request.user.customer)
    return render(request, 'zappyapp/cprofile.html',{'cu_form':cu_form})


def productsdetails(request,id):
    products=Product.objects.get(id=id)

    dict={'products':products}
    return render(request,'zappyapp/productdetails.html',context=dict)

def search(request):
    query=request.GET.get('q',None)
    if query is not None:
        query2= Q(pname__iexact=query) | Q(description__icontains=query)
        products=Product.objects.filter(query2).distinct()

        return render(request,'zappyapp/home.html',{'products':products})
    else:
        return HttpResponseRedirect(reverse('zappyapp:home'))


def cart_home(request):
    cart_obj, new_obj=Cart.objects.new_or_get(request)
    products=cart_obj.products.all()
    total=0
    for x in products:
        total+=x.price
    return render(request,'zappyapp/cart.html')#,{'val':val}

def cart_update(request):
    id=request.POST.get('product_id')
    print(id)
    if id is not None:
        try:
            id=Product.objects.get(id=id)
        except Product.DoesNotExist:
            print('no product')
            return redirect("zappyapp:cart")
        if id in cart_obj.products.all():
            cart_obj.products.remove(id)
        else:
            cart_obj.products.add(id)
    products=Product.objects.get(id=id)
    return render(request,'zappyapp/productdetails.html',{'products':products})
