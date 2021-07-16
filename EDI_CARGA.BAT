@ECHO OFF
REM ************************************
REM EJECUTA LA CARGA DE ESTADÍSTICAS EDI

SET PYTHONPATH=%CD%

python edi\cmd\cargar_ficheros.py -b SSIW6
python edi\cmd\cargar_ficheros.py -b SSRKD
python edi\cmd\cargar_ficheros.py -b SESEMEXICO
python edi\cmd\cargar_ficheros.py -b SESESILS