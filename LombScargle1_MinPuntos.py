#!/usr/bin/env/python
#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from astropy.timeseries import LombScargle
import csv
import argparse
import sys
import os

try:
	parser=argparse.ArgumentParser();
	parser.add_argument("porcentaje_rem", help="Coloque como primer argumento el porcentaje de puntos a remover", type=float);
	parser.add_argument("tipo estrella: ",help="Coloque el timpo de estrella con el que se va a trabajar");
	parser.add_argument("numero ID estrella: ", help="Coloque el número de la estrella a la que le va a remover puntos");
	parser.add_argument("Periodo de la estrella: ", help="Coloque el periodo de la estrella en días");
	args=parser.parse_args();
	porcentaje=float(sys.argv[1]);
	tipo_estrella=sys.argv[2];
	numero_estrella=sys.argv[3];
	periodo=float(sys.argv[4]);
#Coloque aquí el tipo de estrella con el que se va a trabajar. OPCIONES= 'Cefeida', 'RR_Lyrae', 'BinariaECL'.
except:
	e = sys.exc_info()[0];
	print(e);
#fin try

if tipo_estrella=='Cefeida' or tipo_estrella==1:
	label_path='Datos/'+'1_Cefeidas'+'/I/OGLE-LMC-CEP-';
	tp_ini=0.4;
	tp_fin=200;
elif tipo_estrella=='RR_Lyrae' or tipo_estrella==2:
	label_path='Datos/'+'2_RR_Lyrae'+'/I/OGLE-LMC-RRLYR-';
	tp_ini=0.15;
	tp_fin=1.2;
else:
	label_path='Datos/'+'3_BinariasEclipsantes'+'/I/OGLE-LMC-ECL-';
	tp_ini=0.4;
	tp_fin=500;
#fin if 

extension='.dat';

def encontrar_mejores_freq(frecuencias,potencias,tam,vecinos):
	pot_mayores=np.zeros(tam);
	indices=np.zeros(tam);
	freq=np.zeros(tam);
	pots=np.zeros(tam);
	for k in range(len(frecuencias)):
		termino=False;
		l=0;
		while l<tam and termino==False:
			if potencias[k]>pot_mayores[l]:
				if (k-indices[l])<=vecinos:
					pot_mayores[l]=potencias[k];
					indices[l]=k;
					termino=True;
				else:
					if l<(tam-1):
						pot_mayores[l+1]=pot_mayores[l];
						indices[l+1]=indices[l];
					#fin if
					pot_mayores[l]=potencias[k];
					indices[l]=k;
					termino=True;
				#fin if 
			else:
				if (k-indices[l])<=vecinos:
					termino=True;
				#fin if
			#fin if
			l=l+1;
		#fin while
	#fin for
	for n in range(tam):
		freq[n]=frecuencias[int(indices[n])];
		pots[n]=potencias[int(indices[n])];
	#fin for
	return [freq, pots];
#fin función

#IMPORTAR DAROS DEL ARCHIVO Y. 
Finura=100000;
elSeniorArchivo=label_path+numero_estrella+extension;
datos=np.genfromtxt(elSeniorArchivo,delimiter=' ');
ts=datos[:,0];
us=datos[:,1];
desv=datos[:,2];
tini=ts[0];

freq_ini=1/tp_fin;
freq_fin=1/tp_ini;
v_freq=np.linspace(freq_ini,freq_fin,Finura);
N_mult=np.genfromtxt("IndicesMult.csv", delimiter=",", skip_header=1);
N_mult_LS=N_mult[:,0];

Ns='';
N_datos=len(datos[:,0]);
for l in range(20):
	N_remover=int(porcentaje*N_datos);
	encontro=False;
	cBusq=0;
	maxBusq=N_remover;
	while encontro==False and cBusq<=maxBusq:
		elegidos=np.random.choice(N_datos, size=N_remover,replace=False);
		datos_nuevos=np.delete(datos,elegidos,0);
		t_rem=datos_nuevos[:,0];
		u_rem=datos_nuevos[:,1];
		potencias=LombScargle(t_rem,u_rem).power(v_freq);
		frecuencias=v_freq;
		resultados=encontrar_mejores_freq(frecuencias,potencias,10,3);
		freq_sp=resultados[0];
		periodos_s=1/freq_sp;
		for i in range(10):
			if (abs(periodos_s[i]-periodo)/periodo)<=1e-3:
				encontro=True;
			#fin if
		#fin for  
		N_remover=N_remover-1;
		cBusq=cBusq+1;
	#fin while
	N_remanente=N_datos-N_remover;
	if l==19:
		Ns=Ns+str(N_remanente);
	else:
		Ns=Ns+str(N_remanente)+',';
	#fin if
#fin for 

print(Ns);

