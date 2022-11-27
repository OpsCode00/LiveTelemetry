#bin/bash!

sudo apt install mosquitto mosquitto-clients libmosquitto-dev
echo
echo
echo FATTO! ora basta includere la libraria "<mosquitto.h>" ed anche la libreria "<canlib.h>"
echo quando si compila, aggiungere all fine -lmosquitto per includere la libreria nella compilazione. Aggiungere anche -lcanlib per canlib
