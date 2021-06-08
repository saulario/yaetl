#!/usr/bin/python3
import io
import logging
import os
import pathlib
import re

import pdfminer, pdfminer.converter, pdfminer.pdfdocument, pdfminer.pdfinterp, \
        pdfminer.layout, pdfminer.pdfparser, pdfminer.pdfpage
import pdfminer.high_level, pdfminer.layout
import PyPDF2


log = logging.getLogger(__name__)


fecha_re = re.compile(r"(?P<fecha>\d{2}\.\d{2}\.\d{4})")
brutto_re = re.compile(r"^S{0,1}u{0,1}m{0,1}m{0,1}e{0,1}\s{0,1}B{0,1}r{0,1}u{0,1}t{0,1}t{0,1}o{0,1}\n$")
importe_re = re.compile(r"^(?P<importe>\d+,\d+)\s*EUR$")

class Datos():
    fecha = None
    factura = None
    importe = None

def procesar_ficheroxx(nombre):
    with open(nombre, "rb") as f:
        reader = PyPDF2.PdfFileReader(f)
        info = reader.documentInfo
        contents = reader.getPage(0).getContents()
        print(info)

def procesar_ficheroxxx(nombre):
    with open(nombre, "rb") as f:
        parser = pdfminer.pdfparser.PDFParser(f)
        doc = pdfminer.pdfdocument.PDFDocument(parser)
        rsrcmgr = pdfminer.pdfinterp.PDFResourceManager()
        output_string = io.StringIO()
        device = pdfminer.converter.TextConverter(rsrcmgr, output_string, laparams=pdfminer.layout.LAParams())
        interpreter = pdfminer.pdfinterp.PDFPageInterpreter(rsrcmgr, device)
        for page in pdfminer.pdfpage.PDFPage.create_pages(doc):
            interpreter.process_page(page)
            print(output_string.getvalue())


def factura_fecha(datos, page_layout):
    i = 0
    encontrado = False
    for element in page_layout:
        if i >= 10: break
        i += 1
        texto = element.get_text()
        if encontrado:
            datos.factura = texto
            break
        m = fecha_re.match(texto)
        if m:
            datos.fecha = m.group("fecha")
            encontrado = True


def procesar_fichero(nombre):
    datos = None
    factura = False
    fecha_fra = False
    importe = False
    albaranes = False
    for page_layout in pdfminer.high_level.extract_pages(nombre):

        if page_layout.pageid % 2:
            if datos:
                log.info(f"\t{datos.factura}\t{datos.fecha}\t{datos.importe}")
            datos = Datos()

        elements = [ x for x in page_layout if isinstance(x, pdfminer.layout.LTTextContainer) ]
        for element in elements:
            texto = element.get_text()
            if "Belastungsanzeige" in texto:
                factura = True
                datos = Datos()
            m = brutto_re.match(texto)
            if m:
                importe = True
            if "Bezugnummern" in texto:
                albaranes = True
            if "Differenzbetrag" in texto or "Zahlbetrag" in texto:
                albaranes = False
            if fecha_fra:
                factura = fecha_fra = False
                datos.factura = texto[:-1] if texto else ""
            if factura:
                m = fecha_re.match(texto)
                if not m: continue
                datos.fecha = m.group("fecha").replace(".", "/")
                fecha_fra = True
            if importe:
                m = importe_re.match(texto)
                if m:
                    datos.importe = float(m.group("importe").replace(",", "."))
                    importe = False





def procesar_directorio(p):
    path = pathlib.Path(p)
    for file in [ f for f in path.glob("*.pdf") if "_ocr" in f.name ]: 
        procesar_fichero(f"{p}/{file.name}")


if __name__ == "__main__":
    filename = os.path.expanduser("~") + "/log/porsche_pdf.log"
    logging.basicConfig(level=logging.INFO, filename=filename,
            format="%(asctime)s %(levelname)s %(thread)d %(processName)s %(module)s %(funcName)s %(message)s" )
    logging.getLogger('pdfminer').setLevel(logging.ERROR)

    procesar_directorio("c:/temp/porsche/abonos")