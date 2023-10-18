#!/bin/bash
#---------------------------------------
CEND="\e[0m"
CGREEN="\e[1;32m"
#---------------------------------------

SRC_FILE="raw.txt"
BASE_NAME="dataset"

# Загрузка словарей и модулей nltk
python -m nltk.downloader all


echo -e "$CGREENОчистка от мусора...$CEND"
./_clean_dataset.sh $SRC_FILE .tmp.txt

echo -e "$CGREENОбработка диалогов...$CEND"
./_process_dialogs.py .tmp.txt dialogs.txt

rm .tmp.txt

echo -e "$CGREENПоиск имён собственных...$CEND"
./_extract_names.py dialogs.txt

echo -e "$CGREENСоздание датасетов TiMe...$CEND"
./_make_time.py dialogs.txt dataset.txt

echo -e "$CGREENСоздание общего датасета...$CEND"
pv dialogs.txt me_dataset.txt ti_dataset.txt > dataset.txt


