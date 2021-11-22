#!/usr/bin/env/python
#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import csv
import argparse
import sys

#Esto va a permitir que se agregue inputs desde la terminal (justo cuando se ejecuta python3 remover_puntos.py argv[0]....)
try:
	parser=argparse.ArgumentParser();
	parser.add_argument("porcentaje_rem", help="Coloque como primer argumento el porcentaje de puntos a remover", type=float);
	parser.add_argument("tipo estrella: ",help="Coloque el tipo de estrella con el que se va a trabajar");
	parser.add_argument("numero ID estrella: ", help="Coloque el número de la estrella a la que le va a remover puntos");
	args=parser.parse_args();
	porcentaje=float(sys.argv[1]);
	tipo_estrella=sys.argv[2];
	numero_estrella=sys.argv[3];
except:
	e = sys.exc_info()[0];
	print(e);
#fin try

#Importar los números de las estrellas desde el archivo csv:
ID_estrellas=np.loadtxt('numero_estrellas.csv',delimiter=',',dtype='str', skiprows=1);

vecCep=ID_estrellas[:,0];
vecRRLyr=ID_estrellas[:,1]; 
vecECL=ID_estrellas[:,2];

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if tipo_estrella=='Cefeida' or tipo_estrella==0 or tipo_estrella=='0':
	nombre_OGLE='OGLE-LMC-CEP-'
	label_path='Datos/'+'1_Cefeidas'+'/I/'+nombre_OGLE;
	#numero_estrella=vecCep;
elif tipo_estrella=='RR_Lyrae' or tipo_estrella==1 or tipo_estrella=='1':
	nombre_OGLE='OGLE-LMC-RRLYR-'
	label_path='Datos/'+'2_RR_Lyrae'+'/I/'+nombre_OGLE;
	#numero_estrella=vecRRLyr;
else:
	nombre_OGLE='OGLE-LMC-ECL-'
	label_path='Datos/'+'3_BinariasEclipsantes'+'/I/'+nombre_OGLE;
	#numero_estrella=vecECL;
#fin if 
extension='.dat';

#numero_estrella='02889';
elSeniorArchivo=label_path+numero_estrella+extension;
datos=np.genfromtxt(elSeniorArchivo,delimiter=' ');
N_datos=len(datos[:,0]);
N_remover=int(porcentaje*N_datos);
elegidos=np.random.choice(N_datos, size=N_remover,replace=False);
datos_nuevos=np.delete(datos,elegidos,0);

nombre_archivo=nombre_OGLE+numero_estrella+extension;
with open(nombre_archivo, 'w', encoding='UTF8', newline='') as f:
	writer=csv.writer(f, delimiter=' ');
	writer.writerows(datos_nuevos);
#fin with 
