import pandas as pd
import matplotlib.pyplot as plt

"""
#10/26/26 - just looking at demographics so far

df = pd.read_sas("demographics data/DEMO_L.xpt")
print(df.head())


generally important/interesting variables
Age - RIDAGEMN(in monthsunder 24mos), RIDAGEYR(in years, caps at 80),
RIDEXAGM (in months, under 19)

INDFMPIR - Ratio of family income to poverty

DMDBORN4 - country of birth

not quite sure what to do with some of the other ones, such as the household reference
person variables (they start with DM)


print(df["RIDAGEMN"].unique())
print(df.shape)
print(df["RIDAGEMN"].count()) #only 377 individuals under 24mos
print(df.describe())

"""

"""


----------------------------------------------------------



demographic variables used: 
RIDRETH3 (demographics)
DMDBORN4 (country of birth)
BMXWT (weight), age and gender

Socioeconmic status:
DMDEDUC2 - education lvls (adults 20+)
DMDMARTZ (marital status) 
DMDHHSIZ (household size)
INDFMMPC (Family monthly poverty level category)
DR1ILINE (Food/Individual component number)

Food Security:
FSDAD - adult food security category
FSD032C - Household Head couldn't afford balanced meals
FSD041 - Household Head cut/skipped meals
FSD071 - Household Head hungry but didn't eat

Food Assistance:
FSD230 - Does anyone in the household currently receive SNAP benefits?
FSD151 - Emergency Food received



Micro/Macronutrients
-----------------------------------

Energy
DR1TKCAL
Total daily calorie intake

Protein
DR1TPROT
Protein consumed; supports muscles, enzymes, tissue repair

Carbohydrates
DR1TCARB
Total carbohydrate intake; major energy source

Total fat
DR1TTFAT
Total dietary fat; energy and cell function

Total sugars
DR1TSUGR
All dietary sugars, including naturally occurring sugars

Dietary fiber
DR1TFIBE
Nondigestible carbohydrates important for gut and metabolic health

Saturated fat
DR1TSFAT
Type of fat associated with cardiovascular risk when consumed in excess

Monounsaturated fat
DR1TMFAT
Unsaturated fats common in olive oil, nuts, and avocados

Polyunsaturated fat
DR1TPFAT
Fat class that includes essential fatty acids

Cholesterol
DR1TCHOL
Dietary cholesterol from animal foods



Vitamin B9 (folate)
DR1TFDFE
DNA synthesis, red blood cell development

Vitamin B12
DR1TVB12
Nerve function, red blood cell formation

Vitamin C
DR1TVC
Collagen formation, antioxidant defense, iron absorption

Vitamin D
DR1TVD
Calcium absorption and bone health
-----------------------------------------------------




Food insecurity: FSDAD, FSD032C, FSD041, FSD071.
Food assistance: FSD230, FSD151.
Macronutrients: DR1TKCAL, DR1TPROT, DR1TCARB, DR1TTFAT, DR1TFIBE, DR1TCHOL
Micronutrients: DR1TFDFE, DR1TVB12, DR1TVC, DR1TVD.
Socioeconomic and demographic controls: INDFMPIR, DMDEDUC2, DMDHHSIZ, RIDAGEYR, RIAGENDR, RIDRETH3.
Data processing: SEQN, WTDRD1, SDMVSTRA, SDMVPSU, DR1DRSTZ.




Energy
DR1TKCAL
Total daily calorie intake

Protein
DR1TPROT
Protein consumed; supports muscles, enzymes, tissue repair

Carbohydrates
DR1TCARB
Total carbohydrate intake; major energy source

Total fat
DR1TTFAT
Total dietary fat; energy and cell function

Total sugars
DR1TSUGR
All dietary sugars, including naturally occurring sugars

Dietary fiber
DR1TFIBE
Nondigestible carbohydrates important for gut and metabolic health

Saturated fat
DR1TSFAT
Type of fat associated with cardiovascular risk when consumed in excess

Monounsaturated fat
DR1TMFAT
Unsaturated fats common in olive oil, nuts, and avocados

Polyunsaturated fat
DR1TPFAT
Fat class that includes essential fatty acids

Cholesterol
DR1TCHOL
Dietary cholesterol from animal foods



Vitamin B9 (folate)
DR1TFDFE
DNA synthesis, red blood cell development

Vitamin B12
DR1TVB12
Nerve function, red blood cell formation

Vitamin C
DR1TVC
Collagen formation, antioxidant defense, iron absorption

Vitamin D
DR1TVD
Calcium absorption and bone health


Food insecurity: FSDAD, FSD032C, FSD041, FSD071.
Food assistance: FSD230, FSD151.
Macronutrients: DR1TKCAL, DR1TPROT, DR1TCARB, DR1TTFAT, DR1TFIBE, DR1TCHOL
Micronutrients: DR1TFDFE, DR1TVB12, DR1TVC, DR1TVD.
Socioeconomic and demographic controls: INDFMPIR, DMDEDUC2, DMDHHSIZ, 
RIDAGEYR, RIAGENDR, RIDRETH3
Data processing: SEQN, WTDRD1, SDMVSTRA, SDMVPSU, DR1DRSTZ.
"""

