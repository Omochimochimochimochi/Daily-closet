from django.shortcuts import render

def top(request):
    # closet/templates/closet/top.html を探しに行って表示する
    return render(request, 'closet/top.html')