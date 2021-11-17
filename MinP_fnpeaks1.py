#!/usr/bin/env/python
#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import os

tipo_estrella="RR_Lyrae";
numero_estrella='01981';
porc_ini=0.99;


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if tipo_estrella=='Cefeida' or tipo_estrella==0:
	label_path='Datos/'+'1_Cefeidas'+'/I/OGLE-LMC-CEP-';
	nombre_res='OGLE-LMC-CEP-';
	losRangos=' 0.005 2.5 0.00002495';
	col_per=4;
	col_ID=0;
	#numero_estrella=vecCep;
elif tipo_estrella=='RR_Lyrae' or tipo_estrella==1:
	label_path='Datos/'+'2_RR_Lyrae'+'/I/OGLE-LMC-RRLYR-';
	nombre_res='OGLE-LMC-RRLYR-';
	losRangos=' 0.8333 5 0.00004167';
	col_per=7;
	col_ID=1;
	#numero_estrella=vecRRLyr;
else:
	label_path='Datos/'+'3_BinariasEclipsantes'+'/I/OGLE-LMC-ECL-';
	nombre_res='OGLE-LMC-ECL-';
	losRangos=' 0.002 2.5 0.00002498';
	col_per=10;
	col_ID=2;
	#numero_estrella=vecECL;
#fin if 
extension='.dat';
extensionMax='.max';
periodos=np.genfromtxt('numero_estrellas.csv',delimiter=',',skip_header=1, usecols=col_per);
IDs=np.loadtxt('numero_estrellas.csv',delimiter=',',dtype='str', skiprows=1, usecols=col_ID);

elSeniorArchivoOR=label_path+numero_estrella+extension;
datos_originales=np.genfromtxt(elSeniorArchivoOR,delimiter=' ');
N_tot=len(datos_originales[:,0]);
paso_min=1/N_tot;
periodo_halladoP1=periodos[IDs==numero_estrella][0];
maxBusq=int(porc_ini*N_tot);
cBusq=0;
porc=porc_ini;
tolP=1e-3;
encontro=False; 
periodo_new=0;

while encontro==False and cBusq<=maxBusq:
	os.system('python3 remover_puntos.py '+str(porc)+' '+str(tipo_estrella)+' '+numero_estrella);
	elSeniorArchivo=nombre_res+numero_estrella+extension;
	os.system('./fnpeaks '+elSeniorArchivo+losRangos);
	elSeniorArchivoMax=nombre_res+numero_estrella+extensionMax;
	dat_tp=np.genfromtxt(elSeniorArchivoMax,delimiter='    ',skip_header=9, usecols=2);
	for l in range(len(dat_tp)):
		diferenciaPc=abs(dat_tp[l]-periodo_halladoP1)/periodo_halladoP1;
		if diferenciaPc<=tolP:
			encontro=True; 
			periodo_new=dat_tp[l];
		#fin if
	#fin for 
	porc=porc-paso_min;
	cBusq=cBusq+1;
#fin while

datos_fin=np.genfromtxt(elSeniorArchivo,delimiter=' ');
N_datos_fin=len(datos_fin[:,0]);

print("El porcentaje donde funcionó es: ",porc);
print("Eso equivale a :",N_datos_fin," puntos");
print("El periodo con esos puntos es: ", periodo_new); 
