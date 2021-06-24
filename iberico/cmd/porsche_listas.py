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
        lines = []
        textos = []
        if read_result.status == OperationStatusCodes.succeeded:
            trs = [ text_result for text_result in read_result.analyze_result.read_results ]
            for text_result in trs:
                pagina += 1
                ll = [ line for line in text_result.lines ]
                for l in ll:
                    setattr(l, "pag", pagina)
                    setattr(l, "posx", round(l.bounding_box[0], 2))
                    setattr(l, "posy", round(l.bounding_box[1], 2))
                    lines.append(l)

        aux = lines[:]
        aux.sort(key=lambda x: x.pag * 100 + x.posy)

        buff = None
        yant = None
        for l in aux:
            if yant != l.posy:
                if yant: log.info(buff)
                buff = f"\t{l.pag}\t{str(l.posy).replace('.',',')}"           
            buff += f"\t{l.text}"
            yant = l.posy
            


            



def procesar_directorio(lc):
    path = pathlib.Path(lc.directorio)
    endpoint = lc.cp.get("READAPI", "endpoint")
    key = lc.cp.get("READAPI", "key")
    client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))
    for file in [ f for f in path.glob("*.pdf") ]: 
        procesar_fichero(client, f"{lc.directorio}/{file.name}")

if __name__ == "__main__":
    filename = os.path.expanduser("~") + "/log/porsche_listas.log"
    logging.basicConfig(level=logging.INFO, filename=filename,
            format="%(asctime)s %(levelname)s %(thread)d %(processName)s %(module)s %(funcName)s %(message)s" )
    logging.getLogger('pdfminer').setLevel(logging.ERROR)

    directorio = "c:/temp/porsche/listas"
    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")    
    try:
        with LocalContext(cp, directorio) as lc:
            procesar_directorio(lc)
    except Exception as e:
        log.error(e, exc_info=True)