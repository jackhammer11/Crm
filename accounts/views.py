from django.shortcuts import render,redirect
from .models import *
# Create your views here.
from django.http import HttpResponse
from .forms import OrderForm,CreateUserForm,CustomerForm,ProductForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_user,admin_only

from django.contrib.auth.models import Group

from django import template


@unauthenticated_user
def signup(request):

	form =  CreateUserForm()
	if request.method == 'POST':
		form =  CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,"Account was created for " + username)

			

			return redirect('login')
	context = {'form':form}
	return render(request,'accounts/signup.html',context)


@unauthenticated_user
def login_view(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')


		user = authenticate(request,username=username,password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request,'Username OR password is incorrect')



	context = {}
	return render(request,'accounts/login.html',context)



def logout_view(request):
	print("Logging out from inline")
	logout(request)

	return redirect('login')


 







@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()



	total_customers = customers.count()

	total_orders = orders.count()

	delivered = orders.filter(status ='Delivered').count()
	pending = orders.filter(status ='Pending').count()

	context = {
				'orders':orders,
				'customers':customers,
				'total_customers':total_customers,
				'total_orders':total_orders,
				'delivered':delivered,
				'pending':pending
				}
	return render(request,'accounts/dashboard.html',context)



@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def userpage(request):
	orders = request.user.customer.order_set.all()


	customers = Customer.objects.all()



	

	total_orders = orders.count()

	delivered = orders.filter(status ='Delivered').count()
	pending = orders.filter(status ='Pending').count()


	context = {'orders':orders,'total_orders':total_orders,
				'delivered':delivered,
				'pending':pending}
	return render(request,'accounts/user.html',context)





@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)


	if request.method == 'POST':
		form = CustomerForm(request.POST,request.FILES,instance=customer)
		if form.is_valid():
			form.save()

	context = {'form':form}
	return render(request,'accounts/account_settings.html',context)











@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):
	products =  Product.objects.all()
	
	
	return render(request,'accounts/products.html',{'products':products})



@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def create_customer(request):
	#customer = request.user.customer
	form = CustomerForm()


	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()

	context = {'form':form}
	return render(request,'accounts/account_settings.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])

def add_product(request):
	form = ProductForm()

		
	if request.method == 'POST':
		form = ProductForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('product')

	context = {'form':form }

	return render(request,'accounts/add_product.html',context)




login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateProduct(request,pk):
		product = Product.objects.get(id = pk)
		form = ProductForm(instance=product)
		if request.method == "POST":
		#print('Printing Post',request.POST)
			form = ProductForm(request.POST,instance = product)
			if form.is_valid():
				form.save()
				return redirect('product')


		context = {'form':form}
		return render(request,'accounts/add_product.html',context)



login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteProduct(request,pk):

	product = Product.objects.get(id = pk)
	if request.method == 'POST':
		product.delete()
		return redirect('product')
	context = {'item':product}
	
	return render(request,'accounts/delete_product.html',context)









@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer_page(request):
	customers = Customer.objects.all()
	context = {'customers':customers}
	return render(request,'accounts/customer.html',context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer_info(request,pk_test):
	customer = Customer.objects.get(id=pk_test)
	orders = customer.order_set.all()
	total_orders = orders.count()

	myFilter = OrderFilter(request.GET,queryset=orders)
	orders = myFilter.qs

	context = {'customer':customer ,'orders':orders,'total_orders':total_orders,'myFilter':myFilter}
	return render(request,'accounts/customerinfo.html',context)









@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def orders(request):
	orders =  Order.objects.all()

	#print(order.get().product_id)
	products = Product.objects
	customers = Customer.objects
	#print(product)
	i = 0
	j = 0
	for order in orders:
		orders[i].product_name = products.get(id = order.product_id)
		orders[j].customer_name = customers.get(id = order.customer_id)
		i = i + 1
		j = j + 1


	
	context = {'orders':orders,'products':products,'customers':customers}



	
	return render(request,'accounts/order.html',context)





@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)





@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request,pk):
		order = Order.objects.get(id = pk)
		form = OrderForm(instance=order)
		if request.method == "POST":
		#print('Printing Post',request.POST)
			form = OrderForm(request.POST,instance = order)
			if form.is_valid():
				form.save()
				return redirect('/')


		context = {'form':form}
		return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request,pk):

	order = Order.objects.get(id = pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {'item':order}
	
	return render(request,'accounts/delete.html',context)






