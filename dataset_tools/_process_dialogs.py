#!/usr/bin/env python
import re, sys

# ./process_dialogs.py src.txt dest.txt
# На входе src.txt - отфильтрованый от лишних данных текстовый файл
# На выходе два текстовых файла:
# raw_dest.txt - с маркером "@" начала строки диалога
# dest.txt - с токеном "<char>" в начале (для обучения моделей gpt2)


def lreplace(pattern, sub, string):
    return re.sub('^%s' % pattern, sub, string)


def final_string(string):
    new_string = ''
    isopen = False
    for i, char in enumerate(string):
        if char == '|':
            if isopen:
                new_string += ') '
            else:
                new_string += ' ('
            isopen = not isopen
        else:
            if i == 0 and char == '@':
                new_string = '<char>'
            else:
               new_string += char
    if isopen:
        new_string += ')'

    new_string = new_string.replace("()", "")
    new_string = new_string.replace(" )", ")")
    new_string = new_string.replace(".)", ")")

    return new_string.strip()


def process_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    processed_lines = []
    final_lines = []
    for line in lines:
        tmp = line.replace("\r", "") 
        
        tmp = tmp.replace("…", "...")
        tmp = tmp.replace(" ", " ")
        tmp = tmp.replace(", -", "|")
        tmp = tmp.replace("! -", "!|")
        tmp = tmp.replace("? -", "?|")
        tmp = tmp.replace(". -", "|")
        tmp = tmp.replace(", –", "|")
        tmp = tmp.replace(". –", "|")
        tmp = tmp.replace("! –", "!|")
        tmp = tmp.replace("? –", "?|")
        tmp = tmp.replace("? —", "?|")
        tmp = tmp.replace(", —", "|")
        tmp = tmp.replace("? —", "?|")
        tmp = tmp.replace("! —", "!|")
        tmp = tmp.replace(". —", "|")
        tmp = tmp.replace("!—", "!|")
        tmp = tmp.replace(",—", "|")
        tmp = tmp.replace("?—", "?|")
        tmp = tmp.replace(".—", "|")
        tmp = tmp.replace(",-", "|")
        tmp = tmp.replace("!-", "!|")
        tmp = tmp.replace("?-", "?|")
        tmp = tmp.replace(".-", "|")
        tmp = tmp.replace(", —", "|")
        tmp = tmp.replace("\" -", "|")
        tmp = tmp.replace("\" —", "|")
        tmp = tmp.replace("\"-", "|")
        tmp = tmp.replace("\"—", "|")
        tmp = tmp.replace('" -', "|")
        tmp = tmp.replace('" -', "|")
        tmp = tmp.replace('" -', "|")
        if (tmp[0] == '"') | (tmp[0] == '"'):
            tmp = '@' + tmp[1:]
            tmp = tmp.replace('"', '|')
        tmp = tmp.replace("||", "|")
        tmp = tmp.replace("||", "|")
        tmp = tmp.replace("||", "|")
        tmp = tmp.replace("| ", "|")
        tmp = tmp.replace(" | ", "|")
        if tmp[0] == '-':
            tmp = '@' + tmp[1:]
        if tmp[0] == '–':
            tmp = '@' + tmp[1:]
        if tmp[0] == '—':
            tmp = '@' + tmp[1:]
        if tmp[0] == '"':
            tmp = '@' + tmp[1:]
        if tmp[0] == '—':
            tmp = '@' + tmp[1:]

        tmp = tmp.replace("@ ", "@").strip()
        if (len(tmp) > 1):
            processed_lines.append(tmp + "\n")
            final_lines.append(final_string(tmp) + "\n")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(final_lines)

    with open("raw_" + output_file, 'w', encoding='utf-8') as file:
        file.writelines(processed_lines)

if __name__=='__main__':
    if (len(sys.argv) != 3):
        exit('Usage: process_dialogs.py src_file dest_file')
    process_text(sys.argv[1], sys.argv[2])


