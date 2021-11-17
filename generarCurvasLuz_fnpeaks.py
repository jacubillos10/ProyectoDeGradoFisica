#!/usr/bin/env/python
#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import csv

#Coloque aquí el tipo de estrella con el que se va a trabajar. OPCIONES= 'Cefeida', 'RR_Lyrae', 'BinariaECL'.
tipo_estrella='RR_Lyrae';

#Importar los números de las estrellas desde el archivo csv:
ID_estrellas=np.loadtxt('numero_estrellas.csv',delimiter=',',dtype='str', skiprows=1);

vecCep=ID_estrellas[:,0];
vecRRLyr=ID_estrellas[:,1]; 
vecECL=ID_estrellas[:,2];

destinoMax='Parte1/fnpeaks/'
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if tipo_estrella=='Cefeida' or tipo_estrella==1:
	label_path='Datos/'+'1_Cefeidas'+'/I/OGLE-LMC-CEP-';
	nombre_res=destinoMax+'Cefeidas/OGLE-LMC-CEP-';
	numero_estrella=vecCep;
elif tipo_estrella=='RR_Lyrae' or tipo_estrella==2:
	label_path='Datos/'+'2_RR_Lyrae'+'/I/OGLE-LMC-RRLYR-';
	nombre_res=destinoMax+'RR_Lyrae/OGLE-LMC-RRLYR-';
	numero_estrella=vecRRLyr;
else:
	label_path='Datos/'+'3_BinariasEclipsantes'+'/I/OGLE-LMC-ECL-';
	nombre_res=destinoMax+'ECL/OGLE-LMC-ECL-';
	numero_estrella=vecECL;
#fin if 
extension='.dat';
extensionMax='.max';

vint=np.vectorize(np.int);
def transformar_ts(tp,t0,t_datos):
	phi_raw=(1/tp)*(t_datos-t0);
	phi=phi_raw-vint(phi_raw);
	return phi;
# fin transformar phis

N_mult=np.genfromtxt("IndicesMult.csv", delimiter=",", skip_header=1);
N_mult_fnP=N_mult[:,1];

lista_estrellas=[];
lista_periodos=[];
for k in range(len(numero_estrella)):
	elSeniorArchivoMax=nombre_res+numero_estrella[k]+extensionMax;
	dat_tp=np.genfromtxt(elSeniorArchivoMax,delimiter='    ',skip_header=9, usecols=2);
	periodos=dat_tp;
	if tipo_estrella=='BinariaECL':
		tp_estrella=N_mult_fnP[k]*periodos[0];
		if numero_estrella[k]=='01729':
			tp_estrella=periodos[3];
	elif tipo_estrella=='RR_Lyrae' and numero_estrella[k]=='00573':
		tp_estrella=periodos[1];
	else:
		tp_estrella=periodos[0];
	#fin if 
	elSeniorArchivo=label_path+numero_estrella[k]+extension;
	datos=np.genfromtxt(elSeniorArchivo,delimiter=' ');
	t_dat=datos[:,0];
	us=datos[:,1];
	tini=t_dat[0];
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
	nombreFoto2="fnP_Curva_de_luz_de_"+tipo_estrella+"-"+numero_estrella[k]+".png";
	plt.savefig(nombreFoto2);
	plt.close(fig1);
	LabelEstrella="Estella_"+tipo_estrella+"_"+numero_estrella[k]+"_fnP";
	lista_estrellas.append(LabelEstrella);
	lista_periodos.append(tp_estrella);
#fin for 

lista_estrellas=np.array(lista_estrellas);
lista_periodos=np.array(lista_periodos);
datos_exportacion=np.c_[lista_estrellas,lista_periodos];
encabezado=['Nombre_estrella','Periodo_fnP[dias]'];

with open('periodos_hallados_fnP.csv', 'w', encoding='UTF8', newline='') as f:
	writer=csv.writer(f);
	writer.writerow(encabezado);
	writer.writerows(datos_exportacion);
#fin with 
