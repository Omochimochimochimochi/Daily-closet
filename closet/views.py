from django.shortcuts import render

def top(request):
    # closet/templates/closet/top.html を探しに行って表示する
    return render(request, 'closet/top.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def password_reset_view(request):
    return render(request, 'password_reset.html')

def password_reset_done_view(request):
    return render(request, 'password_reset_done.html')

def password_reset_confirm_view(request):
    return render(request, 'password_reset_confirm.html')

    
def signup_complete(request):
    return render(request, 'signup_complete.html')

def mypage(request):
    return render(request, 'mypage.html')    