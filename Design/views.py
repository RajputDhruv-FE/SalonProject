from django.shortcuts import render,redirect
from . forms import CityForm,AreaForm,UserForm,ServiceForm
from . models import CityMst,AreaMst,UserMst,ServiceMst
from django.db.models import Q,F

def IndexView(request):
    content  = CityMst.objects.values_list('CityName',flat=True)
    cityNames = [city.capitalize() for city in content]
    data = {"cities":cityNames}
    return render(request, 'index.html',data)
# Create your views here.

def Login(request):
    flag = 0
    if request.method == 'POST' and flag ==0:
        # username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        usertype = request.POST['acter']

        if email == 'admin@gmail.com' and usertype == 'Admin' and password =='Admin':
            request.session['admin'] = email
            flag = 1
            return redirect('AdminDashboard')
        elif flag == 0 and usertype == 'User' and (UserMst.objects.filter(Q(Email = email)& Q(Password = password)).exists()): 
            request.session['user'] = email
            flag = 1
            return redirect('UserProfile')
        elif flag == 0 and usertype == 'Owner' and (UserMst.objects.filter(Q(Email = email)& Q(Password = password)).exists()): 
            request.session['user'] = email
            flag = 1
            return redirect('SalonOwnerDashboard')
    else:
        return render(request, 'Login.html')

def AdminDashboard(request):
    if request.session.has_key('admin'):
        SalonRequest = UserMst.objects.filter(Usertype="owner")
        users = UserMst.objects.all()
        content={"salonrequest":SalonRequest,"users":users}
        return render(request, 'admin/AdminDashboard.html',content)
    else:
        return redirect('Login')
    
def UpdateSalonStatus(request,id):
    status = request.POST['status']
    # print(status)
    salondata = UserMst.objects.get(id = id)
    salondata.Status = status
    salondata.save()
    return redirect('AdminDashboard')
    
def UserProfile(request):
    if request.session.has_key('user'):
        cityNames  = CityMst.objects.values_list('CityName',flat=True)
        areaNames  = AreaMst.objects.values_list('AreaName',flat=True)
        email = request.session.get("user")
        userdata=UserMst.objects.get(Email=email)
        print(userdata)
        
        data = {"cities":cityNames,"areas":areaNames,"userdata":userdata}
        return render(request,'User/UserProfile.html',data)
    else:
        return redirect('Login')
def SalonOwnerDashboard(request):
    return render(request,'owner/SalonOwnerDashboard.html')
    
def Logout(request):
    if 'admin' in request.session:
        del request.session['admin']
        return redirect('IndexView')
    if 'user' in request.session:
        del request.session['user']
        return redirect('IndexView')
    
def CityTrans(request,id=0):
    # content  = CityMst.objects.values_list('CityName',flat=True)
    # cityNames = [city.capitalize() for city in content]
    # data = {"cities":cityNames}
    if request.method == "GET":
        if id==0:
            form = CityForm()
        else:
            cid = CityMst.objects.get(pk= id)
            form = CityForm(instance=cid)
        return render(request, 'admin/CityForm.html', {'form':form})
    

    # to update the city name
    else:
        if id == 0:
            form = CityForm(request.POST)
        else:
            cid = CityMst.objects.get(pk=id)
            form = CityForm(request.POST,instance=cid)
        if form.is_valid():
            form.save()
        return redirect('CityTrans')   
    
    # return render(request, 'admin/CityForm.html', {'form': form,'data':data})
def AreaTrans(request,id=0):
    if request.method == "GET":
        if id==0:
            form = AreaForm()
        else:
            aid = AreaMst.objects.get(pk= id)
            form = AreaForm(instance=aid)
        return render(request, 'admin/AreaForm.html', {'form':form})
    

    # to update the Area name
    else:
        if id == 0:
            form = AreaForm(request.POST)
        else:
            aid = AreaMst.objects.get(pk=id)
            form = AreaForm(request.POST,instance=aid)
        if form.is_valid():
            form.save()
        return redirect('AreaTrans')
    
    # return render(request, 'AreaForm.html', {'form': form})

def UserTrans(request):
    
    form=UserForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
    
    return render(request, 'UserForm.html', {'form': form})

def ServiceTrans(request,id=0):
    if request.method == "GET":
        if id==0:
            form = ServiceForm()
        else:
            sid = ServiceMst.objects.get(pk= id)
            form = ServiceForm(instance=sid)
        return render(request, 'admin/Service.html', {'form':form})
    

    # to update the Service name
    else:
        if id == 0:
            form = ServiceForm(request.POST)
        else:
            sid = ServiceMst.objects.get(pk=id)
            form = ServiceForm(request.POST,instance=sid)
        if form.is_valid():
            form.save()
        return redirect('ServiceTrans')

def CityList(request):
    content = {"CityList":CityMst.objects.all()}

    return render(request,'admin/CityList.html',content)

def AreaList(request):
    content = {"AreaList":AreaMst.objects.all()}
    return render(request,'admin/AreaList.html',content)

def ServiceList(request):
    content = {"ServiceList":ServiceMst.objects.all()}
    return render(request,'admin/ServiceList.html',content)

def ChangePassword(request):
    return render(request,'ChangePassword.html')

#this code for change password

def HandleChangePassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        print(email,old_password,new_password,confirm_password)
        if confirm_password == new_password:
            if UserMst.objects.filter(Q(Email = email) & Q(Password = old_password)).exists():
                member = UserMst.objects.get(Email = email)
                member.Password = new_password
                member.save()
                content = {"message":"Password Changed Successfully"}
                return render(request,'ChangePassword.html',content)
            else:
                content = {"message":"Old Password is Incorrect"}
                return render(request,'ChangePassword.html',content)
        else:
            content = {"message":"New Password and Confirm Password do not match"}
            return render(request,'ChangePassword.html',content)
    else:
        return render(request,'ChangePassword.html')

def ForgetPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        Username = request.POST['username']
        if UserMst.objects.filter(Q(Email = email) & Q(UserName = Username)).exists():
            member = UserMst.objects.get(Email = email)
            password = member.Password
            content = {"message":password}
            return render(request,'User/ForgetPassword.html',content)
    else:
        return render(request,'User/ForgetPassword.html')
    
def xxx(request):
    import smtplib
    from email.mime.text import MIMEText

    sender_email = "salonproject01@gmail.com"
    sender_password = "salon@1234"
    recipient_email = "umeshshah.uro@gmail.com"
    subject = "Hello from Python"
    body = "This is the body of the email."

# Create the MIMEText object
    html_message = MIMEText(body, 'html')
    html_message['Subject'] = subject
    html_message['From'] = sender_email
    html_message['To'] = recipient_email

# Connect to the SMTP server and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, html_message.as_string())