from . models import CityMst,AreaMst,UserMst,ServiceMst
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
    class Meta:
        model=UserMst
        fields=['Name','UserName','Email','PhoneNumber','Password','Usertype','Img']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceMst
        fields = "__all__"