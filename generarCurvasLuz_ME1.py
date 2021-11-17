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

destinoMax='Parte1/MinimaEntropia/'
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if tipo_estrella=='Cefeida' or tipo_estrella==1:
	label_path='Datos/'+'1_Cefeidas'+'/I/OGLE-LMC-CEP-';
	nombre_res=destinoMax+'Cefeidas/Entropia_OGLE-LMC-CEP-';
elif tipo_estrella=='RR_Lyrae' or tipo_estrella==2:
	label_path='Datos/'+'2_RR_Lyrae'+'/I/OGLE-LMC-RRLYR-';
	nombre_res=destinoMax+'RR_Lyrae/Entropia_OGLE-LMC-RRLYR-';
else:
	label_path='Datos/'+'3_BinariasEclipsantes'+'/I/OGLE-LMC-ECL-';
	nombre_res=destinoMax+'ECL/Entropia_OGLE-LMC-ECL-';
#fin if 
extension='.dat';
extensionMax='.csv';

numero_estrella='02896'
vint=np.vectorize(np.int);
def transformar_ts(tp,t0,t_datos):
	phi_raw=(1/tp)*(t_datos-t0);
	phi=phi_raw-vint(phi_raw);
	return phi;
# fin transformar phis
lista_estrellas=[];
lista_periodos=[];

#Este_es para una estrella específica
elSeniorArchivoMax=nombre_res+numero_estrella+extensionMax;
Datos=np.genfromtxt(elSeniorArchivoMax,delimiter=',');
periodos=Datos[:,0];
entropias=Datos[:,1];
gs=Datos[:,2];
indiceGanador=np.argsort(entropias)[0];
tp_estrella=periodos[indiceGanador];
tol_g=0.6;
while (gs[indiceGanador]>tol_g):
	entropias[indiceGanador]=max(entropias);
	indiceGanador=np.argsort(entropias)[0];
	tp_estrella=periodos[indiceGanador];
#fin while
elSeniorArchivo=label_path+numero_estrella+extension;
fig0=plt.figure();
ax0=fig0.add_subplot(111);
ax0.plot(periodos,entropias);
x_limmax=(2*tp_estrella) if (2*tp_estrella<max(periodos)) else max(periodos);
ax0.set_xlim([min(periodos),x_limmax]);
ax0.set_xlabel("Periodo de prueba [días]");
ax0.set_ylabel("Entropía");
nombreFoto1="ME_Gráfica_entropía_de_"+tipo_estrella+"-"+numero_estrella+".png";
plt.savefig(nombreFoto1);
plt.close(fig0);
elSeniorArchivo=label_path+numero_estrella+extension;
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
nombreFoto2="ME_Curva_de_luz_de_"+tipo_estrella+"-"+numero_estrella+".png";
plt.savefig(nombreFoto2);
LabelEstrella="Estella_"+tipo_estrella+"_"+numero_estrella+"_ME";
lista_estrellas.append(LabelEstrella);
lista_periodos.append(tp_estrella);
lista_estrellas=np.array(lista_estrellas);
lista_periodos=np.array(lista_periodos);
datos_exportacion=np.c_[lista_estrellas,lista_periodos];
encabezado=['Nombre_estrella','Periodo_ME[dias]'];
print("El periodo que salió fue: ",tp_estrella);
print("Su entropía fue: ",entropias[indiceGanador]);
print("Búsquelo en el indice: ",indiceGanador+1);
print("El valor de g es: ",gs[indiceGanador]);

with open('periodos_hallados_ME.csv', 'w', encoding='UTF8', newline='') as f:
	writer=csv.writer(f);
	writer.writerow(encabezado);
	writer.writerows(datos_exportacion);
#fin with 
