#!/usr/bin/env/python
#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from astropy.timeseries import LombScargle
import csv

#Coloque aquí el tipo de estrella con el que se va a trabajar. OPCIONES= 'Cefeida', 'RR_Lyrae', 'BinariaECL'.
tipo_estrella='BinariaECL';

if tipo_estrella=='Cefeida' or tipo_estrella==1:
	label_path='Datos/'+'1_Cefeidas'+'/I/OGLE-LMC-CEP-';
elif tipo_estrella=='RR_Lyrae' or tipo_estrella==2:
	label_path='Datos/'+'2_RR_Lyrae'+'/I/OGLE-LMC-RRLYR-';
else:
	label_path='Datos/'+'3_BinariasEclipsantes'+'/I/OGLE-LMC-ECL-';
#fin if 

numero_estrella='05084';
extension='.dat';


vint=np.vectorize(np.int);
def transformar_ts(tp,t0,t_datos):
	phi_raw=(1/tp)*(t_datos-t0);
	phi=phi_raw-vint(phi_raw);
	return phi;
# fin transformar phis

tpini=0.4;
tpfin=500;
Finura=100000;
freq_ini=1/tpfin;
freq_fin=1/tpini;
v_freq=np.linspace(freq_ini,freq_fin,Finura);
indiceMayor=1;

lista_estrellas=[];
lista_periodos=[];

#IMPORTAR DAROS DEL ARCHIVO Y. 
elSeniorArchivo=label_path+numero_estrella+extension;
datos=np.genfromtxt(elSeniorArchivo,delimiter=' ');
t_dat=datos[:,0];
us=datos[:,1];
desv=datos[:,2];
tini=t_dat[0];
#LOMB-SCARGLE****************************************
#frecuencias, potencias = LombScargle(t_dat,us).autopower(nyquist_factor=50);
potencias=LombScargle(t_dat,us).power(v_freq);
frecuencias=v_freq;
#*******************************************************
pos=potencias.argsort()[-indiceMayor];
freq_mayor=frecuencias[pos];
tp_estrella=2/freq_mayor;
fig=plt.figure()
ax0=fig.add_subplot(111);
ax0.plot(frecuencias,potencias);
ax0.set_xlabel("Frecuencia en dias^-1");
ax0.set_ylabel("Potencia periodograma Lomb-Scargle");
nombreFoto="Periodograma_LS"+tipo_estrella+"-"+numero_estrella+".png";
plt.savefig(nombreFoto);
plt.close(fig);
phis=transformar_ts(tp_estrella,t_dat[0],t_dat);
phis1=phis+1;
phisG=np.r_[phis,phis1];
usG=np.r_[us,us];
fig1=plt.figure();
ax1=fig1.add_subplot(111);
ax1.scatter(phisG,usG);
ax1.set_ylim(ax1.get_ylim()[::-1]);
ax1.set_xlabel("fase");
ax1.set_ylabel("Magnitud");
nombreFoto2="LS_Curva_de_luz_de_"+tipo_estrella+"-"+numero_estrella+".png";
plt.savefig(nombreFoto2);
plt.close(fig1);
LabelEstrella="Estella_"+tipo_estrella+"_"+numero_estrella+"_LS";
print("El periodo con el pico de índice ",indiceMayor," corresponde a un periodo de: ",tp_estrella," días");