demographics = pd.read_sas("demographics data/DEMO_L.xpt")
food_security = pd.read_sas("questionnaire data/quest_FSQ_L.xpt")
intake_d1 = pd.read_sas("dietary data/diet_DR1TOT_L.xpt")
#intake_d2 = pd.read_sas("dietary data/diet_DR2TOT_L.xpt") -might use this later!

#get the vars we need
demographics = demographics[["SEQN", "INDFMPIR", "DMDEDUC2", "DMDHHSIZ", 
                             "RIDAGEYR", "RIAGENDR", "RIDRETH3", "SDMVSTRA", 
                             "SDMVPSU"]]

food_security = food_security[["SEQN", "FSDAD", "FSD032C", "FSD041",
                               "FSD071", "FSD230", "FSD151"]]

intake_d1 = intake_d1[["SEQN", "DR1TKCAL", "DR1TPROT", "DR1TCARB", 
                       "DR1TTFAT", "DR1TFIBE", "DR1TCHOL", "DR1TFDFE", 
                       "DR1TVB12", "DR1TVC", "DR1TVD", "DR1DRSTZ", 
                       "WTDRD1"]]


#1. check null values

print(demographics.isnull().sum()) 
print(food_security.isnull().sum())
print(intake_d1.isnull().sum())

"""
Notes about null values:
- In the demographics file, only two variables have missing values - DMDEDUC2 (Education lvl)
and INDFMPIR (ratio of family income to poverty) - when we need these variables, we will probably 
just remove them. we will look at socioeconomic factors later.

- In the nutrient file, every variable has the same amount of missing values (2166) except for 
dietary recall status (DR1DRSTZ) and day one sample weight (WTDRD1). however, looking at the 
document on the NHANES website, there are many individuals with an incomplete dietary recall 
status. these individuals will be removed.

- In the food security questionnaire, there are a lot of missing values; however, that is due
to the fact that the questionnaire used a skip pattern. The main food security variable is FSDAD, 
so we will focus mainly on this variable, with the others such as FSD032C being used if needed.
The other focus is on food assistance - I believe that FSD151 will be the most important variable

"""

intake_d1_clean = intake_d1.dropna()
intake_d1_clean = intake_d1_clean[(intake_d1_clean["DR1DRSTZ"] == 1) & 
                                  (intake_d1_clean["WTDRD1"] > 0)].copy()
print(intake_d1_clean.shape)

food_security_clean = food_security.dropna(subset = ["FSDAD"])

data = demographics.merge(intake_d1_clean, how = "inner", on = "SEQN")
data = data.merge(food_security_clean, how = "inner", on = "SEQN")
#print(data.shape)
#print(data.columns)
#print(data["SEQN"].nunique()) - no duplicate SEQN values!

#2. Cleaning (with graphs!)

"""
fig, axs = plt.subplots(1, 1, tight_layout=True)

# We can set the number of bins with the *bins* keyword argument.
axs.hist(data["DR1TKCAL"], bins = 10)
#axs[1].hist(dist2, bins = 10)

plt.show()

"""

print(data[data["DR1TKCAL"] == 0].count())
