from django.shortcuts import render
from . import forms
# Create your views here.
def index(request):
    return render(request,'basicapp/index.html')

def form_name_view(request):
    form = forms.FormName()# forms.className()
    if request.method == 'POST': # if user post somthing
        form = forms.FormName(request.POST)
        if form.is_valid():
            # do something
            print("validation success")
            print("name: "+form.cleaned_data['name'])#print data of name in the console
    return render(request,'basicapp/form.html',{'form':form})
    # {}is the content to pass in
