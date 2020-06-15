import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# s = pd.Series([1, 3, 5, np.nan, 6, 8], name='mynams')
# dates = pd.date_range('20130101', periods=6)

country_list = ['Germany', 'France', 'Spain', 'Italy']
df = pd.DataFrame(np.random.randn(4, 6), columns=list('ABCDEF'))
df['Country'] = country_list

# print("!!!!! Before setting the index")
# print(df)
# print("\n")
# print(df['A'])
# print("\n")

# myindex = df[ df['Country'] == 'Germany'].index
# print("myindex = " + "df[ df['Country'] == 'Germany'].index" + "=" + str(myindex))
# # dfa2 = df.loc[ df[ df['Country'] == 'Germany' ].index , : ]
# dfa2 = df.loc[ myindex[0] , : ]
# print("df.loc[ myindex[0] , : ]")
# print(dfa2)
# print("\n")

dfa3 = df.loc[ df[df['Country'] == 'Germany'].index , : ]   #overkill in this case
dfa4 = df.loc[ df['Country'] == 'Germany' , : ]             # BEST?!
dfa6 = df[ df['Country'] == 'Germany' ]                     #OK..
print(dfa3)
print(dfa4)
print(dfa6)
# print("\n")

# dfa4 = df.loc[ 0: 2 ]
# print(dfa4)
# dfa5 = df[ 0:3 ]  # ugly confusing, do not use!
# print(dfa5)
# print(dfa4 == dfa5)
# print("\n")

# ##############
print("!!!!! After setting the index")
df.set_index('Country', inplace=True)
# print(df)
# print("\n")
# print(df['A'])
# print("\n")
# dfb7 = df[ ['A','C'] ]  # OK.. still prefer loc
# print(dfb7)
# dfb2 = df.loc[ 'Germany' , : ]
# print(dfb2)
# print("\n")
# dfb3 = df.loc[ ['Germany'] , : ]
# print(dfb3)
# print("\n")

dfb4 = df.loc[ 'Germany': 'Spain', : ]  # OK
dfb5 = df.loc[ ['Germany','Spain'], : ] # OK
dfb6 = df[ 'Germany': 'Spain' ]         # TODO: UGLY confusing, do not use!
print(dfb4)
print(dfb5)
print(dfb6)
print("\n")

exit(0)