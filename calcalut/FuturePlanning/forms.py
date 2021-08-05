from django import forms
# from django.core import validators
from FuturePlanning.models import c_Records

from django.forms import Textarea,CharField
from . import myconfig

# g_current_family=Familys.objects.all().filter(Fam_id=1)
# fam_1 = g_current_family[0].Fam_name
# g_current_family=Familys.objects.all().filter(Fam_id=2)
# fam_2 = g_current_family[0].Fam_name

# g_types_list=[("1","In"),("2","Exp"),("3","Savings"),("4","Loans")]

class DelC_Records(forms.Form):
    # Rec_Type = forms.CharField(max_length=3)
    # Rec_Type=forms.ChoiceField(choices = g_types_list,)
    Rec_Type=forms.ChoiceField(choices = myconfig.g_types_list,widget=forms.Select(attrs={'onchange':"myFunction1();"}))
    # Rec_Name = forms.CharField(max_length=50)

    Rec_Name = forms.IntegerField(widget=forms.Select(attrs={'onchange':"myFunction();"}))


    # widgets = {
    #     'Rec_Name': Textarea(attrs={'cols': 80, 'rows': 20,'onchange':"myFunction();"}),
    # }

class NewC_RecordForm(forms.ModelForm):

    class Meta():
        model = c_Records
        fields = '__all__'


# FAMILY_CHOICES =(
#     ("1",fam_1),
#     ("2", fam_2),
# )
# class FormName(forms.Form):
#
#     family_name = forms.ChoiceField(choices = FAMILY_CHOICES)
