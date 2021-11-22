#!/bin/bash
# -*- coding: utf-8 -*-

tipo_estrella=('1_Cefeidas' '2_RR_Lyrae' '3_BinariasEclipsantes')
prefijos=('CEP' 'RRLYR' 'ECL')
entrada_tipo=('Cefeida' 'RR_Lyrae' 'BinariaECL');

vecCEP=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f1) );
vecRRLYR=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f2) );
vecECL=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f3) );
tpCEP=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f6) );
tpRRLYR=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f9) );
tpECL=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f12) );

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

for i in `seq 100`
do 
	frase="python3 LombScargle1_MinPuntos.py 0.985 ${entrada_tipo[$1]} ${vecNUM[(($i-1))]} ${vec_tp[(($i-1))]}"
	echo "el comando es: $frase"
	eval $frase >> LS_puntosMinimos_${prefijos[$1]}.csv
done
