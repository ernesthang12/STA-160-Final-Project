import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

pd.set_option("display.max_columns", None)
#pd.set_option("display.float_format", "{:.2f}".format)

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


Macronutrients
---------------------------------------------------
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


Micronutrients
-------------------------------------------------
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


Variables
-----------------------------------------------------------------------------------------
Food insecurity: FSDAD, FSD032C, FSD041, FSD071.
Food assistance: FSD230, FSD151.
Macronutrients: DR1TKCAL, DR1TPROT, DR1TCARB, DR1TTFAT, DR1TFIBE, DR1TCHOL, DR1TSUGR
Micronutrients: DR1TFDFE, DR1TVB12, DR1TVC, DR1TVD.
Socioeconomic and demographic controls: INDFMPIR, DMDEDUC2, DMDHHSIZ, 
RIDAGEYR, RIAGENDR, RIDRETH3
Data processing: SEQN, WTDRD1, SDMVSTRA, SDMVPSU, DR1DRSTZ.
"""

#1. read in data and get the variables
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
                       "DR1TTFAT", "DR1TFIBE", "DR1TSUGR", "DR1TCHOL", 
                       "DR1TFDFE", "DR1TVB12", "DR1TVC", "DR1TVD", 
                       "DR1DRSTZ", "WTDRD1"]]

"""
print(demographics.isnull().sum()) 
print(food_security.isnull().sum())
print(intake_d1.isnull().sum())

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

#------------------------------------------
#this will be useful for plotting later!
macronutrients = ["DR1TKCAL", "DR1TPROT", "DR1TCARB", "DR1TTFAT", 
                  "DR1TFIBE", "DR1TSUGR", "DR1TCHOL"] 
            

micronutrients = ["DR1TFDFE", "DR1TVB12", "DR1TVC", "DR1TVD"]

nutrients = macronutrients + micronutrients

nutrient_names = {
    "DR1TKCAL": "Calories",
    "DR1TPROT": "Protein",
    "DR1TCARB": "Carbohydrates",
    "DR1TTFAT": "Total Fat",
    "DR1TFIBE": "Fiber",
    "DR1TCHOL": "Cholesterol",
    "DR1TSUGR": "Sugar", 
    "DR1TFDFE": "Folate",
    "DR1TVB12": "Vitamin B12",
    "DR1TVC": "Vitamin C",
    "DR1TVD": "Vitamin D"
}

food_security_labels = [
    "Full",
    "Marginal",
    "Low",
    "Very Low"
]

#------------------------------------------------
#2. check null values and other data cleaning


#remove the rows where DR1TKCAL < 1 (seven cases of 5.397605e-79, seems like missing vals)

intake_d1_clean = intake_d1.dropna()
intake_d1_clean = intake_d1_clean[(intake_d1_clean["DR1DRSTZ"] == 1) & 
                                  (intake_d1_clean["WTDRD1"] > 0) &
                                  (intake_d1_clean["DR1TKCAL"] > 1)].copy()

intake_d1_clean[nutrients] = intake_d1_clean[nutrients].replace(5.397605e-79, np.nan)
#print(intake_d1_clean.shape)
#print(intake_d1_clean[intake_d1_clean["DR1DRSTZ"] != 1])

food_security_clean = food_security.dropna(subset = ["FSDAD"])

data = demographics.merge(intake_d1_clean, how = "inner", on = "SEQN")
data = data.merge(food_security_clean, how = "inner", on = "SEQN")
#print(data.shape)
#print(data.columns)
#print(data["SEQN"].nunique()) - no duplicate SEQN values!

"""
Question - Is food insecurity associated with distinct patterns of nutrient deficiencies?

To answer this question, we should use only the data of individuals who:
- have substantial nutrient data 
- Gave an answer to FSDAD (0 - 10)
- (Bonus) answered if they have or have not ever received emergency food/food stamps
"""

#2. Cleaning (with graphs!)
#print((data["DR1TKCAL"] == 0).sum())
#print(data[data["DR1TKCAL"] <= 100])
#print(data[data["DR1TKCAL"] <= 200].shape)



#------------------------------------------------------
#Graph 1 - pie chart of FSDAD (food security level)
FSDAD_full = data[data["FSDAD"] == 1]["FSDAD"].count()
FSDAD_marginal = data[data["FSDAD"] == 2]["FSDAD"].count()
FSDAD_low = data[data["FSDAD"] == 3]["FSDAD"].count()
FSDAD_vlow = data[data["FSDAD"] == 4]["FSDAD"].count()

FSDAD_data = pd.DataFrame({"Labels": ["Full", "Marginal", "Low", "Very Low"], 
                           "Levels": [FSDAD_full, FSDAD_marginal, FSDAD_low, FSDAD_vlow]})

plt.pie(FSDAD_data["Levels"], labels = FSDAD_data["Labels"], autopct="%1.1f%%")
plt.title("Graph 1 - Percentage of Participants for Each Level of Food Security")
plt.legend()
#plt.savefig("graphs/Graph 1.png")
#plt.show()



