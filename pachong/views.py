from django.core.paginator import Paginator
from django.shortcuts import render

from pachong.models import User, RecruitInfo

# Create your views here.




#登录
# from crawl_pachong.pachong.models import User,RecruitInfo


def login(request):
    return  render(request,"login.html")

#登录逻辑
def login_logic(request):
    username = request.GET.get("username")
    password = request.GET.get("password")

    userInfo = User.objects.filter(username=username)
    userpwd=User.objects.filter(password=password)
    if userInfo and userpwd:
        # 查询密码
        return render(request,"main.html")
    else:
        return  render(request,"login.html")



#注册
def register(request):

    return render(request,"register.html")

# 3, 定义注册逻辑的view
def register_logic(request):
    #获取异步传来的用户名
    username = request.GET.get("username")
    email=request.GET.get("email")
    password=request.GET.get("password")
    telephone=request.GET.get("telphone")
    # 判断用户名是否和数据库重复
    if User.objects.filter(username=username):
        return render(request,"register.html")
    else:
        User(username=username,email=email,password=password,telephone=telephone).save()

        return render(request,"login.html")



#主页面
def main(request):

    return  render(request,"main.html")
    # return render(request,"main.html")
#介绍
def introduce(request):
    return  render(request,"introduce.html")

#菜单
def menu(request):
    a = RecruitInfo.objects.all()
    page_num = request.GET.get("num")
    # print(page_num)

    page_conut=request.GET.get("page_count")
    if not page_num:
        page_num = 1
    page=Paginator(object_list=a,per_page=10).page(page_num)
    return render(request,"menu.html",{'page':page,
                                       'page_num':page_num,
                                       'page_count':page_conut})


def get_bar(request):
    return render(request,"柱状图.html")

def get_pie(request):
    return render(request,"饼图.html")

def get_map(request):
    return render(request,"地图.html")


def search_datas(request):
    recruit_infor=RecruitInfo.objects.filter().values()
    pass