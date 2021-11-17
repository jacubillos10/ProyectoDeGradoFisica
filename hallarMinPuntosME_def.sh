#!/bin/bash
# -*- coding: utf-8 -*-

final=$(($3-$2+1))

for j in `seq $final`
do
	./hallarMinPuntosME_uno.sh $1 $(($j+$2-1)) $4 
done

