import datetime
import random
import string
import traceback
import hashlib
from lxml import etree

import requests
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from lr_app.models import User


import os
from django.core.mail import send_mail, EmailMultiAlternatives

from search_app.views import Vister

os.environ['DJANGO_SETTINGS_MODULE']='mid_project.settings' # 发件人的信息所在
# Create your views here.
#  转发登录页面


def login(request):
    return render(request,'login.html')

def login_logic(request):
    # 接收账号密码
    username = request.POST.get("username")
    password = request.POST.get("password")

    # 给访问者塞cookie
    v_cookie = request.COOKIES.get('v_pass')
    print('v_cookie',v_cookie)
    if not v_cookie:
        vister = Vister()
        v_pass = random.sample('qwertyuiopasdfghjkzxcvbnm', 8)
        request.session[str(v_pass)] = vister
    else:
        vister = request.session.get(v_cookie)
        v_pass = v_cookie
        print(vister)


    # 校验 username 和 password
    admin = User.objects.filter(username=username)
    if admin:
        response = redirect('recruit:main')

        salt=admin[0].salt
        print(salt)
        secret_key=admin[0].secret_key
        secret_key1=addSalt(password,salt)
        print('密钥',secret_key,secret_key1)
        print('用户名是:',admin,salt)

        login_time = datetime.datetime.now()
        ip = request.META['REMOTE_ADDR']
        request.session['username'] = username
        # ip='203.198.100.201'
        print(ip, 'ip是多少')
        req = requests.get('https://www.ip.cn/index.php?ip=' + ip)
        html = etree.HTML(req.text)
        ip_address = html.xpath('//*[@id="result"]/div/p[2]/code/text()')[0]
        ip_db = admin[0].ip
        print(ip_db, '数据库查出来的IP是')
        if secret_key==secret_key1:
            index=admin[0].index
            if index:
                index+=1
            else:
                index=1
            admin[0].ip = ip
            admin[0].ip_address = ip_address
            admin[0].index = index
            admin[0].time=login_time
            admin[0].save()
        else:
            return redirect('lr:login') # 用户名存在,但是密码不对,跳转回登录页面

        #给登录过的用户做标记
        vister.vip=True
        vister.ip = admin[0].ip
        vister.username=username
        vister.login_time=login_time
        vister.ip_address=ip_address
        request.session[v_cookie] = vister

        response.set_cookie('v_pass', v_pass) # 待定

        return response # 验证成功，跳转到主页

    # 登陆失败,跳回登录页面
    return redirect('lr:login')


# 转发注册页面
def register(request):
    return render(request,'register.html')


num_tel=0
num_email=0
num_captcha=0
num_username_password=0
# 电话异步验证
def ajax_telephone(request):
    telephone = request.GET.get("telephone")
    admin = User.objects.filter(telephone=telephone)
    print(telephone,'电话号码')
    global num_tel
    if len(telephone)!=11 or telephone[0] !='1':
        print(len(telephone),telephone[0],'失败是多少')
        print('num1是多少', num_tel)
        return JsonResponse('1',safe=False) # 不满足手机号条件
    elif admin:
        return JsonResponse('2',safe=False)
    else:

        num_tel=1
        print('num1是多少', num_tel)
        print(len(telephone), telephone[0], '成功是多少')
        return JsonResponse('0',safe=False) # 满足的话


def ajax_email(request):
    email = request.GET.get('email')
    admin = User.objects.filter(email=email)
    print(email, '邮箱')
    print(admin,len(admin),'用户是')
    global num_email
    if '@' not in email or email[-4:-1]+email[-1] != '.com' or len(email)<15:
        print(email[-4:-1]+email[-1], '失败是多少')
        print('num_email是多少', num_email)
        return JsonResponse('1', safe=False)  # 不满足邮箱条件
    elif admin:
        return JsonResponse('2',safe=False)
    else:
        num_email = 1
        print('num_email是多少', num_email)
        return JsonResponse('0', safe=False)  # 满足的话


# 生成验证码并发送至邮箱
def get_captcha(request):
    email= request.GET.get('email')

    code_list = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 5)
    code = ''.join(code_list)
    request.session['code'] = code
    print("code is:", code)
    subject, from_email, to = '来自的测试邮件', 'a4332707@sina.com', '%s'%email
    text_content = '欢迎访问pzc，祝贺你收到了我的邮件，有幸收到我的邮件说明你极其幸运'
    html_content = '<p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>127.0.0.1:8000/lr/login/</a>，欢迎你来验证你的邮箱，您收到的验证码是'+code+'验证结束你就可以登录了！</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return JsonResponse(1,safe=False)

# 核对验证码是否匹配
def check_email(request):
    captcha=request.GET.get('captcha')
    code =request.session.get('code')
    print('输入的验证码是',captcha)
    print('真正的验证码是',code)
    if captcha==code:
        global num_captcha
        num_captcha=1
        return JsonResponse(1,safe=False)
    else:
        return JsonResponse(0,safe=False)


def ajax_username_password(request):
    username=request.GET.get('username')
    password=request.GET.get('password')
    admin=User.objects.filter(username=username)
    print(username,password,admin,'三者是')
    if len(username)<6 or len(password)<6:
        print('小于6')
        return JsonResponse(0,safe=False)
    elif admin:
        print('名重复')
        return JsonResponse(2,safe=False)
    else:
        global num_username_password
        num_username_password=1
        print('全满足')
        return JsonResponse(1,safe=False)




def register_logic(request):
    try:
        username = request.GET.get("username")
        email = request.GET.get("email")
        password = request.GET.get("password")
        telephone = request.GET.get("telephone")
        print(username,password,telephone,email)
        l = '1234567890qweiosdfghjklzxcvbnm,\./!@#$%^&*()[]~=-+'
        salt = ''.join(random.sample(l, 6))
        tup=addSalt(password,salt) # 加盐
        secret_key=tup
        print('盐和密码',salt,secret_key)
        # 入库
        with transaction.atomic():
            # 电话号 邮箱 验证码 账号密码都验证成功的话,把数据存入数据库
            print('状态码',num_tel,num_email,num_captcha,num_username_password)
            if num_tel==1 and num_email==1 and num_captcha==1 and num_username_password==1:
                User(username=username,password=password,email=email,telephone=telephone,salt=salt,secret_key=secret_key).save()
                return redirect('lr:login')  # 衔接登陆功能
            else:
                return redirect('lr:register')
    except Exception:
        traceback.print_exc()
    #     #注册出错，转回注册页面
        return redirect('lr:register')

# 加盐
def addSalt(password,salt):
    hash_code = hashlib.md5()
    password = str(password) + salt
    hash_code.update(password.encode())
    secret_key =hash_code.hexdigest()
    return secret_key