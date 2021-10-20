from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from .models import *
import re


def home(request):
    if(request.user.is_authenticated):
        if(request.method == "POST"):
            user_input = request.POST['input']
            Filtration_choices = request.POST['radio']
            if(Filtration_choices == 'choice-1'):
                pattern = re.compile(r'[1-9]\d[1-9]\d*|[1-9]\d\d\d+')
            elif(Filtration_choices == 'choice-2'):
                pattern = re.compile(r'\b\d{4}[-]\d{2}[-]\d{2}\b')
            elif(Filtration_choices == 'choice-3'):
                pattern = re.compile(r"'(.*)'")
            elif(Filtration_choices == 'choice-4'):
                pattern = re.compile(  r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
                match = pattern.findall(user_input)[0]
                if(0 <= int(match[0:3]) <= 127):
                    return render(request, 'MainApp/home.html', { 'input_address': match, 'class': 'A' })
                elif(128 <= int(match[0:3]) <= 191):
                    return render(request, 'MainApp/home.html', { 'input_address': match, 'class': 'B'})
                elif(192 <= int(match[0:3]) <= 223):
                    return render(request, 'MainApp/home.html', { 'input_address': match, 'class': 'C'})
                elif(224 <= int(match[0:3]) <= 239):
                    return render(request, 'MainApp/home.html', {'input_address': match, 'class': 'D' })
                elif(240 <= int(match[0:3]) <= 255):
                    return render(request, 'MainApp/home.html', { 'input_address': match, 'class': ' E'})
                else:
                    return render(request, 'MainApp/home.html', {'lol': 'Invalid'  })
            elif(Filtration_choices == "choice-5"):
                pattern = re.compile(r'[A-F0-9a-f]{2}[-:][A-F0-9a-f]{2}[-:][A-F0-9a-f]{2}[-:][A-F0-9a-f]{2}[-:][A-F0-9a-f]{2}[-:][A-F0-9a-f]{2}')
            elif(Filtration_choices == "choice-6"):
                def func(x):
                    char = x.group(0)
                    return "_"+char.lower()
                pattern = re.compile(r'([A-Z])')
                match = pattern.sub(func, user_input)
                return render(request, 'MainApp/home.html', { 'class': match })
            match = pattern.findall(user_input)
            if(len(match) == 0):
                return render(request, 'MainApp/home.html', {'lol': 'Invaild Input / Select Different Category '  })
            return render(request, "MainApp/home.html", {  'output': match})
        return render(request, "MainApp/home.html")
    else:
        return render(request, "login.html", {     "message": "Login to Continue" })

