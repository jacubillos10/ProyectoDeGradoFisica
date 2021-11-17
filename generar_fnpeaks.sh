#!/bin/bash
# -*- coding: utf-8 -*-

tipo_estrella=('1_Cefeidas' '2_RR_Lyrae' '3_BinariasEclipsantes')
prefijos=('CEP' 'RRLYR' 'ECL')

vecCEP=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f1) );
vecRRLYR=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f2) );
vecECL=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f3) );

rangosBusqueda=('0.005 2.5 0.00002495' '0.8333 5 0.00004167' '0.002 2.5 0.00002498')
if (($1==0))
then
    for it in "${vecCEP[@]}"
    do
	    cp ./Datos/${tipo_estrella[$1]}/I/OGLE-LMC-${prefijos[$1]}-${it}.dat ./
	    frase="./fnpeaks OGLE-LMC-${prefijos[$1]}-${it}.dat ${rangosBusqueda[$1]}"
	    echo "el comando es: $frase"
	    eval $frase
    done
elif (($1==1))
then
    for it in "${vecRRLYR[@]}"
    do
	    cp ./Datos/${tipo_estrella[$1]}/I/OGLE-LMC-${prefijos[$1]}-${it}.dat ./
	    frase="./fnpeaks OGLE-LMC-${prefijos[$1]}-${it}.dat ${rangosBusqueda[$1]}"
	    echo "el comando es: $frase"
	    eval $frase
    done
else
    for it in "${vecECL[@]}"
    do
	    cp ./Datos/${tipo_estrella[$1]}/I/OGLE-LMC-${prefijos[$1]}-${it}.dat ./
	    frase="./fnpeaks OGLE-LMC-${prefijos[$1]}-${it}.dat ${rangosBusqueda[$1]}"
	    echo "el comando es: $frase"
	    eval $frase
    done
fi

carpetaDestino=('Cefeidas' 'RR_Lyrae' 'ECL')
rm *.dat
mv *.max ./Parte1/fnpeaks/${carpetaDestino[$1]}
