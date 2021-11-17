#!/usr/bin/env/python
#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import csv

#Coloque aquí el tipo de estrella con el que se va a trabajar. OPCIONES= 'Cefeida', 'RR_Lyrae', 'BinariaECL'.
tipo_estrella='BinariaECL';

#Importar los números de las estrellas desde el archivo csv:
ID_estrellas=np.loadtxt('numero_estrellas.csv',delimiter=',',dtype='str', skiprows=1);

vecCep=ID_estrellas[:,0];
vecRRLyr=ID_estrellas[:,1]; 
vecECL=ID_estrellas[:,2];

destinoMax='Parte1/MinimaEntropia/'
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if tipo_estrella=='Cefeida' or tipo_estrella==1:
	label_path='Datos/'+'1_Cefeidas'+'/I/OGLE-LMC-CEP-';
	nombre_res=destinoMax+'Cefeidas/Entropia_OGLE-LMC-CEP-';
	numero_estrella=vecCep;
elif tipo_estrella=='RR_Lyrae' or tipo_estrella==2:
	label_path='Datos/'+'2_RR_Lyrae'+'/I/OGLE-LMC-RRLYR-';
	nombre_res=destinoMax+'RR_Lyrae/Entropia_OGLE-LMC-RRLYR-';
	numero_estrella=vecRRLyr;
else:
	label_path='Datos/'+'3_BinariasEclipsantes'+'/I/OGLE-LMC-ECL-';
	nombre_res=destinoMax+'ECL/Entropia_OGLE-LMC-ECL-';
	numero_estrella=vecECL;
#fin if 
extension='.dat';
extensionMax='.csv';

vint=np.vectorize(np.int);
def transformar_ts(tp,t0,t_datos):
	phi_raw=(1/tp)*(t_datos-t0);
	phi=phi_raw-vint(phi_raw);
	return phi;
# fin transformar phis

N_mult=np.genfromtxt("IndicesMult.csv", delimiter=",", skip_header=1);
N_mult_LS=N_mult[:,2];

lista_estrellas=[];
lista_periodos=[];
lista_entropias=[];
lista_g=[];
lista_f=[];

for k in range(len(numero_estrella)):
	#Este_es para una estrella específica
	elSeniorArchivoMax=nombre_res+numero_estrella[k]+extensionMax;
	Datos=np.genfromtxt(elSeniorArchivoMax,delimiter=',');
	periodos=Datos[:,0];
	entropias=Datos[:,1];
	gs=Datos[:,2];
	fs=Datos[:,3];
	indiceGanador=np.argsort(entropias)[0];
	tp_estrella=periodos[indiceGanador];
	if numero_estrella[k]=='11639':
		tol_g=0.9;
		tol_f=0.9;
	elif numero_estrella[k]=='14200':
		tol_g=1;
		tol_f=0.8;
	elif numero_estrella[k]=='22820':
		tol_g=1.05;
		tol_f=0.8;
	elif numero_estrella[k]=='24305':
		tol_g=1.1;
		tol_f=0.7;
	else:
		tol_g=1.5;
		tol_f=1.02;
	#fin if 
	while (fs[indiceGanador]>tol_f or gs[indiceGanador]>tol_g):
		entropias[indiceGanador]=max(entropias);
		indiceGanador=np.argsort(entropias)[0];
		tp_estrella=periodos[indiceGanador];
	#fin while
	elSeniorArchivo=label_path+numero_estrella[k]+extension;
	fig0=plt.figure();
	ax0=fig0.add_subplot(111);
	ax0.plot(periodos,entropias);
	x_limmax=(2*tp_estrella) if (2*tp_estrella<max(periodos)) else max(periodos);
	ax0.set_xlim([min(periodos),x_limmax]);
	ax0.set_xlabel("Periodo de prueba [días]");
	ax0.set_ylabel("Entropía");
	nombreFoto1="ME_Gráfica_entropía_de_"+tipo_estrella+"-"+numero_estrella[k]+".png";
	plt.savefig(nombreFoto1);
	plt.close(fig0);
	if tipo_estrella=='BinariaECL':
		tp_estrellaM=N_mult_LS[k]*tp_estrella;
	#fin if 
	datos=np.genfromtxt(elSeniorArchivo,delimiter=' ');
	t_dat=datos[:,0];
	us=datos[:,1];
	tini=t_dat[0];
	phis=transformar_ts(tp_estrellaM,t_dat[0],t_dat);
	phis1=phis+1;
	phisG=np.r_[phis,phis1];
	usG=np.r_[us,us];
	fig1=plt.figure();
	ax1=fig1.add_subplot(111);
	ax1.scatter(phisG,usG);
	ax1.set_ylim(ax1.get_ylim()[::-1]);
	ax1.set_xlabel("fase");
	ax1.set_ylabel("Magnitud");
	nombreFoto2="ME_Curva_de_luz_de_"+tipo_estrella+"-"+numero_estrella[k]+".png";
	plt.savefig(nombreFoto2);
	plt.close(fig1);
	LabelEstrella="Estella_"+tipo_estrella+"_"+numero_estrella[k]+"_ME";
	lista_estrellas.append(LabelEstrella);
	lista_periodos.append(tp_estrella);
	lista_entropias.append(entropias[indiceGanador]);
	lista_g.append(gs[indiceGanador]);
	lista_f.append(fs[indiceGanador]);
	print("***********************************************************************");
	print("Resumen de datos de la estrella ",tipo_estrella," ",numero_estrella[k]);
	print("El periodo que salió fue: ",tp_estrella);
	print("Su entropía fue: ",entropias[indiceGanador]);
	print("Búsquelo en el indice: ",indiceGanador+1);
	print("El valor de g es: ",gs[indiceGanador]);
	print("El valor de f es: ",fs[indiceGanador]);
	print("***********************************************************************");
#fin for 


lista_estrellas=np.array(lista_estrellas);
lista_periodos=np.array(lista_periodos);
lista_entropias=np.array(lista_entropias);
lista_g=np.array(lista_g);
lista_f=np.array(lista_f);
datos_exportacion=np.c_[lista_estrellas,lista_periodos,lista_entropias,lista_g,lista_f];
encabezado=['Nombre_estrella','Periodo_ME[dias]','Entropía','g','f'];

with open('periodos_hallados_ME.csv', 'w', encoding='UTF8', newline='') as f:
	writer=csv.writer(f);
	writer.writerow(encabezado);
	writer.writerows(datos_exportacion);
#fin with 
