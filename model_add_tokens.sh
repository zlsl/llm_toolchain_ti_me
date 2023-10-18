#!/bin/bash

# Добавление нового токена <char> в модель

SRC_MODEL="gpt2_small" # Каталог с исходной моделью
NEW_MODEL="gpt2_small_for_train" # Имя новой модели

./_add_tokens.py $SRC_MODEL $NEW_MODEL

