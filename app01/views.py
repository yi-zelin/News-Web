from django.shortcuts import render


# Create your views here.

def mainpage(request):
    return render(request, "mainpage.html")


def user_list(request):
    return render(request, "user_list.html")


def news(req):
    import requests
    import re

    startNews = 0
    getTimes = 2
    # will get getTimes * 10 news
    newsList = []
    getTitle = re.compile(r'\"-webkit-line-clamp:3\">(?P<title>.*?)[<\n]', re.S)
    getTime = re.compile(r'px\"><span>(?P<time>.*?) ago</span>', re.S)
    getSource = re.compile(r'alt=\"\"></g-img><span>(?P<source>.*?)</span>', re.S)
    getLink = re.compile(r'<a class=\"[a-zA-Z\d]{6}\" href=\"(?P<link>.*?)\" data-ved=', re.S)
    getDetail = re.compile(
        r'style=\"margin-top:\dpx;-webkit-line-clamp:3\">(?P<detail>.*?)</div><span class=\"[a-zA-Z\d]{6}\"', re.S)
    layoutDic = ('source', 'title', 'time', 'link', 'detail')

    url = 'https://www.google.com/search'
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 "
                      "Safari/537.36 "
    }
    while getTimes >= 1:
        param = {
            "q": "news",
            "sxsrf": "ALiCzsYtvsSLSN_nox6pRMzinRP1FqCchw:1654728676189",
            "source": "lnms",
            "tbm": "nws",
            "start": startNews,
            "sa": "X",
            "ved": "2ahUKEwjglsbX-J74AhXFIzQIHQUrBckQ_AUoAXoECAEQAw",
            "biw": "1047",
            "bih": "1359",
            "dpr": 1,
        }

        resp = requests.get(url=url, params=param, headers=head)
        pageCode = resp.text

        tempNewsList = []

        i = 0
        for item in getTitle.finditer(pageCode):
            dicNews = dict.fromkeys(layoutDic)
            dicNews['title'] = item.group("title")
            tempNewsList.append(dicNews)
        for item in getTime.finditer(pageCode):
            tempNewsList[i]['time'] = item.group("time")
            i += 1
        i = 0
        for item in getSource.finditer(pageCode):
            tempNewsList[i]['source'] = item.group("source")
            i += 1
        i = 0
        for item in getLink.finditer(pageCode):
            tempNewsList[i]['link'] = item.group("link")
            i += 1
        i = 0
        for item in getDetail.finditer(pageCode):
            tempNewsList[i]['detail'] = item.group("detail")
            i += 1
        del i

        print(tempNewsList)

        resp.close()
        # 关闭resp
        getTimes -= 1
        startNews += 10
        newsList.extend(tempNewsList)
    # end loop here


    return render(req, 'news.html', {"newsList": newsList})
