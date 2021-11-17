#!/usr/bin/env/python
#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from astropy.timeseries import LombScargle
import csv

#Coloque aquí el tipo de estrella con el que se va a trabajar. OPCIONES= 'Cefeida', 'RR_Lyrae', 'BinariaECL'.
tipo_estrella='Cefeida';
opcion=0;

#Importar los números de las estrellas desde el archivo csv:
ID_estrellas=np.loadtxt('numero_estrellas.csv',delimiter=',',dtype='str', skiprows=1);

vecCep=ID_estrellas[:,0];
vecRRLyr=ID_estrellas[:,1]; 
vecECL=ID_estrellas[:,2];

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if tipo_estrella=='Cefeida' or tipo_estrella==1:
	if opcion==2:
		label_path='DatosRem/1_Cefeidas/OGLE-LMC-CEP-';
	else:
		label_path='Datos/'+'1_Cefeidas'+'/I/OGLE-LMC-CEP-';
	#fin if 
	numero_estrella=vecCep;
elif tipo_estrella=='RR_Lyrae' or tipo_estrella==2:
	if opcion==2:
		label_path='DatosRem/2_RR_Lyrae/OGLE-LMC-RRLYR-';
	else:
		label_path='Datos/'+'2_RR_Lyrae'+'/I/OGLE-LMC-RRLYR-';
	#fin if 
	numero_estrella=vecRRLyr;
else:
	if opcion==2:
		label_path='DatosRem/3_BinariasEclipsantes/OGLE-LMC-ECL-';
	else:
		label_path='Datos/'+'3_BinariasEclipsantes'+'/I/OGLE-LMC-ECL-';
	#fin if 
	numero_estrella=vecECL;
#fin if 
extension='.dat';
#-----------------------verificar que existen los archivos--------------------------
# ~ for k in range(len(numero_estrella)):
	# ~ elSeniorArchivo=label_path+numero_estrella[k]+extension;
	# ~ datos=np.genfromtxt(elSeniorArchivo,delimiter=' ');
	
# ~ #fin for 
# ~ print("EXISTEN");
#---------------------------------------------------------------------------------------------------

vint=np.vectorize(np.int);
def transformar_ts(tp,t0,t_datos):
	phi_raw=(1/tp)*(t_datos-t0);
	phi=phi_raw-vint(phi_raw);
	return phi;
# fin transformar phis

tpini=0.4;
tpfin=200;
Finura=100000;
freq_ini=1/tpfin;
freq_fin=1/tpini;
v_freq=np.linspace(freq_ini,freq_fin,Finura);

N_mult=np.genfromtxt("IndicesMult.csv", delimiter=",", skip_header=1);
N_mult_LS=N_mult[:,0];

lista_estrellas=[];
lista_periodos=[];
for k in range(len(numero_estrella)):
	
	#IMPORTAR DAROS DEL ARCHIVO Y. 
	elSeniorArchivo=label_path+numero_estrella[k]+extension;
	datos=np.genfromtxt(elSeniorArchivo,delimiter=' ');
	t_dat=datos[:,0];
	us=datos[:,1];
	desv=datos[:,2];
	tini=t_dat[0];
	#LOMB-SCARGLE****************************************
	#frecuencias, potencias = LombScargle(t_dat,us).autopower(nyquist_factor=50);
	potencias=LombScargle(t_dat,us).power(v_freq);
	potencias[potencias<0]=0;
	frecuencias=v_freq;
	#*******************************************************
	if numero_estrella[k]=='01729' and tipo_estrella=='BinariaECL':
		pos=np.argsort(potencias)[-45];
	elif numero_estrella[k]=='26555' and tipo_estrella=='BinariaECL':
		pos=np.argsort(potencias)[-5];
	elif numero_estrella[k]=='30750'and tipo_estrella=='BinariaECL':
		pos=np.argsort(potencias)[-4];
	elif numero_estrella[k]=='36923' and tipo_estrella=='BinariaECL':
		pos=np.argsort(potencias)[-8];
	elif numero_estrella[k]=='00573' and tipo_estrella=='RR_Lyrae':
		pos=np.argsort(potencias)[-3];
	else:
		pos=potencias.argmax();
	#fin if
	freq_mayor=frecuencias[pos];
	if tipo_estrella=='Cefeida':
		n_borrar=1000;
	else:
		n_borrar=1;
	epsilon=n_borrar*(freq_fin-freq_ini)/Finura;
	while freq_mayor>=2-epsilon and freq_mayor<=2+epsilon:
		potencias[pos]=0;
		pos=potencias.argmax();
		freq_mayor=frecuencias[pos];
	#fin while
	if tipo_estrella=='BinariaECL':
		tp_estrella=N_mult_LS[k]/freq_mayor;
	else:
		tp_estrella=1/freq_mayor;
	#fin if 
	fig=plt.figure()
	ax0=fig.add_subplot(111);
	ax0.plot(frecuencias,potencias);
	ax0.set_xlabel("Frecuencia en dias^-1");
	ax0.set_ylabel("Potencia periodograma Lomb-Scargle");
	nombreFoto="LS_Periodograma"+tipo_estrella+"-"+numero_estrella[k]+".png";
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
	nombreFoto2="LS_Curva_de_luz_de_"+tipo_estrella+"-"+numero_estrella[k]+".png";
	plt.savefig(nombreFoto2);
	plt.close(fig1);
	LabelEstrella="Estella_"+tipo_estrella+"_"+numero_estrella[k]+"_LS";
	lista_estrellas.append(LabelEstrella);
	lista_periodos.append(tp_estrella);
#fin for 
lista_estrellas=np.array(lista_estrellas);
lista_periodos=np.array(lista_periodos);
datos_exportacion=np.c_[lista_estrellas,lista_periodos];
encabezado=['Nombre_estrella','PeriodoLS [dias]'];

with open('periodos_hallados.csv', 'w', encoding='UTF8', newline='') as f:
	writer=csv.writer(f);
	writer.writerow(encabezado);
	writer.writerows(datos_exportacion);
#fin with 
