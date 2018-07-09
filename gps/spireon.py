import logging
import requests

log = logging.getLogger(__name__)

def asset(context, url, id):
    log.info("-----> Inicio")    
    log.info("       (url): %s" % url)
    log.info("       (id) : %s" % id)
    
    
    r = requests.get(url + "/api/asset" , auth=(id, id))
    
    log.info(r.json())
    
    
    log.info("<----- Fin")
    
def assetTraffic(context, url, id):
    log.info("       (url): %s" % url)
    log.info("       (id) : %s" % id)
    
    
    
    log.info("<----- Fin")