#!/usr/bin/python3
import configparser
import logging
import os
import pathlib
import re
import time

import shapely.geometry

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from shapely.geometry.geo import shape

log = logging.getLogger(__name__)

importe_re = re.compile(r"^(?P<importe>\d+,\d+)\s*EUR$")

class LocalContext():

    def __init__(self, cp, directorio):
        self.cp = cp
        self.directorio = directorio
        self.engine = None
        self.metadata = None
        self.conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class Carta():
    #factura = shapely.geometry.box(6.2948, 3.4234, 6.8866, 3.5526)
    #fecha = shapely.geometry.box(6.2732, 3.2296, 6.9619, 3.3481)
    #importe = shapely.geometry.box(6.5422, 7.1483, 7.4353, 7.3098)

    fecha   = shapely.geometry.box(6.2, 3.1, 7.0, 3.5)
    factura = shapely.geometry.box(6.2, 3.3, 7.0, 3.7)
    importe = shapely.geometry.box(6.0, 7.0, 7.7, 7.6)


    comentario = shapely.geometry.box(1.6, 5.2, 8.0, 5.5)
    codigo = shapely.geometry.box(1.0, 6.0, 2.5, 6.6)
    nombre = shapely.geometry.box(4.6, 6.0, 9.0, 7.0)
    slbs = shapely.geometry.box(2.3, 6.0, 5.0, 10.0)


class Datos():
    pagina = None
    fecha = None
    factura = None
    importe = None
    comentario = None
    codigo = None
    nombre = None
    slbs = None

def procesar_carta(datos, lineas):
    for f in [ f for f in lineas if f.box.within(Carta.factura) ]:
        datos.factura = f.text
        break
    for f in [ f for f in lineas if f.box.within(Carta.fecha) ]:
        datos.fecha =  f.text.replace(".", "/") if f.text else None
        break
    for f in [ f for f in lineas if f.box.within(Carta.importe) ]:
        m = importe_re.match(f.text)
        if m:
            datos.importe = m.group("importe")
        else:
            datos.importe = f.text
        break

def procesar_cargo(datos, lineas):
    for f in [ f for f in lineas if f.box.within(Carta.comentario) ]:
        datos.comentario = f.text
        break
    for f in [ f for f in lineas if f.box.within(Carta.codigo) ]:
        datos.codigo = f.text
        break
    for f in [ f for f in lineas if f.box.within(Carta.nombre) ]:
        datos.nombre = f.text
        break    
    datos.slbs = [ f.text for f in lineas if f.box.within(Carta.slbs) ]

def procesar_fichero(client, fich):
    log.info(f"(fichero) : {fich}")
    with open(fich, "rb") as fich:
        read_response = client.read_in_stream(fich, language="de", raw=True)
        print(read_response)

        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]            

        # Call the "GET" API and wait for the retrieval of the results
        while True:
            read_result = client.get_read_result(operation_id)
            if read_result.status.lower () not in ['notstarted', 'running']:
                break
            print ('Waiting for result...')
            time.sleep(10)            

        pagina = 0
        if read_result.status == OperationStatusCodes.succeeded:
            trs = [ text_result for text_result in read_result.analyze_result.read_results ]
            for text_result in trs:
                lines = [ line for line in text_result.lines ]
                for line in lines:
                    line.box = shapely.geometry.box(line.bounding_box[0], line.bounding_box[1],
                            line.bounding_box[4], line.bounding_box[5])

                if not pagina % 2:
                    datos = Datos()
                    datos.pagina = pagina
                    procesar_carta(datos, lines)
                else:
                    procesar_cargo(datos, lines)
                    log.info(f"\t{datos.factura}\t{datos.fecha}\t{datos.importe}\t{datos.codigo}"
                            f"\t{datos.nombre}\t{','.join(datos.slbs)}\t{datos.comentario}\t{fich}\t{datos.pagina}")

                pagina += 1



def procesar_directorio(lc):
    path = pathlib.Path(lc.directorio)
    endpoint = lc.cp.get("READAPI", "endpoint")
    key = lc.cp.get("READAPI", "key")
    client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))
    for file in [ f for f in path.glob("*.pdf") if not "_ocr" in f.name ]: 
        procesar_fichero(client, f"{lc.directorio}/{file.name}")

if __name__ == "__main__":
    filename = os.path.expanduser("~") + "/log/porsche_readapi.log"
    logging.basicConfig(level=logging.INFO, filename=filename,
            format="%(asctime)s %(levelname)s %(thread)d %(processName)s %(module)s %(funcName)s %(message)s" )
    logging.getLogger('pdfminer').setLevel(logging.ERROR)

    directorio = "c:/temp/porsche/abonos"
    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")    
    try:
        with LocalContext(cp, directorio) as lc:
            procesar_directorio(lc)
    except Exception as e:
        log.error(e, exc_info=True)