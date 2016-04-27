import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
from pandas.tools.plotting import scatter_matrix
from scipy.optimize import curve_fit
from matplotlib.colors import LogNorm

df = pd.read_csv('/Users/tylern/Homework/PHYS723/project/LHC/CMS_data/MuRun.csv')

#Make sure events are neutral
#if first event is positive and the second is negative
#or the second is positive and the first is negative
df1 = df[df.Q1 == 1]
df1 = df1[df1.Q2 == -1]

df2 = df[df.Q1 == -1]
df2 = df2[df2.Q2 == 1]

frames = [df1, df2]

df = pd.concat(frames)
df = df[df.Type1 == 'G']
df = df[df.Type2 == 'G']
#df = df[np.sqrt(df.px1**2 + df.py1**2) + np.sqrt(df.px2**2 + df.py2**2) < 50]

mass_Up = 9.45

def poly(x, c1, c2, c3, c4):
    return c1*x*x*x + c2*x*x + c3*x + c4

def big_poly(x, c1, c2, c3, c4, c5, c6, c7, c8):
    return c8*x**7 + c7*x**6 + c6*x**5 + c5*x**4 + c4*x**3 + c3*x**2 + c2*x + c1

def gaussian(x, mu, sig, const):
    return const * 1/(sig*np.sqrt(2*np.pi)) * np.exp(-(x - mu)**2 / 2*sig**2)

def gaus_poly(x, mu, sig, cont, c1, c2, c3, c4):
    return poly(x, c1, c2, c3, c4) + gaussian(x, mu, sig, cont)

def big_poly_gaus(x, mu, sig, cont, c1, c2, c3, c4, c5, c6, c7, c8):
    return gaussian(x, mu, sig, cont) + big_poly(x, c1, c2, c3, c4, c5, c6, c7, c8)

def chi_2(ys,yknown):
    total = 0
    for i in xrange(len(yknown)):
        temp = (ys[i]-yknown[i])**2.0
        if yknown[i] == 0:
            total += 1
        else :
            total += temp/yknown[i]
    return total/len(yknown)

fig = plt.figure(num=None, figsize=(16,9), dpi=200, facecolor='w', edgecolor='k')
upsilon = df[df.M < 14]
upsilon = upsilon[upsilon.M > 6]
mass = upsilon.M

num_bins = 400

hist, bin_edges = np.histogram(mass,bins=num_bins)
xdata = 0.5*(bin_edges[1:]+bin_edges[:-1])
ydata = hist

plt.hist(mass, num_bins, histtype=u'stepfilled',facecolor='g' , alpha=0.45)

popt_1, pcov_1 = curve_fit(poly, xdata, ydata)
x0 = np.array([9.45,10.7,1,popt_1[0],popt_1[1],popt_1[2],popt_1[3]])
popt_1, pcov_1 = curve_fit(gaus_poly, xdata, ydata,p0=x0)

c2 = chi_2(gaus_poly(xdata, *popt_1),ydata)
plt.plot(xdata,gaus_poly(xdata,*popt_1),'b--', lw=4,
    label=r'$\mathrm{Poly\ bkg\ gaus\ peak\ : \ \chi^{2} = %.4f}$' %(c2))
plt.plot(xdata,poly(xdata,*popt_1[3:]),'g--', lw=4)

signal_line = lambda x : gaus_poly(x,*popt_1) - poly(x, *popt_1[3:])

signal = []
for i in xrange(num_bins):
    temp = ydata[i] - signal_line(xdata[i])
    signal.append(temp)

signal = []
for i in xrange(num_bins):
    temp = ydata[i] - poly(xdata[i],*popt_1[3:])
    signal.append(temp)

plt.xlim((np.min(xdata),np.max(xdata)))
plt.legend(loc=0)
plt.xlabel(r'Mass (GeV)', fontsize=20)
plt.ylabel(r'Counts (#)', fontsize=18)
plt.savefig('U_hist.pdf')


fig = plt.figure(num=None, figsize=(16,9), dpi=200, facecolor='w', edgecolor='k')
ydata = signal
plt.scatter(xdata,ydata,marker='o',color='g')
popt_1, pcov_1 = curve_fit(gaussian, xdata, ydata,p0=[9.45,12,1])
perr_1 = np.sqrt(np.diag(pcov_1))
plt.plot(xdata,gaussian(xdata,*popt_1),'g-', lw=4,
    label=r'$\mathrm{Mass=%.4f \pm %.4f \ GeV,\ \Gamma=%.4f \pm %.4f \ GeV}$' 
    %(popt_1[0], perr_1[0], popt_1[1]*(2.0*np.sqrt(2.0 * np.log(2))), perr_1[1]))

mean,width = popt_1[0],popt_1[1]
sigma = 0.20/3.0 #width*(2.0*np.sqrt(2.0 * np.log(2)))
plt.axvline(x=(mean - 3.0*sigma),color='g')
plt.axvline(x=(mean + 3.0*sigma),color='g')

