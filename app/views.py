from django.shortcuts import render
from.models import Orders
from django.views.decorators.csrf import csrf_exempt
from .PayTm import Checksum
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
MERCHANT_KEY = 'ebmw@sHniqB3IjEQ'

# Create your views here.
def index(request):
    return render(request,'index.html')


def cart(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson','')
        total = request.POST.get('total','')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '')+" "+ request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')


        order = Orders(items_json=items_json, name=name,email=email,phone=phone,address=address,city=city,state=state,zip_code=zip_code,total=total)
        order.save()
        thank = True
        id = order.order_id
        
        param_dict = {
            'MID': 'VcQuvg10977550566952',
            'ORDER_ID': str(id),
            'TXN_AMOUNT': str(total),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'https://amazon-deploy.herokuapp.com/cart/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict':param_dict})
    return render(request,'cart.html')

@csrf_exempt
def handlerequest(request):
    #paytm send request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order Successfull')
        else:
            print('order was not success full' + response_dict['RESPMSG'])
    return render(request,'paymentstatus.html',{'response': response_dict})
