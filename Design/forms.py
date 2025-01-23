from . models import CityMst,AreaMst,UserMst,ServiceMst,SalonMst,SelectedServicemsMst,ImageMst
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
    class Meta:
        model=UserMst
        fields=['Name','UserName','Email','PhoneNumber','Password','Usertype','Img']
    def __init__(self,*args,**kwargs):
        super(UserForm, self).__init__(*args,**kwargs)
        self.fields['Usertype'].empty_label = "--Select Usertype--"

class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceMst
        fields = "__all__"

class SalonForm(forms.ModelForm):
    choices = [('Male', 'Male'), ('Female', 'Female'),('Unisex', 'Unisex')]
    Type = forms.ChoiceField(choices=choices,widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = SalonMst
        fields = ['Name','Location','Area','City','OpenTime','CloseTime','Type','Img']
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

