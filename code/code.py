import pandas as pd

#10/26/26 - just looking at demographics so far

df = pd.read_sas("demographics data/DEMO_L.xpt")
print(df.head())

"""
generally important/interesting variables
Age - RIDAGEMN(in monthsunder 24mos), RIDAGEYR(in years, caps at 80),
RIDEXAGM (in months, under 19)

INDFMPIR - Ratio of family income to poverty

DMDBORN4 - country of birth

not quite sure what to do with some of the other ones, such as the household reference
person variables (they start with DM)
"""

print(df["RIDAGEMN"].unique())
print(df.shape)
print(df["RIDAGEMN"].count()) #only 377 individuals under 24mos
print(df.describe())
print(df["SEQN"].unique())
