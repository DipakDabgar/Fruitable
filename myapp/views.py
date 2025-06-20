from django.shortcuts import render,HttpResponse,redirect
from .models import*
from django.core.paginator import Paginator
from django.utils import timezone
# Create your views here.

def home(request):
    return HttpResponse("hello python")

def index(request):
    if "email" in request.session:
        pid=Product.objects.all()[:8]
        uid=User.objects.get(email=request.session["email"])
        cart_item=Add_to_cart.objects.filter(user_id=uid)
       
        wish_count=Add_to_wishlist.objects.filter(user_id=uid).count()
        cart_count=Add_to_cart.objects.filter(user_id=uid).count()
        con={"pid":pid,"wish_count":wish_count,"cart_count":cart_count,"cart_item":cart_item,"uid":uid}
        return render(request,"index.html",con)
    else:
        return render(request,"login.html")

def wishlist(request):
    if "email" in request.session:
        uid=User.objects.get(email=request.session["email"])
        wish_item=Add_to_wishlist.objects.filter(user_id=uid)

        wish_count=Add_to_wishlist.objects.filter(user_id=uid).count()
        cart_count=Add_to_cart.objects.filter(user_id=uid).count()
        con={"wish_item":wish_item,"wish_count":wish_count,"cart_count":cart_count,"uid":uid}
        return render(request,"wishlist.html",con)
    else:
        return render(request,"login.html")

def add_wish(request,id):
    if "email" in request.session:
        uid=User.objects.get(email=request.session["email"])
        pid=Product.objects.get(id=id)
        wish_item=Add_to_wishlist.objects.filter(product_id=pid,user_id=uid).first()
        
        if wish_item:
            wish_item.delete()
            return redirect("shop")
        else:
            Add_to_wishlist.objects.create(
                user_id=uid,
                product_id=pid,              
                price=pid.price,
                name=pid.name,
                image=pid.image,
                )
        return redirect("shop")
    else:
        return render(request,"login.html")
    
def delete_wishlist(request,id):
    dell=Add_to_wishlist.objects.get(id=id)
    dell.delete()
    return redirect("wishlist")


# def add_whishlist(request, id):
#     uid = User.objects.get(email=request.session['email'])
#     pp = product.objects.get(id=id)
#     w_id = Add_Whishlist.objects.filter(product_id=pp, user_id=uid).first()
    
#     if w_id:
#         w_id.delete()
#         messages.info(request, "Item Removed From Your Wishlist")
#     else:
#         Add_Whishlist.objects.create(
#             user_id=uid,
#             product_id=pp,
#             price=pp.price,
#             name=pp.name,
#             image=pp.img)
#         messages.info(request, "Item Saved In Your Wishlist")
        
#     return redirect("shop")


def cart(request):
        if "email" in request.session:
            uid=User.objects.get(email=request.session["email"])
            cart_item=Add_to_cart.objects.filter(user_id=uid)

     
            wish_count=Add_to_wishlist.objects.filter(user_id=uid).count()
            cart_count=Add_to_cart.objects.filter(user_id=uid).count()
        

            total_price=0
            for i in cart_item:
                total_price += i.product_id.price * i.quantity


            shipping_charge=50

            if total_price==0:
                shipping_charge=0
            else:
                shipping_charge=50

            
            grand_total= total_price + shipping_charge




            con={"wish_count":wish_count,"cart_count":cart_count,"total_price":total_price,"grand_total":grand_total,"shipping_charge":shipping_charge,"cart_item":cart_item,"uid":uid}


            return render(request,"cart.html",con)
        else:
            return render(request,"login.html")



def add_cart(request,id):
    if "email" in request.session:
        uid=User.objects.get(email=request.session["email"])

        pid=Product.objects.get(id=id)
        
        
        cart_item=Add_to_cart.objects.filter(product_id=pid,user_id=uid).first()



        if cart_item :

            cart_item.quantity += 1
            cart_item.total_price = cart_item.quantity * cart_item.price
            cart_item.save()

        else:
            Add_to_cart.objects.create(
                product_id=pid,
                user_id=uid,
                price=pid.price,
                name=pid.name,
                quantity=1,
                image=pid.image,
                total_price=pid.price                        
            )
        return redirect("shop")
    else:
        return render(request,"login.html")



def quantity_plus(request,id):
    cart_item=Add_to_cart.objects.get(id=id)
    if cart_item :
        cart_item.quantity += 1
        cart_item.total_price=cart_item.quantity * cart_item.price
        cart_item.save()

        return redirect("cart")
    else :
        return redirect("cart")
    

def quantity_minus(request,id):
    cart_item=Add_to_cart.objects.get(id=id)
    
    if cart_item :
        if (cart_item.quantity==1):
            Add_to_cart.objects.get(id=id).delete()
        else:
            cart_item.quantity -= 1
            cart_item.total_price=cart_item.quantity * cart_item.price
            cart_item.save()
            return redirect("cart")

        return redirect("cart")
    else :
        return redirect("cart")


