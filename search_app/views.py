import datetime
import os
import random
import time
from threading import Timer

from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import happybase,hashlib
# Create your views here.
from django.db.models import Count, Max,Avg,Min,Sum
from django.views.decorators.cache import cache_page
from redis import Redis

from search_app.models import RecruitInfo
conn_hbase=happybase.Connection(host='172.16.14.56',port=9090)
conn_hbase.open()
table=conn_hbase.table('crawler:recruit')
red=Redis(host='172.16.14.110',port=7000)
#显示主页
def main(request):
    return render(request,'main.html')
def introduce(request):
    return render(request,'introduce.html')

#查询页面
# @cache_page(timeout=2,key_prefix='cache_page')
def page(request):
    v_cookie = request.COOKIES.get('v_pass')
    ip=request.META['REMOTE_ADDR']
    if not v_cookie:
        vister=Vister()
        vister.ip=ip
        v_pass=random.sample('qwertyuiopasdfghjkzxcvbnm',8)
        request.session[str(v_pass)]=vister
        page = Paginator(object_list=RecruitInfo.objects.filter(city="北京", job_category='大数据'), per_page=20).page(1)
        resp = render(request, 'menu.html', {'page': page, 'num':1})
        resp.set_cookie('v_pass', str(v_pass))
        log_redis_user(vister.username, vister.ip,vister.ip_address, "北京", '大数据', vister.login_time)
        return resp
    else:
        vister=request.session.get(v_cookie)
        vister.all_time+=1
        v_pass=v_cookie
        vister.ip = ip
        request.session[str(v_pass)] = vister
    num = request.GET.get("num")
    city = request.GET.get('city')
    if not city:
        city='北京'
    category = request.GET.get('category')
    if not category:
        category='大数据'
    website = request.GET.get('website')
    if not website:
        website = '内推网'
    job_name = request.GET.get('job_name')
    if not job_name:
        job_name = '20503-AI应用Linux后台研发工程师（上海）'

    prev = request.GET.get('prev')
    if not num:
        num=1
    if int(num)>10 and not vister.vip:
        num=10
    if int(num) > 5:
        if vister.check() or not v_cookie and vister.crawler:
            log_redis_user(vister.username, vister.ip,vister.ip_address, city, category, vister.login_time)
            return search(request,website,city,category,job_name,num,prev)
        else:
            time.sleep(30)
            log_redis_user(vister.username, vister.ip,vister.ip_address, city, category, vister.login_time)
            return search(request, website, city, category, job_name,num,prev)
    else:
        page=Paginator(object_list=RecruitInfo.objects.filter(city__icontains=city, job_category__icontains=category), per_page=20).page(int(num))
        if vister.check() or not v_cookie and vister.crawler:
            log_redis_user(vister.username, vister.ip,vister.ip_address, city, category, vister.login_time)
            return render(request,'menu.html',{'page':page,'num':num})
        else:
            time.sleep(30)
            log_redis_user(vister.username, vister.ip,vister.ip_address, city, category, vister.login_time)
            return render(request,'menu.html',{'page':page,'num':num})
#hbase上查询数据
# @cache_page(timeout=2,key_prefix='cache_search')
def search(request,website,city,category,job_name,num,prev):
    row_start=website+':'+city+':'+category+':'+job_name

    if prev:
        datas=table.scan(row_start=row_start,columns=['show'],limit=10,reverse=True)
    else:
        datas=table.scan(row_start=row_start,columns=['show'],limit=10)
    pages=[]
    for key,value in datas:
        info=dict()
        for i,j in value.items():
            info.update({i.decode()[5:]:j.decode()})
        pages.append(info)
    if prev:
        pages.reverse()
        print('hello')
    return render(request,'menu_base.html',{'page':pages,'num':num})
def search_vague(request):
    value=request.GET.get('value')
    # value='大数据'
    datas=RecruitInfo.objects.filter(job_name__contains=value).values('job_name')[:10]
    data=[]
    for i in datas:
        data.append(i['job_name'])
    return JsonResponse({'data':data})
#根据城市查询数量的方法
def get_data(item):
    return RecruitInfo.objects.filter(city__icontains=item).aggregate(Count('id'))['id__count']
#获取相应城市的统计数量
def get_data_hbase(item):
    datas=[]
    for i in  table.scan(filter="RowFilter(=,'regexstring:\.*"+item+".*')"):
        datas.append(i)
    return len(datas)
def get_data_city():
    num_bj = int(get_data('北京'))+get_data_hbase('北京')
    num_sh = int(get_data('上海'))+get_data_hbase('上海')
    num_sz = int(get_data('广州'))+get_data_hbase('广州')
    num_gz = int(get_data('深圳'))+get_data_hbase('深圳')
    return [num_bj, num_sh, num_sz, num_gz]
#查询种类的方法
def get_data_category(item):
    return RecruitInfo.objects.filter(job_category=item).aggregate(Count('id'))['id__count']

#柱状图
def column(request):
    data=get_data_city()
    return render(request,'column.html',{'data':data})
#饼图
def pie(request):
    python_web= int(get_data_category('Python'))+get_data_hbase('Python')
    crawler = int(get_data_category('爬虫'))+get_data_hbase('爬虫')
    big_data = int(get_data_category('大数据'))+get_data_hbase('大数据')
    ai= int(get_data_category('AI'))+get_data_hbase('AI')
    data = [python_web,crawler,big_data,ai]
    return render(request,'pie.html',{'data': data})
#地图
def map(request):
    data = get_data_city()
    return render(request,'map.html',{'data':data})
#折线图
def line(request):
    data = get_data_city()
    return render(request,'line.html',{'data':data})
#vister类,
class Vister:
    def __init__(self,all_time=1,first_time=time.time()):
        self.all_time=all_time
        self.first_time=int(first_time)
        self.vip=None
        self.crawler=True
        self.ip=None
        self.username=None
        self.login_time=None
        self.ip_address=None
    def check(self):
        if self.all_time>10:
            result=int(time.time()) - self.first_time
            if result<1:
                self.all_time = 1
                self.crawler = None
                #1小时后解除
                Timer(3600, self.relieve).start()
                return None
            self.all_time=1
        return True
    def relieve(self):
        self.crawler=True
#用户登录了访问了哪个城市,哪个类数据
def log_redis_user(username=None,ip=None,ip_address=None,city=None,category=None,login_time=None):
    if not username:
        username=ip
    login_time=str(login_time)[:-7]
    request_time=str(datetime.datetime.now())[:-7]
    data={'ip': ip,'ip_address':ip_address, 'city': city, 'job_category': category, 'login_time': login_time, 'request_time': request_time}
    #把用户存到redis中
    red.sadd(str(username)+':'+request_time,data)
    #从把用户名存到user_log
    red.lpush('user_log',str(username))

