#!/bin/bash
# -*- coding: utf-8 -*-

tipo_estrella=('1_Cefeidas' '2_RR_Lyrae' '3_BinariasEclipsantes')
prefijos=('CEP' 'RRLYR' 'ECL')

vecCEP=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f1) );
vecRRLYR=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f2) );
vecECL=( $(tail -n +2 numero_estrellas.csv | cut -d ',' -f3) );

# periodo inicial - periodo final - A - B - Finura - Ncas
rangosBusqueda=('0.4 200 12 7 100000 4' '0.15 1.2 12 7 100000 4' '0.4 500 17 5 100000 4')
if (($1==0))
then
    for it in "${vecCEP[@]}"
    do
	    cp ./Datos/${tipo_estrella[$1]}/I/OGLE-LMC-${prefijos[$1]}-${it}.dat ./
	    frase="./MinimaEntropia OGLE-LMC-${prefijos[$1]}-${it}.dat ${rangosBusqueda[$1]}"
	    echo "el comando es: $frase"
	    eval $frase
    done
elif (($1==1))
then
    for it in "${vecRRLYR[@]}"
    do
	    cp ./Datos/${tipo_estrella[$1]}/I/OGLE-LMC-${prefijos[$1]}-${it}.dat ./
	    frase="./MinimaEntropia OGLE-LMC-${prefijos[$1]}-${it}.dat ${rangosBusqueda[$1]}"
	    echo "el comando es: $frase"
	    eval $frase
    done
else
    for it in "${vecECL[@]}"
    do
	    cp ./Datos/${tipo_estrella[$1]}/I/OGLE-LMC-${prefijos[$1]}-${it}.dat ./
	    frase="./MinimaEntropia OGLE-LMC-${prefijos[$1]}-${it}.dat ${rangosBusqueda[$1]}"
	    echo "el comando es: $frase"
	    eval $frase
    done
fi

carpetaDestino=('Cefeidas' 'RR_Lyrae' 'ECL')
rm *.dat
mv Entropia_OGLE* ./Parte1/MinimaEntropia/${carpetaDestino[$1]}
