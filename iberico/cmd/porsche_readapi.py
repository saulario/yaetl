#!/usr/bin/python3
import configparser
import logging
import os
import pathlib
import time

import shapely.geometry

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from shapely.geometry.geo import shape

log = logging.getLogger(__name__)

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
        self.conn.close()

class Carta():
    #factura = shapely.geometry.box(6.2948, 3.4234, 6.8866, 3.5526)
    #fecha = shapely.geometry.box(6.2732, 3.2296, 6.9619, 3.3481)
    #importe = shapely.geometry.box(6.5422, 7.1483, 7.4353, 7.3098)

    factura = shapely.geometry.box(6.2948, 3.4234, 6.8866, 3.5526)
    fecha = shapely.geometry.box(6.2732, 3.2296, 6.9619, 3.3481)
    importe = shapely.geometry.box(6.2, 7.1, 7.5, 7.4)


    comentario = shapely.geometry.box(1.7216, 5.2751, 2.873, 5.415)
    codigo = shapely.geometry.box(1.1298, 6.1471, 1.7324, 6.287)
    nombre = shapely.geometry.box(4.8314, 6.104, 5.6061, 6.2547)
    slbs = shapely.geometry.box(2.3457, 6.1363, 5.0, 14.0)


class Datos():
    pagina = 0
    fecha = None
    factura = None
    importe = None
    comentario = None
    codigo = None
    nombre = None
    slbs = None

def procesar_carta(datos, lineas):
    datos.pagina += 1
    for f in [ f for f in lineas if f.box.almost_equals(Carta.factura, decimal=1) ]:
        datos.factura = f.text
        break
    for f in [ f for f in lineas if f.box.almost_equals(Carta.fecha, decimal=1) ]:
        datos.fecha =  f.text
        break
    for f in [ f for f in lineas if f.box.within(Carta.importe) ]:
        datos.importe = f.text
        break

def procesar_cargo(datos, lineas):
    for f in [ f for f in lineas if f.box.almost_equals(Carta.comentario) ]:
        datos.comentario = f.text
        break
    for f in [ f for f in lineas if f.box.almost_equals(Carta.codigo) ]:
        datos.codigo = f.text
        break
    for f in [ f for f in lineas if f.box.almost_equals(Carta.nombre) ]:
        datos.nombre = f.text
        break    
    datos.slbs = [ f.text for f in lineas if f.box.within(Carta.slbs) ]

def procesar_fichero(client, fich):
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
                    procesar_carta(datos, lines)
                else:
                    procesar_cargo(datos, lines)

                print("aquí estoy")
                

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