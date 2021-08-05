from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages

import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import *

from FuturePlanning.models import MySettings,c_Familys,c_Records
from FuturePlanning.forms import DelC_Records,NewC_RecordForm
from . import myconfig

# create dataframe that its columns start from start date till end date
# add a raw with total to the df
def f_create_dataframe(Start,End):
    #create list of dates with date python object from
    #start to end date interval month
    dates_list = pd.date_range(Start, End, freq='MS').strftime('%m %Y')
    #create pandas data frame object with the list of dates and "Total" Row
    df = pd.DataFrame(columns = dates_list,  index = ['Total'])

    return df,dates_list
#######################################################################
def f_build_df_from_db(Rec_Type,Current_Family,Table_Month_List,In_Df):
    # Quary familys that have name from the first family (got from above calling with Fam_id=1)
    family_in_records=c_Records.objects.all().filter(Family__Fam_name=Current_Family).filter(Rec_Type=Rec_Type)
    for elemnt in family_in_records:

        data_dates = pd.date_range(elemnt.Start_Date, elemnt.End_Date, freq='MS').strftime('%m %Y').tolist()
        value_list=[]
        for month in Table_Month_List:
            if month in data_dates:
                value_list.append(int(elemnt.Value))
            else:
                value_list.append(0)
        index_length=(len(In_Df))
        line = pd.DataFrame({},index=[elemnt.Rec_Name])
        In_Df = pd.concat([In_Df.iloc[:index_length-1], line, In_Df.iloc[index_length-1:]])

        i=0
        for month in Table_Month_List:
            In_Df[month][elemnt.Rec_Name]=value_list[i]
            i=i+1
            x=In_Df[:-1][month].sum()
            In_Df[month]["Total"] = x
    return In_Df
#****************************************************************************
g_record_to_edit=c_Records.objects.all()
print("fffff",g_record_to_edit)
#Global Variable to hold the start date of the simulation
g_start=""
#Global Variable to hold the end date of the simulation
g_end=""
#Read from DB the setting parameters per version request

g_my_settings = MySettings.objects.all().filter(simulation_version=1)[0]

#Set the global variable for the start and end of the simulation based on the settings

g_start=g_my_settings.simulation_start_date

g_end=g_my_settings.simulation_end_date

g_current_family=c_Familys.objects.all().filter(Fam_name="Ofir")

def v_f_index(request):

    global g_current_family
    #Create an empty adataframe object for the incomes and return df and month list
    (g_income_table_df,g_table_month_list) = f_create_dataframe(g_start,g_end)

    #Create an empty adataframe object for the Expanse and return df and month list
    (g_expanse_table_df,g_table_month_list) = f_create_dataframe(g_start,g_end)

    # set the current family to fam_id==1 from the DB
    # in the future will be changed from the user input
    # g_current_family=Familys.objects.all().filter(Fam_id=1)
    # build in come df from db records

    df_in=f_build_df_from_db(myconfig.g_types_list[0][0],g_current_family[0].Fam_name,g_table_month_list,g_income_table_df)

    # build expanse df from db records
    df_exp=f_build_df_from_db(myconfig.g_types_list[1][0],g_current_family[0].Fam_name,g_table_month_list,g_expanse_table_df)

    #transfer in comes df to html string
    income_table_string = df_in.to_html(classes="table table-striped table-bordered table-responsivek",table_id="tInTable")

    #transfer expanse df to html string
    expanse_table_string = df_exp.to_html(classes="table table-striped table-bordered table-responsivek",table_id="tExpTable")

    in_index_length=(len(df_in))
    exp_index_length=(len(df_exp))

    dates_list_plotly = pd.date_range(g_start, g_end, freq='MS').strftime('%Y-%m').tolist()

    my_dict = {'InTable':income_table_string,
               'ExpTable':expanse_table_string,
               'FamName':g_current_family[0].Fam_name,
               'IncomeYAxies':df_in.iloc[in_index_length-1].tolist(),
               'IncomeXAxies':dates_list_plotly,
               'ExpYAxies':df_exp.iloc[exp_index_length-1].tolist(),
               'ExpXAxies':dates_list_plotly
               }
    return render(request,'FuturePlanning/v_f_index.html',context=my_dict)
# ********************************************************************************
def form_name_view(request):
    global g_current_family
    form = forms.FormName()
    if request.method == 'POST':
        form = forms.FormName(request.POST)

        if form.is_valid():

            print("Family_Name: "+form.cleaned_data['family_name'])
            g_current_family=c_Familys.objects.all().filter(Fam_id=int(form.cleaned_data['family_name']))
            return redirect(v_f_index)


    return render(request,'FuturePlanning/form_page.html',{'form':form})


