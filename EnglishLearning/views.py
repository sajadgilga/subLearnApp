from django.shortcuts import render

"""
Don't add any functions in this app except the index page
"""


def index(request):
    return render(request, 'index.html')
