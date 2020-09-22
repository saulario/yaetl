#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime as dt

"""
    Configuración de log
"""
LOG_FORMAT = "%(asctime)s %(levelname)s %(threadName)s %(module)s.%(funcName)s %(message)s"

"""
    Configuración de módulos de aplicación
"""

MODULO_TERRESTRE    = 1
MODULO_FACTURACION  = 1 << 1
MODULO_MARITIMO     = 1 << 2
MODULO_AEREO        = 1 << 3

MODULOS_MAXVALUE    = MODULO_TERRESTRE | MODULO_FACTURACION | \
                        MODULO_MARITIMO | MODULO_AEREO 
                    

"""
    Atributos de sesión
"""
SESSION_DURATION=dt.timedelta(hours=1)