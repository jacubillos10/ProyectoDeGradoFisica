#!/bin/bash
# -*- coding: utf-8 -*-

final=('43' '46' '47' '60' '70' '71' '74' '83' '85' '96' '99')
restantes=('10' '1' '1' '3' '4' '4' '4' '1' '13' '1' '4')
porc=('0.975' '0.95' '0.95' '0.975' '0.95' '0.9' '0.95' '0.975' '0.975' '0.95' '0.975')
numeroFaltante=${#final[@]}

for (( j=0; j<$numeroFaltante; j++))
do
	./hallarMinPuntosME_uno.sh $1 ${final[$j]} ${porc[$j]} ${restantes[$j]}
done

