from django.shortcuts import render,redirect
from . forms import CityForm,AreaForm,UserForm,ServiceForm,SalonForm,SelectServicesForm,ImageForm,BookingForm
from . models import CityMst,AreaMst,UserMst,ServiceMst,SalonMst,SelectedServicemsMst,ImageMst,SlotBookingMst
from django.db.models import Q,F
from django.forms import modelformset_factory
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta


def IndexView(request):

    areaNames  = AreaMst.objects.all()
    salons = SalonMst.objects.all()
    if request.method == 'POST':
        area = request.POST['area']
        salons = SalonMst.objects.filter(Area = area)
        print(salons)
        data = {"areas":areaNames,"salons":salons}
    data = {"areas":areaNames,"salons":salons}
    return render(request, 'index.html',data)



def Login(request):
    flag = 0
    if request.method == 'POST' and flag ==0:
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
            return redirect('OwnerProfile')
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
       
        return render(request,'owner/OwnerProfile.html')
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


def UserTrans(request):
    form=UserForm(request.POST,request.FILES)
    if form.is_valid():
        email = form.cleaned_data.get('Email')
        name = form.cleaned_data.get('Name')
        form.save()
        RegistrationEmail(email,name)
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
    else: #to update the Service name 
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
                SendEmail(email,new_password)
                content = {"message":"Password Changed Successfully"}
                return render(request,'User/ChangePassword.html',content)
            else:
                content = {"message":"Old Password is Incorrect"}
                return render(request,'User/ChangePassword.html',content)
        else:
            content = {"message":"New Password and Confirm Password do not match"}
            return render(request,'User/ChangePassword.html',content)
    else:
        return render(request,'User/ChangePassword.html')
    


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
    


def OwnerProfile(request):
    if request.session.has_key('owner'):
        email = request.session.get("owner")
        member = UserMst.objects.get(Email=email)  # Get the UserMst instance
        # get the salon by the owner id
        salon = SalonMst.objects.get(Owner=member)
        bookings = SlotBookingMst.objects.filter(SalonId =salon.id)
        content = {"owner":member,"salon":salon,"bookings":bookings}

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
        email = request.session.get("owner")
        member = UserMst.objects.get(Email=email)  # Get the UserMst instance
        # get the salon by the owner id
        salon = SalonMst.objects.get(Owner=member)
        images = ImageMst.objects.filter(SalonId = salon.id)
        formset = ImageFormSet(queryset=ImageMst.objects.none())
    return render(request, 'owner/UploadImg.html', {'formset': formset,'images':images})


def BookinTransaction(request,id):  
     if request.method == 'POST':
        
        service=request.POST['service']
        date=request.POST['date']
        time=request.POST['time_slot']
        
        serviceobj = SelectedServicemsMst.objects.get(id = service)
        salon = SalonMst.objects.get(id = id)
        user = UserMst.objects.get(Email = request.session.get('user'))
        amount  = serviceobj.Price
        
        SlotBookingMst.objects.create(BookingDate=date,TimeSlote=time,ServiceId=serviceobj,UserId=user,SalonId=salon,BillAmount=amount)
        send_appointment_confirmation_email(user.Email,user.Name,service,date,time,salon.Location,amount)
        return redirect(UserProfile)
     
# for the input taken in 24hour formate
def generate_slots(opening_time, closing_time):
    slots = []
    current_time = datetime.strptime(str(opening_time), "%H:%M:%S")
    closing_time = datetime.strptime(str(closing_time), "%H:%M:%S")

    while current_time < closing_time:
        slot = f"{current_time.strftime('%I:%M %p')} - {(current_time + timedelta(hours=1)).strftime('%I:%M %p')}"
        slots.append(slot)
        current_time += timedelta(hours=1)
    
    return slots

# def generate_slots(opening_time, closing_time):
#     slots = []
#     print(opening_time,closing_time)
    