#-------------------------------------------------------
#Graph 2: distribution of macronutritient intake
fig, axs = plt.subplots(4, 2, figsize = (13, 17))
fig.tight_layout(rect = [0, 0, 1, 0.94])
axs = axs.flatten()

for i, col in enumerate(macronutrients):
    axs[i].hist(data[col], bins = 20)
    axs[i].set_title(f"{col} ({nutrient_names[col]})")
    axs[i].axvline(np.mean(data[col]), color = 'red', linestyle = 'dashed', linewidth = 2)

plt.suptitle("Graph 2 - Distribution of Intake of Macronutrients")
plt.savefig("graphs/Graph 2.png")
#plt.show()



#--------------------------------------------------
#Graph 3: distribution of micronutrient intake

fig, axs = plt.subplots(2, 2, figsize = (13, 17))
fig.tight_layout(rect=[0, 0, 1, 0.94])
axs = axs.flatten()

for i, col in enumerate(micronutrients):
    axs[i].hist(data[col], bins = 20)
    axs[i].set_title(f"{col} ({nutrient_names[col]})")
    axs[i].axvline(np.mean(data[col]), color = 'red', linestyle = 'dashed', linewidth = 2)

plt.suptitle("Graph 3 - Distribution of Intake of Micronutrients")
plt.savefig("graphs/Graph 3.png")
#plt.show()



#--------------------------------------------------------------
#Graph 4: Boxplots of macronutrients based on FSDAD category
fig, axs = plt.subplots(4, 2, figsize = (13, 17))
fig.tight_layout(rect=[0, 0, 1, 0.94])
axs = axs.flatten()

for i, col in enumerate(macronutrients):
    sns.boxplot(
        data = data,
        x = "FSDAD",
        y = col,
        ax = axs[i]
    )

    axs[i].set_title(f"{col} ({nutrient_names[col]})")
    axs[i].set_xlabel("Food Security Category")
    axs[i].set_xticklabels(food_security_labels)
    axs[i].set_ylabel("Daily Intake")

for i in range(len(macronutrients), len(axs)):
    axs[i].set_visible(False)

fig.subplots_adjust(hspace = 0.5, wspace = 0.2)
fig.suptitle("Graph 4 - Macronutrient Intake by Food Security Status", fontsize = 18)
plt.savefig("graphs/Graph 4.png")
#plt.show()



#----------------------------------------------------------------
#Graph 5: Boxplots of micronutrients based on FSDAD category
fig, axs = plt.subplots(2, 2, figsize = (13, 17))
fig.tight_layout(rect = [0, 0, 1, 0.94])
axs = axs.flatten()

for i, col in enumerate(micronutrients):
    sns.boxplot(
        data = data,
        x = "FSDAD",
        y = col,
        ax = axs[i]
)
    
    axs[i].set_title(f"{col} ({nutrient_names[col]})")
    axs[i].set_xlabel("Food Security Category")
    axs[i].set_xticklabels(food_security_labels)
    axs[i].set_ylabel("Daily Intake")

fig.subplots_adjust(hspace = 0.2, wspace = 0.2)
fig.suptitle("Graph 5 - Micronutrient Intake by Food Security Status", fontsize = 18)
plt.savefig("graphs/Graph 5.png")
#plt.show()



#--------------------------------------
#Graph 6 - Boxplots of Nutrients based on FSDAD category (not showing outliers)
fig, axs = plt.subplots(3, 4, figsize = (13, 17))
fig.tight_layout(rect = [0, 0, 1, 0.94])
axs = axs.flatten()

for i, col in enumerate(nutrients):
    sns.boxplot(
        data = data,
        x = "FSDAD",
        y = col,
        ax = axs[i],
        showfliers = False
)
    
    axs[i].set_title(f"{col} ({nutrient_names[col]})")
    axs[i].set_xlabel("Food Security Category")
    axs[i].set_xticklabels(food_security_labels)
    axs[i].set_ylabel("Daily Intake")


for i in range(len(nutrients), len(axs)):
    axs[i].set_visible(False)

fig.subplots_adjust(hspace = 0.2, wspace = 0.4)
fig.suptitle("Graph 6 - Micronutrient Intake by Food Security Status (Zoomed in)", fontsize = 18)
plt.savefig("graphs/Graph 6.png")
#plt.show()



#-----------------------------------------
#Graph 7: Correlation Heatmap between Food Security (FSDAD) and Nutrients
corr_columns = nutrients + ["FSDAD"]
corr_data = data[corr_columns]
corr = corr_data.corr()

plt.figure(figsize = (10, 10))
heatmap = sns.heatmap(corr, annot = True)
plt.title("Graph 7 - Correlation Heatmap of Food Security Levels and Nutrient Intake")
plt.savefig("graphs/Graph 7.png")
plt.show()

