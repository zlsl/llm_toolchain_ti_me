#!/usr/bin/env python
import sys
import nltk
import pymorphy2
from pathlib import Path

# ./extract_names.py src.txt
# На входе src.txt - текстовый файл
# На выходе 2 файла python с массивом Имя:местоимение для Я - ТЫ


morph = pymorphy2.MorphAnalyzer()


def get_rep(p, word):
        if p.tag.case == 'nomn': # именительный	Кто? Что?	хомяк ест
            return 'ты'
        if p.tag.case == 'gent': # родительный	Кого? Чего?	у нас нет хомяка
            return 'тебя'
        if p.tag.case == 'datv': # дательный	Кому? Чему?	сказать хомяку спасибо
            return 'тебе'
        if p.tag.case == 'accs': # винительный	Кого? Что?	хомяк читает книгу
            return 'тебя'
        if p.tag.case == 'ablt': # творительный	Кем? Чем?	зерно съедено хомяком
            return 'тобой'
        if p.tag.case == 'loct': # предложный	О ком? О чём? и т.п.	хомяка несут в корзинке
            return 'тебе'
        if p.tag.case == 'voct': # звательный	Его формы используются при обращении к человеку.	Саш, пойдем в кино.
            return 'ты'
        if p.tag.case == 'gen2': # второй родительный (частичный)	 	ложка сахару (gent - производство сахара); стакан яду (gent - нет яда)
            return 'тебя'
        if p.tag.case == 'acc2': # второй винительный	 	записался в солдаты
            return 'ты'
        if p.tag.case == 'loc2': # второй предложный (местный)	 	я у него в долгу (loct - напоминать о долге); висит в шкафу (loct - монолог о шкафе); весь в снегу (loct - писать о снеге)
            return 'тебя'
    
        return word
                

def get_rep2(p, word):
        if p.tag.case == 'nomn': # именительный	Кто? Что?	хомяк ест
            return 'я'
        if p.tag.case == 'gent': # родительный	Кого? Чего?	у нас нет хомяка
            return 'меня'
        if p.tag.case == 'datv': # дательный	Кому? Чему?	сказать хомяку спасибо
            return 'мне'
        if p.tag.case == 'accs': # винительный	Кого? Что?	хомяк читает книгу
            return 'меня'
        if p.tag.case == 'ablt': # творительный	Кем? Чем?	зерно съедено хомяком
            return 'мной'
        if p.tag.case == 'loct': # предложный	О ком? О чём? и т.п.	хомяка несут в корзинке
            return 'мне'
        if p.tag.case == 'voct': # звательный	Его формы используются при обращении к человеку.	Саш, пойдем в кино.
            return 'я'
        if p.tag.case == 'gen2': # второй родительный (частичный)	 	ложка сахару (gent - производство сахара); стакан яду (gent - нет яда)
            return 'меня'
        if p.tag.case == 'acc2': # второй винительный	 	записался в солдаты
            return 'я'
        if p.tag.case == 'loc2': # второй предложный (местный)	 	я у него в долгу (loct - напоминать о долге); висит в шкафу (loct - монолог о шкафе); весь в снегу (loct - писать о снеге)
            return 'я'
    
        return word
                

def extract_names(input_file):
    res = ''

    # Здесь необходимо откорректировать базовые словари под свои нужды, с учётом заглавных букв.

    ti_names = [
            "'Девушка':'Ты',\n"
            "'Женщина':'Ты',\n"
            "'Мучжина':'Ты',\n"
            "'Парень':'Ты',\n"
            "'Эльфийка':'Ты',\n"
            ]
    me_names = [
            "'Девушка':'Я',\n"
            "'Женщина':'Я',\n"
            "'Мужчина':'Я',\n"
            "'Парень':'Я',\n"
            "'Эльфийка':'Я',\n"
            ]

    with open(input_file) as FileObj:
        for text in FileObj:

            for word in nltk.word_tokenize(text):
                if (len(word) > 2):
                   if word[0].isupper():
                       if not 'я' == word.lower():
                           for p in morph.parse(word):
                               if (p.tag.POS == 'NOUN') and (p.tag.number == 'sing'):
                                   if (not 'Patr' in p.tag) and (not 'Surn' in p.tag):
                                       if (p.tag.animacy == 'anim') and (not 'ms-f' in p.tag) and ('Name' in p.tag):
                                           ti_itm = "'" + word + "' : '" + get_rep(p, word) + "',\n"
                                           me_itm = "'" + word + "' : '" + get_rep2(p, word) + "',\n"
                                           if not ti_itm in ti_names:
                                               ti_names.append(ti_itm)
                                           if not me_itm in me_names:
                                               me_names.append(me_itm)
                                           break


    ti_names.sort()
    me_names.sort()

    ti_names.insert(0, "dict_ti = {\n")
    ti_names.append("\n}")
    me_names.insert(0, "dict_me = {\n")
    me_names.append("\n}")

    with open("dict_ti.py", 'w', encoding='utf-8') as file:
        file.writelines(ti_names)
    
    with open("dict_me.py", 'w', encoding='utf-8') as file:
        file.writelines(me_names)
        


if __name__=='__main__':
    if (len(sys.argv) != 2):
        exit('Usage: process_dialogs.py src_file')
    extract_names(sys.argv[1])
