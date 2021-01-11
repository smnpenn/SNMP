from pysnmp import hlapi
from pysnmp.hlapi import *
import ipaddress
import os
from threading import Thread


def getMoreOIDs(target, oids, credentials):  #für /get um mehrere Informationen auszulesen
    handler = getCmd(
        SnmpEngine(),
        CommunityData(credentials),
        UdpTransportTarget((target, 161)),
        ContextData(),
        *construct_object_types(oids)
    )

    return fetch(handler, 1)[0]

def get(target, oid, credentials, scanNetwork=False): #für /scan und /getbyoid um eine Information auszulesen
    handler= getCmd(
        SnmpEngine(),
        CommunityData(credentials),
        UdpTransportTarget((target, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(handler)
    
    if errorIndication:             #wenn Fehler auftritt und der Befehl nicht /scan war gibt es eine Fehlermeldung aus, dass die IP nicht erreichbar ist
        if scanNetwork == False:
            print("Host " + target + " nicht erreichbar!")
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        if scanNetwork:
            for varBind in varBinds:
                print(target + ": " + varBind[1])
        else:
            for varBind in varBinds:
                return varBind[1]

def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types


def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
        except StopIteration:
            break
    return result


def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value


