from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save,m2m_changed
from PIL import Image
# Create your models here.

class Product(models.Model):
    categories=(('rte','Ready To Eat'),('rtc','Ready To Cook'))
    cat_choice=models.CharField(max_length=20,choices=categories,default='rte')
    pname=models.CharField(max_length=200)
    image=models.ImageField(upload_to='Products',default='Products/default1.jpg')
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.pname



    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (1024, 768)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse("products:id",kwrgs={'id':self.id})




class Customer(models.Model):
    customer=models.OneToOneField(User,on_delete=models.CASCADE)
    cust_address=models.CharField(max_length=400)
    mobile = models.CharField(max_length=12)
    images = models.ImageField(upload_to='Customers',default='Customers/default.jpg')

    def __str__(self):
        return self.customer

class Order(models.Model):
    pid=models.ForeignKey(Product,on_delete=models.CASCADE)
    delievery_address=models.CharField(max_length=200)
    status=models.IntegerField()

class CartManager(models.Manager):
    def new_or_get(self,request):
        cart_id=request.session.get("cart_id",None)
        qs=self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj=False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user=request.user
                cart_obj.save()
        else:
            cart_obj = self.new(user=request.user)
            new_obj=True
            request.session['cart_id']=cart_obj.id
        return cart_obj,new_obj

    def new(self,user=None):
        user_obj=None
        if user is not None:
            if user.is_authenticated is True:
                user_obj=user
        return self.model.objects.create(user=user_obj)



class Cart(models.Model):
    user=models.OneToOneField(User, null=True, blank=True,on_delete=models.SET_NULL)
    products=models.ManyToManyField(Product,blank=True)
    total=models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    objects=CartManager()
    def __str__(self):
        return str(self.id)


def pre_save_cart_receiver(sender,instance,action,*args,**kwargs):
    if action=='post_add' or action=='post_remove' or action=='post_clear':
        products=instance.products.all()
        total=0
        for x in products:
            total+=x.price
        instance.total=total
        instance.save()

m2m_changed.connect(pre_save_cart_receiver,sender=Cart.products.through)
