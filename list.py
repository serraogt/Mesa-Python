    # required packages: pandas, openpyxl

    #--- import section -------------------------------------------------
import pandas 

    #--- create file variable: ------------------------------------------

my_excel_file = "PopulatioDataEncoded.xlsx"

    #--- create lists: --------------------------------------------------
df = pandas.read_excel(my_excel_file)

    # with header:
my_list = (list)(df["Ethnic Group"].values)

    # without header:
my_second_list = (list)(df[df.columns[11]].values)

print(len(my_second_list))
 
for my_item in my_second_list:
        print(my_item, end ="\n ") 