mean_U = mean
sigma_U = sigma

plt.xlim((np.min(xdata),np.max(xdata)))
plt.xlabel(r'Mass (GeV)', fontsize=20)
plt.ylabel(r'Counts (#)', fontsize=18)
plt.legend(loc=0)
plt.savefig('U_peak.pdf')

signal1 = []
for i in xrange(num_bins):
    temp = ydata[i] - gaussian(xdata[i],*popt_1)
    signal1.append(temp)
    
ydata = signal1
plt.scatter(xdata, signal1,marker='o', color='b')

popt_1, pcov_1 = curve_fit(gaussian, xdata, ydata, p0=[10,10.7,1],maxfev=8000)
perr_1 = np.sqrt(np.diag(pcov_1))

plt.plot(xdata,gaussian(xdata,*popt_1),'b', lw=4,
    label=r'$\mathrm{Mass=%.4f \pm %.4f \ GeV,\ \Gamma=%.4f \pm %.4f}$' 
    %(popt_1[0], perr_1[0], popt_1[1]*(2.0*np.sqrt(2.0 * np.log(2))), perr_1[1]))

mean,width = popt_1[0],popt_1[1]
sigma = 0.30/3.0 #width*(2.0*np.sqrt(2.0 * np.log(2)))

mean_Up = mean
sigma_Up = sigma
plt.axvline(x=(mean - 3.0*sigma),color='b')
plt.axvline(x=(mean + 3.0*sigma),color='b')

plt.xlim((np.min(xdata),np.max(xdata)))
plt.xlabel(r'Mass (GeV)', fontsize=20)
plt.ylabel(r'Counts (#)', fontsize=18)
plt.legend(loc=0)
plt.savefig('Up_peak.pdf')
'''
fig = plt.figure(num=None, figsize=(16,9), dpi=200, facecolor='w', edgecolor='k')

signal1 = []
for i in xrange(num_bins):
    temp = ydata[i] - gaussian(xdata[i],*popt_1)
    signal1.append(temp)
    
ydata = signal1
plt.scatter(xdata, signal1,marker='o', color='b')

popt_1, pcov_1 = curve_fit(gaussian, xdata, ydata, p0=[10,10.7,1],maxfev=80000)

perr_1 = np.sqrt(np.diag(pcov_1))
plt.plot(xdata,gaussian(xdata,*popt_1),'b', lw=4,
    label=r'$\mathrm{Mass=%.4f \pm %.4f \ GeV,\ \Gamma=%.4f \pm %.4f}$' 
    %(popt_1[0], perr_1[0], popt_1[1]*(2.0*np.sqrt(2.0 * np.log(2))), perr_1[1]))

mean,width = popt_1[0],popt_1[1]
sigma = 0.30/3.0 #width*(2.0*np.sqrt(2.0 * np.log(2)))
mean_Up = mean
sigma_Up = sigma

plt.axvline(x=(mean - 3.0*sigma),color='b')
plt.axvline(x=(mean + 3.0*sigma),color='b')

plt.xlim((np.min(xdata),np.max(xdata)))
plt.xlabel(r'Mass (GeV)', fontsize=20)
plt.ylabel(r'Counts (#)', fontsize=18)
plt.legend(loc=0)
plt.savefig('Up_peak.pdf')
'''
Up = df[df.M > (mean_Up - 3.0*sigma_Up)]
Up = Up[Up.M < (mean_Up + 3.0*sigma_Up)]

Up['Upx'] = Up.px1+Up.px2
Up['Upy'] = Up.py1+Up.py2
Up['Upz'] = Up.pz1+Up.pz2
Up['Upt'] = np.sqrt(np.square(Up.Upx) + np.square(Up.Upy))
Up['UE'] = Up.E1+Up.E2

