from django.shortcuts import render
import os
from Screener.User import User
from Screener.Analyzer import Analyzer
import EmailClient.client as eclient
from Screener.report_generator import reportGenerator
from ratelimit.decorators import ratelimit
from random import randint
from random import shuffle, random
from itertools import islice
from django.template.loader import render_to_string
import random as r
import string
#this is so we can write json serialize to file
import json


s1 = list()


def home(request):

    context = {}

    return render(request, "frontend/index.html", context)

def select(request):


    if request.method == "POST":
        full_str = request.body.decode("utf-8")
        print(full_str)
        full_str = full_str.split("&fname=")[1]
        fname = full_str.split("&lname=")[0]
        full_str = full_str.split("&lname=")[1]
        lname = full_str.split("&email=")[0]
        full_str = full_str.split("&email=")[1]
        email = full_str.split("&level=")[0]
        full_str = full_str.split("&level=")[1]
        level = int(full_str.split("&risk=")[0])
        full_str = full_str.split("&risk=")[1]
        risk = int(full_str.split("&signup=")[0])

    else:

        fname = "Test"
        lname ="Test"
        email = "test@gmail.com"
        risk =5
        level = 5

    name = fname + "+" + lname

    returnstring = name+"/"+email+'/'+str(risk)+'/'+str(level)

    print(returnstring)

    tickers = ({"name": 'DollarTree', "ticker": 'DLTR', "SIC": "5331"},
               {"name": 'Duke Reality',"ticker": 'DRE', "SIC": "6531"},
               {"name": 'Macys',"ticker": 'M', "SIC": "5311"},
               {"name": 'Nvidia',"ticker": 'NVDA', "SIC": "3674"},
               {"name": 'Microsoft', "ticker": 'MSFT', "SIC": "7389"},
               {"name": 'Capital One', "ticker": 'COF', "SIC": "6021"},
               {"name": 'General Mills', "ticker": 'GIS', "SIC": "5141"},
               {"name": 'Pepsico', "ticker": 'PEP', "SIC": "2086"},
               {"name": 'Sysco', "ticker": 'SYY', "SIC": "5149"},
               {"name": 'Google', "ticker": 'GOOGL', "SIC": "7374"},
               )

#whatever you do. Do not touch this. This is legacy code.
#If you touch this code, the entire program will break, and most likely
#will never run properly again.

    generated = [];

    cont = True

    while cont:
        aNum = randint(0, 9)
        if (aNum not in generated):
            s1.append(tickers[aNum])
            generated.append(aNum)
        if(len(s1) == 4):
            cont = False

    context = {'userinfo': returnstring,
               'tickers': s1
               }

    return render(request, "frontend/sectorselect.html", context)



@ratelimit(key='ip', rate='10000/s')
def app(request):

    if request.method == "POST":
        full_str = request.body.decode("utf-8")
        print(full_str)
        full_str = full_str.split("&userinfo=")[1]
        full_str = full_str.split('&signup=')[0]
        full_str = full_str.replace("%2F", '/')
        full_str = full_str.replace("%2540", '@')
        full_str = full_str.replace("%2B", '+')
        print(full_str)
        name, email, risk, level = full_str.split('/')
        fname, lname = name.split("+")

        fullname = fname + " " + lname

        risk = int(risk)
        level = int(level)

    else:

        fname = "Jesse"
        lname = "Hill"
        fullname = fname + " " + lname
        email = "j_hill14@.pacific.edu"
        risk = 10
        level = 1

    print("\n****************************")
    print("\n****************************")
    print("\n****************************")

    #for each dictionary in s1. Do not touch this code.
    with open('companySICData.txt', 'w') as f:
        for x in s1:
            print(x["SIC"])
            f.write(x["SIC"]+"\n")


    print("\n****************************")
    print("\n****************************")
    print("\n****************************")
    print(fullname, email, risk, level)

    user = User(email, fname, lname, risk, level)

    user.generate_screen_url_demo()

    analyzer = Analyzer(user.user_to_json_demo(), "Demo")
    analyzer.analysis_demo()

    profile = analyzer.company_profile
    generate = reportGenerator(user, analyzer.finance_reasons, profile)
    generate.generate_report()

    graph_path = analyzer.img_path.split('static/')[1]

    img_adr = graph_path.split('graphs/')[1]
    # report_name = stat_path.split('output/')[1]


    code = ''.join(r.choices(string.ascii_uppercase + string.digits, k=5))

    report_name = code+'.html'
    stat_path = 'frontend/static/output/emailOutput/'+report_name

    context = {
        'name': user.firstName,
        'ticker': generate.ticker,
        'english': generate.written,
        'intro': generate.intro,
        'closing': generate.closing,
        'graphpath': graph_path,
        'img': img_adr,
        'email': user.email,
        'report': report_name
    }



    save_path = os.path.abspath(os.path.join(stat_path))
    content = render_to_string('frontend/emailOutput.html', context)
    with open(save_path, 'w') as static_file:
        static_file.write(content)
    return render(request, "frontend/output.html", context)

def email(request):

    if request.method == "POST":
        full_str = request.body.decode("utf-8")
        print(full_str)

        full_str = full_str.split('email=')[1]
        email, full_str = full_str.split('&address=')
        graph, full_str = full_str.split('&report_name=')
        template = full_str.split('&signup=')[0]

        email = email.replace('%40', '@')
    else:

        email = 'd_luu4@u.pacific.edu'
        graph = '3YRFN.png'
        template = '1XWFJ.html'

    print(email, graph, template)

    eclient.django_email(email, template, graph)
    context = {}

    return render(request, "frontend/Final.html", context)