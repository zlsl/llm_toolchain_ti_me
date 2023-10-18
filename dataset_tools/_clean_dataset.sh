#/bin/bash

# Фильтрация строк с мусором, пустых и коротких строк

# pv - аналог cat с выводом прогресса
# sudo apt install pv

pv $1 | \
	sed 's/^\t*//;s/ *$//' | \
	sed 's/^ *//;s/ *$//'| \
	sed '/^$/d'| \
	sed '/^.\{,4\}$/d' | \
	sed '/eBook/d' | \
	sed '/e-book/d' | \
	sed '/royalty-free/d' | \
	sed '/^* /d' | \
	sed '/^o /d' | \
	sed '/the publisher/d' | \
	sed '/ISBN/d' | \
	sed '/Table of Contents/d' | \
	sed '/characters and events/d' | \
	sed '/CIP record/d' | \
	sed '/All Rights Reserved/d' | \
	sed '/Games Workshop/d' | \
	sed '/ABOUT THE AUTHOR/d' | \
	sed '/is the author of the/d' | \
	sed '/BLACK LIBRARY PUB/d' | \
	sed '/first published in/d' | \
	sed '/Workshop Limited/d' | \
	sed '/are fictional/d' | \
	sed '/\.com/d' | \
	sed '/This license is made between/d' | \
	sed '/Click here to buy/d' | \
	sed '/Cover illustra/d' | \
	sed '/Art by:/d' | \
	sed '/internet/d' | \
	sed '/British/d' | \
	sed '/Black Library Pub/d' | \
	sed '/Часть /d' | \
	sed '/Глава /d' | \
	sed '/http/d' | \
	sed '/Britain/d' | \
	sed 's/\r/\n/g' \
	> $2
