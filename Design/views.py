from django.shortcuts import render,redirect
from . forms import CityForm,AreaForm,UserForm,ServiceForm,SalonForm,SelectServicesForm,ImageForm
from . models import CityMst,AreaMst,UserMst,ServiceMst,SalonMst,SelectedServicemsMst,ImageMst
from django.db.models import Q,F
from django.forms import modelformset_factory

def IndexView(request):
    content  = CityMst.objects.values_list('CityName',flat=True)
    cityNames = [city.capitalize() for city in content]
    salons = SalonMst.objects.all()
    for i in salons:
        print(i.Name)
    data = {"cities":cityNames,"salons":salons}
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
        elif flag == 0 and usertype == 'Owner' and (UserMst.objects.filter(Q(Email = email)& Q(Password = password)& Q(Status="verified")).exists()): 
            request.session['owner'] = email
            flag = 1
            return redirect('SalonOwnerDashboard')
        else:
            content = {"message":"Something went wrong"}
            return render(request,'Login.html',content)
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
    salondata = UserMst.objects.get(id = id)
    salondata.Status = status
    salondata.save()
    return redirect('AdminDashboard')
    
def UserProfile(request):
    if request.session.has_key('user'):
        areaNames  = AreaMst.objects.all()
        email = request.session.get("user")
        userdata=UserMst.objects.get(Email=email)
        salons = SalonMst.objects.all()
        if request.method == 'POST':
            area = request.POST['area']
            salons = SalonMst.objects.filter(Area = area)
            print(salons)
            data = {"areas":areaNames,"userdata":userdata,"salons":salons}
        data = {"areas":areaNames,"userdata":userdata,"salons":salons}
        return render(request,'User/UserProfile.html',data)
    else:
        return redirect('Login')
def SalonOwnerDashboard(request):
    if request.session.has_key('owner'):
        return render(request,'owner/SalonOwnerDashboard.html')
    else:
         return redirect('Login')
    
def Logout(request):
    if 'admin' in request.session:
        del request.session['admin']
        return redirect('IndexView')
    if 'user' in request.session:
        del request.session['user']
        return redirect('IndexView')
    if 'owner' in request.session:
        del request.session['owner']
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
        return render(request,'UserForm.html',{'form':form,'message':'You have registered successfully'})
    
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

    if request.session.has_key( 'user'):
        return render(request,'User/ChangePassword.html')
    else:
        return redirect("Login")

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

def OwnerProfile(request):
    if request.session.has_key('owner'):
        email = request.session.get("owner")
        member = UserMst.objects.get(Email=email)  # Get the UserMst instance
        # get the salon by the owner id
        salon = SalonMst.objects.get(Owner=member)
        content = {"owner":member,"salon":salon}
        return render(request,'owner/OwnerProfile.html',content)

def SalonTrans(request):
    if request.session.has_key('owner'):
        form = SalonForm(request.POST, request.FILES)
        if form.is_valid():
            email = request.session.get("owner")
            member = UserMst.objects.get(Email=email)  # Get the UserMst instance
            instance = form.save(commit=False)  # Create an instance without saving to DB
            instance.Owner = member  # Assign the UserMst instance, not the id
            print(instance.Owner)

            instance.save()  # Save the instance to the database
            return render(request,'owner/OwnerProfile.html',{"message":"You Have Registered the salon successfully"})
    
        return render(request, 'owner/SalonForm.html', {'form': form})
    else:
        return redirect('Login')
    
def SelectServices(request):
    if request.session.has_key('owner'):
        form = SelectServicesForm(request.POST)
        if form.is_valid():
            email = request.session.get("owner")
            member = UserMst.objects.get(Email=email)  # Get the UserMst instance
            # get the salon by the owner id
            salon = SalonMst.objects.get(Owner=member)
            instance = form.save(commit=False)
            instance.SalonId = salon
            instance.save()  # Save the instance to the database
            return render(request,'owner/OwnerProfile.html',{"message":"You Have Selected the services successfully"})
            
            
        return render(request, 'owner/SelectServices.html', {'form': form})
    else:
        return redirect('Login')
    
def SalonDetails(request,id):
    if request.session.has_key('user'):
        salon = SalonMst.objects.get(id = id)
        servies = SelectedServicemsMst.objects.filter(SalonId = id)
        images = ImageMst.objects.filter(SalonId = id)
        print(images)
        return render(request,'SalonDetails.html',{'salon':salon,'services':servies,'images':images})
    else:
        return redirect('Login')
    

def upload_images(request):
    ImageFormSet = modelformset_factory(
        ImageMst,
        form=ImageForm,
        extra=5  # Number of blank forms
    )
    if request.method == 'POST':
        formset = ImageFormSet(request.POST, request.FILES, queryset=ImageMst.objects.none())
        if formset.is_valid():
            email = request.session.get("owner")
            member = UserMst.objects.get(Email=email)  # Get the UserMst instance
            # get the salon by the owner id
            salon = SalonMst.objects.get(Owner=member)
            
            for form in formset:
                if form.cleaned_data:
                    instance = form.save(commit=False)
                    instance.SalonId = salon
                    instance.save() 
                    
            return redirect('OwnerProfile')
    else:
        formset = ImageFormSet(queryset=ImageMst.objects.none())
    return render(request, 'owner/UploadImg.html', {'formset': formset})




