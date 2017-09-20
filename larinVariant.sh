#!/bin/bash

WEEKNUM=$(($(date +%V) + 165))
if curl -s --head http://alexlarin.net/ege/2018/trvar$WEEKNUM.pdf | head -n 1 | grep OK;
then
    cd ~/bot/bank/LARIN/variants/;
	wget http://alexlarin.net/ege/2018/trvar$WEEKNUM.pdf
    mv trvar$WEEKNUM.pdf $WEEKNUM.pdf;
fi

