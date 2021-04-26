#!/usr/bin/python3

import logging
import os
import pathlib
import shutil

log = logging.getLogger(__name__)


def main():
    fromDir = pathlib.Path(r"\\promtb1\d$\Ficheros\Porsche\IN\VDA4987\procesados")
    toDir = r"c:\temp\porsche\vda4987"

    for p in fromDir.iterdir():
        log.info(f"\tprocesando {p.name}")
        if not p.is_dir(): continue
        if not p.name.startswith("2021"): continue
        
        files = list(p.glob("*4987.TXT"))
        for file in files:
            log.info(f"\t\t{file.name}")
            tofile = f"{toDir}/{file.name}"
            shutil.copyfile(str(file), tofile, follow_symlinks=False)



if __name__ == "__main__":
    f = pathlib.Path(__file__).stem
    filename = os.path.expanduser("~") + f"/log/{f}.log"
    logging.basicConfig(level=logging.DEBUG, filename=filename,
            format="%(asctime)s %(levelname)s %(thread)d %(processName)s %(module)s %(funcName)s %(message)s" )
    log.info("-----> Info")
    try:
        main()
    except:
        log.error("Se ha producido una excepción no controlada...", exc_info=True)
    log.info("<----- Fin")