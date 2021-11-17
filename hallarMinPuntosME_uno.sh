#!/bin/bash
# -*- coding: utf-8 -*-

tipo_estrella=('1_Cefeidas' '2_RR_Lyrae' '3_BinariasEclipsantes')
prefijos=('CEP' 'RRLYR' 'ECL')
rangosBusqueda=('0.4 200 12 7 100000 4' '0.15 1.2 12 7 100000 4' '0.4 500 17 5 100000 4')

vecCEP=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f1) );
vecRRLYR=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f2) );
vecECL=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f3) );
tpCEP=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f4) );
tpRRLYR=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f7) );
tpECL=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f10) );

if (($1==0))
then
	vecNUM=(${vecCEP[@]})
	vec_tp=(${tpCEP[@]})
elif (($1==1))
then
	vecNUM=(${vecRRLYR[@]})
	vec_tp=(${tpRRLYR[@]})
else
	vecNUM=(${vecECL[@]})
	vec_tp=(${tpECL[@]})
fi 

cp ./Datos/${tipo_estrella[$1]}/I/OGLE-LMC-${prefijos[$1]}-${vecNUM[$2]}.dat ./
frase="./HallarPuntosME OGLE-LMC-${prefijos[$1]}-${vecNUM[$2]}.dat ${rangosBusqueda[$1]} ${vec_tp[$2]} $3 $4"
echo "el comando es: $frase"
eval $frase

rm OGLE-LMC-${prefijos[$1]}-${vecNUM[$2]}.dat

