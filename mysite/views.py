from django.shortcuts import render,redirect
from django.http import HttpResponse
from blog.models import Article
from django.contrib.auth.views import LoginView
from mysite.forms import UserCreationForm,ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sitemaps import ping_google
import os
# Create your views here.

#記事表示
def index(request):
    ranks = Article.objects.order_by('-count')[:2]#降順
    objs = Article.objects.all()[:3]
    context = {
        'title': 'really site',
        'articles':objs,
        'ranks':ranks,#ランキング
    }
    return render(request,'mysite/index.html',context)

#landing page
def landing(request):
    context={}
    return render(request,'mysite/landing.html',context)

#ログイン
class Login(LoginView):
    template_name = 'mysite/auth.html'

    def form_valid(self,form):
        messages.success(self.request,'ログイン完了')
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request,'エラー')
        return super().form_invalid(form)

#新規登録signup
def signup(request):
    context = {}
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            #user.is_active=False
            user.save()
            #新規登録時にログインさせる
            login(request,user)

            messages.success(request,'登録完了')
            return redirect('/')
    return render(request,'mysite/auth.html',context)

#mypage　クラスビューを使った記載
class MypageView(LoginRequiredMixin,View):
    context={}

    def get(self,request):
        return render(request,'mysite/mypage.html',self.context)

    def post(self,request):
        form = ProfileForm(request.POST,request.FILES)
        print(form)
        if form.is_valid():
            profile = form.save(commit=False)#処理前にsaveすると改変作業が下の行にあるから、saveさせずにform要素を入れ込むために(commit=False)をつける
            profile.user = request.user
            profile.save()#DBの更新
            messages.success(request,'登録完了')
            #print(context)
        return render(request,'mysite/mypage.html',self.context)

#お問い合わせ
def contact(request):
    context={'grecaptcha_sitekey': os.environ['GRECAPTCHA_SITEKEY'] ,}
    if request.method=='POST':
        recaptcha_token = request.POST.get("g-recaptcha-response")
        res =grecaptcha_request(recaptcha_token)
        if not res:
            messages.error(request,'reCAPTCHAに失敗したようです')
    return render(request,'mysite/contact.html',context)


def grecaptcha_request(token):
    from urllib import request, parse
    import json, ssl
 
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
 
    url = "https://www.google.com/recaptcha/api/siteverify"
    headers = { 'content-type': 'application/x-www-form-urlencoded' }
    data = {
        'secret': os.environ['GRECAPTCHA_SECRETKEY'],
        'response': token,
    }
    data = parse.urlencode(data).encode()
    req = request.Request(
        url,
        method="POST",
        headers=headers,
        data=data,
    )
    f = request.urlopen(req, context=context)
    response = json.loads(f.read())
    f.close()
    return response['success']


@login_required
def ping(request):
    try:
        if request.user.is_admin:
            ping_google()
    except:
        pass
    return redirect('/')