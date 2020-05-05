from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
# from django.views.decorators.csrf import csrf_protect

from .forms import SelectForm

import json
from random import randrange

from rest_framework.views import APIView

from pyecharts.charts import Bar, Sunburst
from pyecharts import options as opts
from pyecharts.options import SunburstItem

from myapp.models import Company_Info, Credit_Info

import random


# Create your views here.
'''首页'''
# @csrf_protect
def index(request):
    if request.method == 'POST':  # 如果为“post”方法提交
        obj = SelectForm(request.POST)  # 使用提交的数据实例化表单类
        if obj.is_valid():
            '''
            处理数据
            '''
            global MySunburst
            company = obj.cleaned_data['company']  # 获取选中的company对象
            MySunburst = sunburst_base(company)  # 构造绘图对象
            if not Credit_Info.objects.filter(company_id = company.id):  # 当选择公司对应数据为空时重定向
                return HttpResponseRedirect('/nodataerror/')        
            return HttpResponseRedirect('/demo/creditinfo/')
    else:  # 如果是“get”方法提交
        obj = SelectForm()  # 实例化一个空表单
    return render(request, 'index.html', {'obj': obj})  # 将表单数据整合到模板并呈现

def nodetaerror(request):
    return render(request, 'nodataerror.html')

'''pyecharts渲染相关'''
def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


'''
此全局变量为绘图对象，当重定向到/demo/creditinfo时界面获取数据时需要访问/demo/sunbrust
在/demo/sunburst返回数据时需要将绘图对象转换为json
总的流程为:
1.index中判断数据，获取绘图对象并赋值给MySunbrust，然后重定向到/demo/creditinfo
2./demo/creditinfo中fetchdata函数访问/demo/sunbrust来获取数据
3.MySunbrust在/demo/sunbrust返回时为json类型
''' 
MySunburst = None


# 随机颜色
def randomcolor():
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for _ in range(6):
        color += colorArr[random.randint(0,14)]
    return "#"+color

# 构造绘图对象
def sunburst_base(company) -> Sunburst:
    units = company.units
    charttitle = company.company

    sunburst_item_list = []
    for each in Credit_Info.objects.filter(company_id = company.id):
        sunburstitem = SunburstItem(
            name=each.bank,
            value=each.credit,
            itemstyle_opts={"color":randomcolor()},
            children=[
                SunburstItem(name="已用", value=each.used, itemstyle_opts={"color":randomcolor()}),
                SunburstItem(name="未用", value=(each.credit - each.used), itemstyle_opts={"color":randomcolor()}),
            ]
        )
        sunburst_item_list.append(sunburstitem)
    
    c = (
        Sunburst()
        .add(
            "",
            sunburst_item_list, 
            radius=[0, "95%"],
            highlight_policy="ancestor",
            sort_="null",
            levels=[
                {},
                {
                    "r0": "10%",
                    "r": "76%",
                    "itemStyle": {"borderWidth": 2},
                    "label": {"rotate": "radial"},
                },
                {
                    "r0": "76%", 
                    "r": "80%", 
                    "label": {"align": "right","position": "outside","silent": False},
                    "itemStyle": {"borderWidth": 3},
                },
            ]
        )
        .set_global_opts(title_opts=opts.TitleOpts(
            title=charttitle, 
            subtitle="[单位：%s]" % units, 
            subtitle_textstyle_opts={"font_weight":"bold", "color":"#000000"})
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}"))
        .dump_options_with_quotes()
    )
    return c


class ChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(MySunburst))


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/creditinfo.html").read())