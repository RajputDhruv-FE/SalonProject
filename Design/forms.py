from . models import CityMst,AreaMst,UserMst,ServiceMst,SalonMst,SelectedServicemsMst,ImageMst,SlotBookingMst
from django import forms

class CityForm(forms.ModelForm):
    class Meta:
        model=CityMst
        fields="__all__"


class AreaForm(forms.ModelForm):
    class Meta:
        model=AreaMst
        fields="__all__"
    def __init__(self,*args,**kwargs):
        super(AreaForm, self).__init__(*args,**kwargs)
        self.fields['CityName'].empty_label = "--Select city name--"


class UserForm(forms.ModelForm):
    choices = [('Owner','Owner'), ('User', 'User')]
    Usertype = forms.ChoiceField(choices=choices,widget=forms.Select(attrs={'class':'form-control'}))
    Password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','pattern': '^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,}$','title':'Password must contain at least 8 characters, including UPPER/lowercase , special symbols and numbers'}))
    # PhoneNumber = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),min_length=10,max_length=10,)
    PhoneNumber = forms.CharField(
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': '10',
        'maxlength': '10',
        'pattern': '[0-9]{10}',
        'inputmode': 'numeric',
        'placeholder': 'Enter 10-digit phone number',
        'title':'Please enter a valid 10-digit phone number'
    })
)

    class Meta:
        model=UserMst
        fields=['Name','UserName','Email','PhoneNumber','Password','Usertype','Img']
    def __init__(self,*args,**kwargs):
        super(UserForm, self).__init__(*args,**kwargs)
        self.fields['Usertype'].empty_label = "--Select Usertype--"\
        

class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceMst
        fields = "__all__"


class SalonForm(forms.ModelForm):
    choices = [('Male', 'Male'), ('Female', 'Female'),('Unisex', 'Unisex')]
    Type = forms.ChoiceField(choices=choices,widget=forms.Select(attrs={'class':'form-control'}))
    OpenTime = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time',}))
    CloseTime = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time',}))


    class Meta:
        model = SalonMst
        fields = ['Name','Location','Area','City','OpenTime','CloseTime','NumberOfSeats','Type','Img']
    def __init__(self,*args,**kwargs):
        super(SalonForm, self).__init__(*args,**kwargs)
        self.fields['Area'].empty_label = "--Select Area--"
        self.fields['City'].empty_label = "--Select City--"
        self.fields['OpenTime'].empty_label = "--Select Open Time--"
        self.fields['CloseTime'].empty_label = "--Select Close Time--"
        self.fields['Type'].empty_label = "--Select Type--"


class SelectServicesForm(forms.ModelForm):
    class Meta:
        model = SelectedServicemsMst
        fields = ['ServiceName','Price']
        

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageMst
        fields = ['Img']  # Only include the `image` field

class BookingForm(forms.ModelForm):
    BookingDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    BookingTime = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time',}))
    class Meta:
        model = SlotBookingMst
      
        fields = ['BookingDate','BookingTime','ServiceId']



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserMst
        fields = ['Name', 'UserName', 'Email', 'PhoneNumber', 'Img']

    def clean_PhoneNumber(self):
        phone = self.cleaned_data.get('PhoneNumber')
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone
    
from django import forms
from .models import SalonMst  # Import your model

class EditSalonForm(forms.ModelForm):
    class Meta:
        model = SalonMst
        fields = [
            'Name', 'Location', 'Img', 
            'NumberOfSeats', 'Area', 'City', 'OpenTime', 'CloseTime', 'Type'
        ]

    def clean_NumberOfSeats(self):
        seats = self.cleaned_data.get('NumberOfSeats')
        if seats <= 0:
            raise forms.ValidationError("Number of seats must be greater than zero.")
        return seats

