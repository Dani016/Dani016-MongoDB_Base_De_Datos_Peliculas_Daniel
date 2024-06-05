# Proyecto Cine 2.0

## Descripción

Este proyecto es una aplicación de gestión de una base de datos de películas utilizando Python, MongoDB y Tkinter. La aplicación permite a los usuarios introducir, ver, buscar y eliminar películas en la base de datos, especificando la plataforma de streaming donde están disponibles.

## Requisitos

### Software

1. **Python 3.8+**
   - Asegúrate de tener Python 3.0 o una versión superior instalada. Puedes descargarlo desde [python.org](https://www.python.org/downloads/). O bien con "sudo apt install python3"
   1.1 Tkinter
     - es posible que no funcione el tkinter, aun siendo parte de la biblioteca de python, en ese caso utilizar el comando "pip3 install tkinter"
2. **MongoDB**
   - Necesitarás tener una instancia de MongoDB en funcionamiento. Puedes descargar MongoDB desde [mongodb.com](https://www.mongodb.com/try/download/community) y seguir las instrucciones para instalarlo y configurarlo. O bien con el comando en docker "docker pull mongo".
   - Alternativamente, puedes usar MongoDB Atlas para una base de datos en la nube.

### Bibliotecas de Python

Instala las siguientes bibliotecas de Python utilizando `pip`:

- `pymongo` para conectarse y operar con MongoDB.
- `tkinter` para la interfaz gráfica de usuario.
### Indicaciones:

   -Primeramente, iniciamos un docker de MongoDB, con el puerto de entrada 27017, una vez iniciado correctamente, ejecutamos el programa de python, con los requerimientos instalados, y ya tendriamos todo listo.
