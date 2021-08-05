from django.db import models
from . import myconfig

# Create your models here.
# Setting models for the FuturePlanning app
class MySettings(models.Model):
    #fromat used in the app is "MM YYYY"
    simulation_version = models.PositiveIntegerField(default=1)
    simulation_start_date = models.CharField(max_length=7,default="01 2020")
    simulation_end_date = models.CharField(max_length=7,default="02 2020")
    record_type1 = models.CharField(max_length=7,default="In")
    record_type2 = models.CharField(max_length=7,default="Expanse")
    record_type3 = models.CharField(max_length=7,default="Savings")
    record_type4 = models.CharField(max_length=7,default="Loans")

    def __str__(self):
        return "Setting"


# Famiy is the name of the table in sql
# class Familys(models.Model):
#     Fam_name = models.CharField(max_length=80)
#     Fam_id = models.IntegerField(unique=True)
#
#     # function for printing as a staring our class
#     def __str__(self):
#         return self.Fam_name

# class Records(models.Model):
#     Family = models.ForeignKey(Familys,on_delete=models.CASCADE)
#     # testmy = models.CharField(max_length=50)
#     # type: In Exp Sav Loa Ass
#     Rec_Type = models.CharField(max_length=3,default='In')
#     Rec_Name = models.CharField(max_length=50,default='Name')
#     Start_Date = models.CharField(max_length=20,default='mm_yyyy')
#     End_Date = models.CharField(max_length=20,default='mm_yyyy')
#     Value = models.PositiveIntegerField(default=0)

    # function for printing as a staring our class
    # def __str__(self):
    #     return self.Rec_Name

# Famiy is the name of the table in sql
class c_Familys(models.Model):
    Fam_name = models.CharField(max_length=80,unique=True)



    # function for printing as a staring our class
    def __str__(self):
        return self.Fam_name

DEFAULT_FAMILY_ID = 1
# g_types_list=[("1","In"),("2","Exp"),("3","Savings"),("4","Loans")]

class c_Records(models.Model):
    Family = models.ForeignKey(c_Familys,on_delete=models.CASCADE,default=DEFAULT_FAMILY_ID)
    Rec_Name = models.CharField(max_length=50,default='Name')
    Rec_Type=models.CharField(max_length=7,choices = myconfig.g_types_list,default=myconfig.g_types_list[0])
    Start_Date = models.CharField(max_length=20,default='10 2021')
    End_Date = models.CharField(max_length=20,default='10 2022')
    Value = models.PositiveIntegerField(default=0)
    Rate = models.FloatField(default=1.0)

    # function for printing as a staring our class
    def __str__(self):
        return "rec name:"+self.Rec_Name+" Family:"+self.Family.Fam_name


class c_Events(models.Model):
    Family = models.ForeignKey(c_Familys,on_delete=models.CASCADE,default=DEFAULT_FAMILY_ID)
    Rec_Name = models.CharField(max_length=50,default='Name')
    Rec_Type = models.CharField(max_length=3,default='In')
    Eve_Name = models.CharField(max_length=80)

    def __str__(self):
        return "Event:"+self.Eve_Name+" Family:"+self.Family.Fam_name