def delete_item(request,id):
    dell=Add_to_cart.objects.filter(id=id)
    dell.delete()
    return redirect("cart")

   

def checkout(request):
    if "email" in request.session:
        uid=User.objects.get(email=request.session["email"])
        cart_item=Add_to_cart.objects.filter(user_id=uid)


        wish_count=Add_to_wishlist.objects.filter(user_id=uid).count()
        cart_count=Add_to_cart.objects.filter(user_id=uid).count()
        check_id=Add_to_cart.objects.filter(user_id=uid)

        total_price=0
        for i in check_id:
            total_price += i.product_id.price * i.quantity

        con={"wish_count":wish_count,"cart_count":cart_count,"check_id":check_id,"total_price":total_price,"cart_item":cart_item,"uid":uid}
        return render(request,"checkout.html",con)

    else:
        return render(request,"login.html")


def billing_add(request):
    if "email" in request.session:
        uid=User.objects.get(email=request.session["email"])

        dipak_id= Add_to_cart.objects.filter(user_id=uid)



        if request.POST:
            first_name=request.POST["first_name"]
            last_name=request.POST["last_name"]
            company_name=request.POST["company_name"]
            address=request.POST["address"]
            city=request.POST["city"]
            country=request.POST["country"]
            pincode=request.POST["pincode"]
            mobile=request.POST["mobile"]
            email=request.POST["email"]
            note=request.POST["note"]

            if first_name and last_name and company_name and address and city and country and pincode and mobile and email and note:
                
                Billing_details.objects.create(first_name=first_name,
                                    last_name=last_name,
                                    company_name=company_name,
                                    address=address,
                                    city=city,
                                    country=country,
                                    pincode=pincode,
                                    mobile=mobile,
                                    email=email,
                                    note=note)

             
                for i in dipak_id:
                    Order.objects.create(
                        user_id=uid,
                        name=i.name,
                        image=i.image,
                        quantity=i.quantity,
                        price=i.price,
                        total_price=i.price)
                    i.delete()

                    return redirect("order")
        
          
            
            return render(request,"order.html")
            
        else:
            return render(request,"checkout.html")
        
    else:
        return render(request,"login.html")



def contact(request):
    if "email" in request.session:
        uid=User.objects.get(email=request.session["email"])
        cart_item=Add_to_cart.objects.filter(user_id=uid)

        name=request.POST.get("name")
        email=request.POST.get("email")
        message=request.POST.get("message")
        wish_count=Add_to_wishlist.objects.filter(user_id=uid).count()
        cart_count=Add_to_cart.objects.filter(user_id=uid).count()
        con={"wish_count":wish_count,"cart_count":cart_count,"cart_item":cart_item,"uid":uid}

        if name and email and message:
            Contact.objects.create(name=name,email=email,message=message)
            return redirect("index")
        
        return render(request,"contact.html",con)
    else:
        return render(request,"login.html")


def error(request):
    if "email" in request.session:
        uid=User.objects.get(email=request.session["email"])
        cart_item=Add_to_cart.objects.filter(user_id=uid)

        wish_count=Add_to_wishlist.objects.filter(user_id=uid).count()
        cart_count=Add_to_cart.objects.filter(user_id=uid).count()
        con={"wish_count":wish_count,"cart_count":cart_count,"cart_item":cart_item,"uid":uid}
        return render(request,"error.html",con)
    else:
        return render(request,"login.html")



# def login(request):
#     if request.POST:       
#         email=request.POST["email"]
#         password=request.POST["password"]

#         if email and password:
#             try:
#                 User.objects.get(email=email,password=password)
#                 return redirect("index")
#             except:
#                 er={"e_msg":"Invalid Email or Password"}
#                 return render(request,"login.html",er)
#     return render(request,"login.html")
        
 


def login(request):
    if 'email' in request.session:
        return render(request,"index.html")
    if request.POST:
        email=request.POST['email']
        password=request.POST['password']
        try:
            uid=User.objects.get(email=email)
            if uid.password==password:
                # if uid.email==email:
                    request.session['email']=uid.email
                    return redirect("index")
            else:
                con={"msg":"password do not match"}
                return render(request,"login.html",con)
        except:
            con={"msg":"email dose not match any register user" }
            return render(request,"login.html",con)
    else:
        return render(request,"login.html")


def logout(request):
    del request.session["email"]
    return render(request,"login.html")




def register(request):
    if request.POST:
        name=request.POST["name"]
        email=request.POST["email"]
        password=request.POST["password"]
        confirm_password=request.POST["confirm_password"]

        if password!=confirm_password:
           er={"e_msg":"Password do not match"}
           return render(request,"register.html",er)
        
        else:
            User.objects.create(name=name,email=email,password=password)
            return redirect("login")
    return render(request,"register.html")
    
        