#########################################
fig = plt.figure(num=None, figsize=(16,9), dpi=200, facecolor='w', edgecolor='k')
temp = Up[Up.Upt < 120]
temp = temp[temp.UE < 150]
plt.hist2d(temp.UE,temp.Upt,bins=200,cmap='viridis',norm=LogNorm())
plt.xlabel(r'Energy (GeV)', fontsize=20)
plt.ylabel(r'Transverse Momentum (GeV)', fontsize=20)
plt.colorbar()
plt.savefig('Ue_Upt_log.pdf')
#########################################
#########################################
fig = plt.figure(num=None, figsize=(16,9), dpi=200, facecolor='w', edgecolor='k')
temp = Up[Up.Upt < 30]
temp = temp[temp.UE < 30]
plt.hist2d(temp.UE,temp.Upt,bins=200,cmap='viridis',norm=LogNorm())
plt.xlabel(r'Energy (GeV)', fontsize=20)
plt.ylabel(r'Transverse Momentum (GeV)', fontsize=20)
plt.colorbar()
plt.savefig('Ue_Upt_log_2.pdf')
#########################################
#########################################
fig = plt.figure(num=None, figsize=(16,9), dpi=200, facecolor='w', edgecolor='k')
temp = Up[Up.Upt < 120]
temp = temp[temp.UE < 150]
plt.hist2d(temp.UE,temp.Upt,bins=200,cmap='viridis')#,norm=LogNorm())
plt.xlabel(r'Energy (GeV)', fontsize=20)
plt.ylabel(r'Transverse Momentum (GeV)', fontsize=20)
plt.colorbar()
plt.savefig('Ue_Upt.pdf')
#########################################
#########################################
#fig = plt.figure(num=None, figsize=(16,9), dpi=200, facecolor='w', edgecolor='k')
#temp = Up.drop(['Event','Run','Type1','Type2'],axis=1)
#temp = temp.drop(['E1','px1','py1','pz1','pt1','eta1','phi1','Q1'],axis=1)
#temp = temp.drop(['E2','px2','py2','pz2','pt2','eta2','phi2','Q2'],axis=1)
#scatter_matrix(temp, alpha=0.1, figsize=(20, 15),diagonal='kde')
#plt.savefig('scatter_matrix.jpg')
#########################################
#########################################
fig = plt.figure(num=None, figsize=(16,9), dpi=200, facecolor='w', edgecolor='k')
temp = Up[Up.Upz < 120]
temp = temp[temp.UE < 150]
plt.hist2d(temp.UE,temp.Upz,bins=200,cmap='viridis',norm=LogNorm())
plt.xlabel(r'Energy (GeV)', fontsize=20)
plt.ylabel(r'Z Momentum (GeV)', fontsize=20)
plt.colorbar()
plt.savefig('UE_Upz.pdf')
#########################################

UPp = df[df.M > (mean_U - 3.0*sigma_U)]
UPp = UPp[UPp.M < (mean_U + 3.0*sigma_U)]

UPp['UPpx'] = UPp.px1+UPp.px2
UPp['UPpy'] = UPp.py1+UPp.py2
UPp['UPpz'] = UPp.pz1+UPp.pz2
UPp['UPpt'] = np.sqrt(np.square(UPp.UPpx) + np.square(UPp.UPpy))
UPp['UpE'] = UPp.E1+UPp.E2

#########################################
fig = plt.figure(num=None, figsize=(16,9), dpi=200, facecolor='w', edgecolor='k')
temp = UPp[UPp.UPpt < 120]
temp = temp[temp.UpE < 150]
plt.hist2d(temp.UpE,temp.UPpt,bins=200,cmap='viridis',norm=LogNorm())
plt.xlabel(r'Energy (GeV)', fontsize=20)
plt.ylabel(r'Transverse Momentum (GeV)', fontsize=20)
plt.colorbar()
plt.savefig('UpE_UPpt_log.pdf')
#########################################
#########################################
fig = plt.figure(num=None, figsize=(16,9), dpi=200, facecolor='w', edgecolor='k')
temp = UPp[UPp.UPpt < 120]
temp = temp[temp.UpE < 150]
plt.hist2d(temp.UpE,temp.UPpt,bins=200,cmap='viridis')#,norm=LogNorm())
plt.xlabel(r'Energy (GeV)', fontsize=20)
plt.ylabel(r'Transverse Momentum (GeV)', fontsize=20)
plt.colorbar()
plt.savefig('UpE_UPpt.pdf')
#########################################
#########################################
fig = plt.figure(num=None, figsize=(16,9), dpi=200, facecolor='w', edgecolor='k')
temp = UPp[UPp.UPpz < 120]
temp = temp[temp.UpE < 150]
plt.hist2d(temp.UpE,temp.UPpz,bins=200,cmap='viridis',norm=LogNorm())
plt.xlabel(r'Energy (GeV)', fontsize=20)
plt.ylabel(r'Z Momentum (GeV)', fontsize=20)
plt.colorbar()
plt.savefig('UE_UPpz.pdf')
#########################################
#########################################
fig = plt.figure(num=None, figsize=(16,9), dpi=200, facecolor='w', edgecolor='k')
temp = Up[np.abs(Up.Upz) < 200]
plt.hist(temp.Upz, 100, histtype=u'stepfilled',facecolor='b' , alpha=0.45)
plt.ylabel(r'Counts (#)', fontsize=18)
plt.xlabel(r'Z Momentum (GeV)', fontsize=20)
#plt.colorbar()
plt.savefig('Upz.pdf')
#########################################
#########################################
fig = plt.figure(num=None, figsize=(16,9), dpi=200, facecolor='w', edgecolor='k')
temp = Up[np.abs(Up.Upt) < 20]
plt.hist(temp.Upt, 100, histtype=u'stepfilled',facecolor='b' , alpha=0.45)
plt.ylabel(r'Counts (#)', fontsize=18)
plt.xlabel(r'Transverse Momentum (GeV)', fontsize=20)
#plt.colorbar()
plt.savefig('Upt.pdf')
#########################################