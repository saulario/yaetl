import configparser
import datetime
import logging
import os
import sys
import traceback
import uuid

from zeep import Client, Settings


YAETL_HOME = ("%s/yaetl" % os.path.expanduser("~"))
YAETL_CONFIG = ("%s/etc/yaetl.config" % YAETL_HOME)
YAETL_LOG = ("%s/log/%s.log" %
             (YAETL_HOME, os.path.basename(__file__).split(".")[0]))
logging.basicConfig(level=logging.INFO, filename=YAETL_LOG,
                    format="%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s")
log = logging.getLogger(__name__)

def get_session(contexto):
    return contexto['sesion']['SecurityProfile']['Session']['SessionId']

def get_owner(contexto):
    return contexto['sesion']['SecurityProfile']['User']['OwnerID']

def do_login(contexto):

    client = contexto['cliente']
    cp = contexto['cp']
    
    SessionInfoType = client.get_type('ns0:SessionInfo')
    sessionInfo = SessionInfoType(SessionId = str(uuid.uuid4()))
    
    UserCredentialInfoType = client.get_type('ns0:UserCredentialInfo')
    userCredentialInfo = UserCredentialInfoType(UserName = cp.get('TELETRAC', 'username')
                                                , Password = cp.get('TELETRAC', 'password')
                                                , ApplicationID = str(uuid.uuid4())
                                                , ClientID = str(uuid.uuid4())
                                                , ClientVersion = None)
    
    DoLoginRequestType = client.get_type('ns0:DoLoginRequest')
     
    doLoginRequest = DoLoginRequestType(Session = sessionInfo
                                        , UserCredential = userCredentialInfo
                                        , ClockVerificationUtc = datetime.datetime.utcnow())
        
    response = client.service.DoLogin(doLoginRequest)
    return response


def do_logoff(contexto):
    
    client = contexto['cliente']
    
    SessionInfoType = client.get_type('ns0:SessionInfo')
    sessionInfo = SessionInfoType(SessionId = get_session(contexto))    
    
    DoLogoffRequestType = client.get_type('ns0:DoLogoffRequest')
    doLogoffRequest = DoLogoffRequestType(Session = sessionInfo)

    response = client.service.DoLogoff(doLogoffRequest)
    return response
    
def get_owners(contexto):
    
    client = contexto['cliente']
    
    SessionInfoType = client.get_type('ns0:SessionInfo')
    sessionInfo = SessionInfoType(SessionId = get_session(contexto))  
    
    GetOwnersRequestType = client.get_type('ns0:GetOwnersRequest')
    getOwnersRequest = GetOwnersRequestType(Session = sessionInfo, Version = 0)
    
    response = client.service.GetOwners(getOwnersRequest)
    return response
    
    
def get_vehicles(contexto):
    
    client = contexto['cliente']

    SessionInfoType = client.get_type('ns0:SessionInfo')
    sessionInfo = SessionInfoType(SessionId = get_session(contexto))
    
    GetVehiclesRequestType = client.get_type('ns0:GetVehiclesRequest')
    getVehiclesRequest = GetVehiclesRequestType(Session = sessionInfo
                                                , Version = 0
                                                , OwnerId = get_owner(contexto)
                                                , IsProfile = False
                                                , PopulateTypeDisplayName = True
                                                )
    
    response = client.service.GetVehicles(getVehiclesRequest)
    return response


def get_vehicle_snapshots(contexto):
    
    client = contexto['cliente']

    SessionInfoType = client.get_type('ns0:SessionInfo')
    sessionInfo = SessionInfoType(SessionId = get_session(contexto))
    
    GetVehicleSnapShotRequestType = client.get_type('ns0:GetVehicleSnapShotsRequest')
    getVehicleSnapShotRequest = GetVehicleSnapShotRequestType(
            Session = sessionInfo
            , Version = 0
            , OwnerId = get_owner(contexto)
            , MaximumSerializableEventSubType = 'SMDP_EVENT_UNKNOWN'
            , FetchTemperatureData = True
            )
    
    response = client.service.GetVehicleSnapShots(getVehicleSnapShotRequest)
    return response
    

def get_period_activity(contexto):

    client = contexto['cliente']

    SessionInfoType = client.get_type('ns0:SessionInfo')
    sessionInfo = SessionInfoType(SessionId = get_session(contexto))
    
    ahora = datetime.datetime.utcnow()
    startTime = ahora - datetime.timedelta(days = 2)
    endTime = ahora - datetime.timedelta(days = 1)
    
    GetPeriodActivityExRequestType = client.get_type('ns0:GetPeriodActivityExRequest')
    getPeriodActivityExRequest = GetPeriodActivityExRequestType(
            Session = sessionInfo
            , Version = 0
            , OwnerId = get_owner(contexto)
            , StartTime = startTime
            , EndTime = endTime
            , PreviousCallEndTime = endTime
            , MaximumSerializableEventSubType = 'SMDP_EVENT_UNKNOWN'
            )
    
    response = client.service.GetPeriodActivityEx(getPeriodActivityExRequest)
    return response


def get_hos_timers(contexto):

    client = contexto['cliente']

    SessionInfoType = client.get_type('ns0:SessionInfo')
    sessionInfo = SessionInfoType(SessionId = get_session(contexto))
    
    GetHOSTimersRequestType = client.get_type('ns0:GetHOSTimersRequest')
    getHOSTimersRequest = GetHOSTimersRequestType(
            Session = sessionInfo
            , Version = 0
            , ID = get_owner(contexto)
            , RequestType = 'Owner'
            )
    
    response = client.service.GetHOSTimers(getHOSTimersRequest)
    return response


if __name__ == '__main__':
    log.info("=====> Inicio (%s)" % os.getpid())
    retval = 0
    
    contexto = {}
    try:        
        
        cp = configparser.ConfigParser()
        cp.read(YAETL_CONFIG)        
        
        contexto['cp'] = cp
        
        settings = Settings(strict = False, forbid_dtd = False, forbid_entities = False)
        contexto['cliente'] = Client(cp.get('TELETRAC','url'), settings = settings)  

        contexto['sesion'] = do_login(contexto)
        log.info("     (session): %s abierta" % get_session(contexto))
        
        contexto['owners'] = get_owners(contexto)
        contexto['vehicles'] = get_vehicles(contexto)        
        contexto['snapshot'] = get_vehicle_snapshots(contexto) 
        contexto['activity'] = get_period_activity(contexto)
        contexto['timers'] = get_hos_timers(contexto)

    except Exception as e:
        log.error(traceback.format_tb(sys.exc_info()[2]))
        log.error(e) 
        
    finally:
        do_logoff(contexto)
        log.info("     (session): %s cerrada" % get_session(contexto))
    
    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)