def v_f_new_c_record(request):
    error_list=[]
    form = NewC_RecordForm()

    if request.method == "POST":

        form = NewC_RecordForm(request.POST)

        if form.is_valid():

            current_family=g_current_family[0].Fam_name
            record_type=form.cleaned_data['Rec_Type']
            records_list=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=record_type)
            name_list=[]
            for element in records_list:
                name_list.append(element.Rec_Name)
            print("name list:")
            print(name_list)
            print("name to insert:")
            print(form.cleaned_data['Rec_Name'])
            print (form.cleaned_data['Rec_Name'] not in name_list)
            if (form.cleaned_data['Rec_Name'] not in name_list):
                form.save(commit=True)
                return redirect("index")
            else:
                error_list.append("record name already exist in DB")
        else:
            print('ERROR FORM INVALID')
            error_list.append("for not valid")

    return render(request,'FuturePlanning/v_f_new_c_record.html',{'c_record_form':form,'erros':error_list})

def v_f_del_c_record(request):

    error_list=[]
    form = DelC_Records()
    current_family=g_current_family[0].Fam_name

    records_list=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=myconfig.g_types_list[0][0])
    in_name_list=[]
    for element in records_list:
        in_name_list.append(element.Rec_Name)
    records_list=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=myconfig.g_types_list[1][0])
    exp_name_list=[]
    for element in records_list:
        exp_name_list.append(element.Rec_Name)
    if request.method == "POST":
        print("in post del",request.POST)
        form = DelC_Records(request.POST)

        if form.is_valid():
            current_family=g_current_family[0].Fam_name

            record_type=form.cleaned_data['Rec_Type']
            if (record_type == myconfig.g_types_list[0][0]) :
                record_name=in_name_list[form.cleaned_data['Rec_Name']]
            if (record_type == myconfig.g_types_list[1][0]):
                record_name=exp_name_list[form.cleaned_data['Rec_Name']]
            print(record_name)
            record_to_delete=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=record_type).filter(Rec_Name=record_name)
            if len(record_to_delete)==1:
                record_to_delete[0].delete()
                return redirect("index")
                # return index(request)
            else:
                if len(record_to_delete)==0:
                    error_list.append("no record found")
                else:
                    if len(record_to_delete)>1:
                        error_list.append("There is more then one record with this name, contact admin")
                    else:
                        error_list.append("fatak error, contact admin")

        else:
            print('ERROR FORM INVALID')

    return render(request,'FuturePlanning/v_f_del_c_record.html',{'del_c_record_form':form,'erros':error_list,'Indata':in_name_list,'Expdata':exp_name_list })


def v_f_edit_c_record(request):
        global g_record_to_edit
        error_list=[]
        form = DelC_Records()
        current_family=g_current_family[0].Fam_name

        records_list=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=myconfig.g_types_list[0][0])
        in_name_list=[]
        for element in records_list:
            in_name_list.append(element.Rec_Name)

        records_list=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=myconfig.g_types_list[1][0])
        exp_name_list=[]
        for element in records_list:
            exp_name_list.append(element.Rec_Name)
        print("if post",request.method)
        if request.method == "POST":
            print("in post",request.POST)
            print(request)
            form = DelC_Records(request.POST)
            if form.is_valid():
                current_family=g_current_family[0].Fam_name

                record_type=form.cleaned_data['Rec_Type']
                if (record_type == myconfig.g_types_list[0][0]) :
                    record_name=in_name_list[form.cleaned_data['Rec_Name']]
                if (record_type == myconfig.g_types_list[1][0]):
                    record_name=exp_name_list[form.cleaned_data['Rec_Name']]
                g_record_to_edit=c_Records.objects.all().filter(Family__Fam_name=current_family).filter(Rec_Type=record_type).filter(Rec_Name=record_name)
                print("barak g_record in edit view:",g_record_to_edit)
                return redirect("edit_record_data")
            else:
                error_list.append("no record found")

        return render(request,'FuturePlanning/v_f_edit_c_record.html',{'del_c_record_form':form,'erros':error_list,'Indata':in_name_list,'Expdata':exp_name_list })


def v_f_edit_c_record_data(request):
    global g_record_to_edit
    error_list=[]
    form = NewC_RecordForm(instance=g_record_to_edit[0])
    if request.method == "POST":
        form = NewC_RecordForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("index")
        else:
                error_list.append("error saving new data")

    return render(request,'FuturePlanning/v_f_new_c_record_edit.html',{'c_record_form':form,'erros':error_list})