def shop_detail(request):
    return render(request,"shop_detail.html")

def shop_detail1(request,id):
    pid=Product.objects.get(id=id)
    con={"pid":pid}

    return render(request,"shop_detail.html",con)

def price_filter(request):
    if request.POST:
        max1=request.POST["max1"]
        pid=Product.objects.filter(price__lte=max1)
        con={"pid":pid,"max1":max1}

    return render(request,"shop.html",con)

def shop(request):
    if "email" in request.session:
        uid=User.objects.get(email=request.session["email"])
        cid=Category.objects.all()
        cat=request.GET.get("cat")
        pid=Product.objects.all().order_by("-id")
        # cart_item=Add_to_cart.objects.filter(user_id=uid)
        wish_count=Add_to_wishlist.objects.filter(user_id=uid).count()
        cart_count=Add_to_cart.objects.filter(user_id=uid).count()
        sort_by=request.GET.get('sort_by')
        wishlist_product=Add_to_wishlist.objects.filter(user_id=uid)
        l1=[]
        for i in wishlist_product:
            l1.append(i.product_id.id)

        if cat:
            pid=Product.objects.filter(cate_id=cat)
        elif sort_by == 'price_lth':
            pid = Product.objects.all().order_by('price')  
        elif sort_by == 'price_htl':
            pid = Product.objects.all().order_by('-price')  
        elif sort_by == 'name_atz':
            pid = Product.objects.all().order_by('name')  
        elif sort_by == 'name_zta':
            pid = Product.objects.all().order_by('-name') 
        else:
            pid=Product.objects.all().order_by("-id")

        paginator=Paginator(pid,3)  
        page_number=request.GET.get("page",2)  
        pid=paginator.get_page(page_number)
        show_page=paginator.get_elided_page_range(page_number,on_each_side=1,on_ends=1)

        con={"cid":cid,"pid":pid,"cat":cat,"wish_count":wish_count,"cart_count":cart_count,"l1":l1,"sort_by":sort_by,"uid":uid,"show_page":show_page}
        return render(request,"shop.html",con)

    else:
        return render(request,"login.html")
    
  


def testimonial(request):
    if "email" in request.session:
        uid=User.objects.get(email=request.session["email"])
        cart_item=Add_to_cart.objects.filter(user_id=uid)

        wish_count=Add_to_wishlist.objects.filter(user_id=uid).count()
        cart_count=Add_to_cart.objects.filter(user_id=uid).count()
        con={"wish_count":wish_count,"cart_count":cart_count,"cart_item":cart_item,"uid":uid}
        return render(request,"testimonial.html",con)
    else:
        return render(request,"login.html")




import random
from django.core.mail import send_mail

def forgot_password(request):
    if request.POST:
        email=request.POST['email']
        otp1=random.randint(1000,9999)
        try:
            uid=User.objects.get(email=email)
            uid.otp=otp1
            uid.save()
            send_mail("demo",f"your otp is - {otp1}",'dipakdabgar76@gmail.com',[email])
            contaxt={
                "email":email
            }
            return render(request,"confirm_password.html",contaxt)
        except:
            print("Invalid Email")       
            return render(request,"forgot_password.html") 
    else:
        return render(request,"forgot_password.html")
    


def confirm_password(request):
    if request.POST:
        email=request.POST['email']
        otp=request.POST['otp']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        
        try:
            uid=User.objects.get(email=email)
            if str(uid.otp) == otp:
                er={'msg':"Valid OTP"}
                
                if new_password==confirm_password:
                    uid.password=new_password
                    uid.save()
                    er={'msg':"Password Updated"}
                    return redirect("login")
                
                else :
                    er={"msg":"New Password and Confirm Password don't match"}
                    return render(request,"confirm_password.html",er)
                              
            elif str(uid.otp) != otp: 
                er = {"msg":"invalid otp"}
                return render(request,"confirm_password.html",er)
            
        except:
            except1 = {"except msg":"except block"}
            return render(request,"confirm_password.html",except1)
                    
        
    return render(request,"confirm_password.html")

def coupon(request):
    coupon_list = Apply_coupon.objects.all()
    con={'coupon_list': coupon_list}
    return render(request, 'coupon_list.html',con )



def order(request):
        if "email" in request.session:
            uid=User.objects.get(email=request.session["email"])
    

     
            wish_count=Add_to_wishlist.objects.filter(user_id=uid).count()
            cart_count=Add_to_cart.objects.filter(user_id=uid).count()


        
            order_i= Order.objects.filter(user_id=uid)
            



            con={"wish_count":wish_count,"cart_count":cart_count,"uid":uid,"order_i":order_i}


            return render(request,"order.html",con)
        else:
            return render(request,"login.html")
        

