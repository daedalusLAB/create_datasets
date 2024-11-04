#!/bin/bash

./create_dataset.py --input tmp/yesterday_2016_10K.txt --output_folder tmp/yesterday_2016_10K_NUEVO  --searchterm yesterday --offset 2 

echo "yesterday finalizado" | mail -s "Yesterday" raul@um.es;

./create_dataset.py --input tmp/today_2016_10K.txt --output_folder tmp/today_2016_10K_NUEVO  --searchterm today --offset 2 

echo "today finalizado" | mail -s "Today" raul@um.es;

./create_dataset.py --input tmp/tomorrow_2016_10K.txt --output_folder tmp/tomorrow_2016_10K_NUEVO  --searchterm tomorrow --offset 2 

echo "tomorrow finalizado" | mail -s "Tomorrow" raul@um.es;