#     # Convert 12-hour format strings to datetime objects
#     opening_time = datetime.strptime(opening_time, "%I:%M %p")
#     closing_time = datetime.strptime(closing_time, "%I:%M %p")

#     current_time = opening_time
#     while current_time < closing_time:
#         slot = f"{current_time.strftime('%I:%M %p')} - {(current_time + timedelta(hours=1)).strftime('%I:%M %p')}"
#         slots.append(slot)
#         current_time += timedelta(hours=1)
    
#     return slots

def ShowSlots(request,id):
    salon = SalonMst.objects.get(id = id)
    servies = SelectedServicemsMst.objects.filter(SalonId = id)
    time_slots = generate_slots(salon.OpenTime, salon.CloseTime)
    print(time_slots)
    return render(request,'BookingForm.html',{'slots':time_slots,"salon":salon,"services":servies})


def SendEmail(email,password):
    subject = 'Welcome to the Family of Hari Harmony'
    message = f"""Dear User,
    
This is a confirmation that your password for your Hari Harmony account was successfully changed. If you made this change, no further action is required.

If you didn’t make this change, your account may be compromised. Please reset your password immediately using the following link:

www.hariharmony.com/reset-password

To keep your account secure:
- Never share your password with anyone.
- Use a strong, unique password for your account.

If you have any questions or need assistance, feel free to contact us at support@hariharmony.com.

Stay secure,  
The Hari Harmony Team  
www.hariharmony.com | Contact Support
"""
    email_from = settings.EMAIL_HOST_USER  # Sender email
    recipient_list = ["dhurvraj142@gmail.com"]  # Recipient email
    if send_mail(subject, message, email_from, recipient_list):
        print("Email sent successfully")
    return redirect('IndexView')


def RegistrationEmail(email,name):
    subject = 'Welcome to the Family of Hari Harmony'
    message = f"""Dear {name},
    
Welcome to Hari Harmony! We’re thrilled to have you as part of our community. Your account has been successfully registered, and you're all set to explore the features and benefits we offer.

Here’s what you can do next:
- Discover Features: Browse through our platform to get familiar with all we offer.
- Stay Connected: Keep an eye on upcoming events, announcements, and exclusive content.
- Get Support: Our team is always here to assist you whenever you need help.

If you have any questions or need assistance, feel free to contact us at support@hariharmony.com.

Thank you for choosing Hari Harmony! We look forward to supporting you on your journey.

Warm regards,  
The Hari Harmony Team  
www.hariharmony.com | Contact Support
"""
    email_from = settings.EMAIL_HOST_USER  # Sender email
    recipient_list = [email]  # Recipient email
    if send_mail(subject, message, email_from, recipient_list):
        print("Email sent successfully")
    return redirect('IndexView')


def send_appointment_confirmation_email(user_email, user_name, services, date, time, location, total):
    subject = "Your Salon Appointment is Confirmed – Hari Harmony"
    
    # Creating bill details dynamically
    
    message = f"""Dear {user_name},

Thank you for booking your salon appointment with Hari Harmony! We are excited to provide you with the best service. Below are the details of your appointment:

📅 Appointment Details:
- Service(s) Booked: {", ".join(services)}
- Date & Time: {date} at {time}
- Salon Location: {location}

💳 Bill Summary:

Total Amount: ₹{total}


📌 Important Information:
✔️ Please arrive 10 minutes early to ensure a smooth experience.
✔️ In case of any changes, you can reschedule or cancel your appointment here: www.hariharmony.com/reschedule
✔️ If you have any questions, feel free to contact us at support@hariharmony.com.

We look forward to serving you!

Best regards,
The Hari Harmony Team
🌐 www.hariharmony.com | 📞 +91-XXXXXXXXXX
"""
    email_from = settings.EMAIL_HOST_USER  # Sender email
    recipient_list = [user_email]  # Recipient email
    if send_mail(subject, message, email_from, recipient_list):
        print("Email sent successfully")
    return redirect('IndexView')
