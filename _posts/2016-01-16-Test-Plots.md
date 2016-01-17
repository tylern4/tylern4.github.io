---
layout: post
title: Test Plots
tags: [code]
modified: 2016-01-16
---

Livingston plots: 
![Energy_plot](/PDFs/acc_logE.pdf "Energy Plot")
![Lum_plot](/PDFs/acc_LogLum.pdf "Luminosity Plot")


```python 
#!/usr/local/bin/ipython
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import json

fig_size = (16, 9)
fig = plt.figure(num=None, figsize=fig_size, dpi=200, facecolor='w', edgecolor='k')

with open('acc.json') as data_file:
    data = json.load(data_file)

df_acc = pd.DataFrame(data["Accelerator"])
df_lum = pd.DataFrame(data["Luminosity"])
df_acc['logE'] = df_acc["Energy_MeV"].apply(np.log)
df_lum['logLum'] = df_lum["Lum_per_cm2s"].apply(np.log)
types_acc = np.hstack(np.array(df_acc['Type']))
types_lum = np.hstack(np.array(df_lum['Type']))

uniq_acc = np.unique(types_acc)
values = cm.rainbow(np.linspace(0,1,len(uniq_acc)))
col = dict(zip(uniq_acc, values))

for i,acc in zip(xrange(len(uniq_acc)),uniq_acc):
    temp = df_acc[df_acc['Type'] == acc]
    year = np.hstack(np.array(temp['Year']))
    logE = np.hstack(np.array(temp['logE']))
    plt.scatter(year, logE, alpha=1,color=col[acc],label=r'%s' %(acc))

plt.xlabel(r'Year')
plt.ylabel(r'Log of Energy')
plt.legend(loc=4)
#plt.show()
plt.savefig("acc_logE.pdf")

fig = plt.figure(num=None, figsize=fig_size, dpi=200, facecolor='w', edgecolor='k')
uniq_lum = np.unique(types_lum)
values = cm.rainbow(np.linspace(0,1,len(uniq_lum)))
col = dict(zip(uniq_lum, values))

for i,acc in zip(xrange(len(uniq_lum)),uniq_lum):
    temp = df_lum[df_lum['Type'] == acc]
    year = np.hstack(np.array(temp['Year']))
    LogLum = np.hstack(np.array(temp['logLum']))
    plt.scatter(year, LogLum, alpha=1,color=col[acc],label=r'%s' %(acc))

plt.xlabel(r'Year')
plt.ylabel(r'Log Luminosity')
plt.legend(loc=4)
#plt.show()
plt.savefig("acc_LogLum.pdf")
```