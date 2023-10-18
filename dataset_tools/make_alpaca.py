#!/usr/bin/env python
import re, sys
import json
from collections import OrderedDict

# Создание json датасета в формате альпаки (input:output)
# На входе - файл диалогов (где в начале строки с диалогом стоит символ "@")


CHUNK_SIZE = 50000

blacklist = [
    'исключатьстрокисэтимсловом',
    'исэтим'
        ]


def valid(string, substrings):
    for substring in substrings:
        if substring in string:
            return True
    return False


def qq(string):
    new_string = ''
    isopen = False
    for i, char in enumerate(string):
        if char == '|':
            if not isopen:
                new_string += ' ('
                isopen = True
            else:
                new_string += ') '
                isopen = False
        else:
            new_string += char
    if isopen:
        new_string += ')'

    new_string = new_string.replace(" )", ")")
    new_string = new_string.replace(".)", ")")
    new_string = new_string.replace("()", "")
    new_string = new_string.replace("(,", "(")
    new_string = new_string.replace("(.", "(")
    new_string = new_string.replace(",)", ")")
    new_string = new_string.replace("(-", "(")
    new_string = new_string.replace("( ", "(")
    new_string = new_string.replace("-)", ")")

    return new_string


def item(context, input, output):
    return {
            "input": context + "\n" + input,
            "output": output,
        }

def item2(context, input):
    return {
            "input": context,
            "output": input,
        }

def save(dataset, name):
    global CHUNK_SIZE
    print("dedup")
    dataset1 = list(OrderedDict((tuple(d.items()), d) for d in dataset).values())
    print("saving")

    for i in range(0, len(dataset1), CHUNK_SIZE):
        chunk = dataset1[i:i + CHUNK_SIZE]
        file_name = f"{name}_{i // CHUNK_SIZE}.json"
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(chunk, file, ensure_ascii=False, indent=2)

def process_text(input_file, output_name):
    print("loading...")
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    print("make...")
    dataset = []
    baddataset = []

    is_dialog = False
    think = ''
    tmp = ''
    t_ctx = 'Секс'
    t_a = ''
    t_b = ''
    a = ''
    b = ''
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            if line[0] != '@':         
                t_a = ''
                t_b = ''
                t_ctx = line
            else:
                if (t_ctx):
                    if not t_a: #новый диалог начало
                        t_a = qq(line.replace("@", ""))
                    else:
                        if t_a and not t_b:
                            t_b = qq(line.replace("@", ""))
                        else:
                            t_a = t_b
                            t_b = qq(line.replace("@", ""))

        if t_ctx and t_a and t_b:
            if (len(t_a) < 200):
                i = item(t_ctx, t_a, t_b)
                if not valid(t_ctx + t_a + t_b, blacklist):
                    t_ctx = t_ctx + "\n" + t_a
                    dataset.append(i)
                else:
                    baddataset.append(i)




    save(dataset, output_name)
    save(baddataset, 'bad_' + output_name)

if __name__=='__main__':
    if (len(sys.argv) != 4):
        exit('Usage: make_alpaca.py src_file dest_file chunk_size\n\tchunk_size - split output json by chunks')
    CHUNK_SIZE = int(sys.argv[3])
    process_text(sys.argv[1], sys.argv[2])

