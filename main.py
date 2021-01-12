import snmp
import pysnmp
import socket
from threading import Thread
import ipaddress

def thread_function(ip, oid, name):

    try:
        snmp.get(str(ip), oid, "public", True)

    except pysnmp.smi.error.PySnmpError:
        pass
    except ip.AddressValueError:
        print("ERROR: Network addrss not valid!")


if __name__ == "__main__":

    uptime = "1.3.6.1.2.1.1.3.0"
    contact =  "1.3.6.1.2.1.1.4.0"
    name = "1.3.6.1.2.1.1.5.0"
    location = "1.3.6.1.2.1.1.6.0"
    systemdescription = "1.3.6.1.2.1.1.1.0"
    processnumber = "1.3.6.1.2.1.25.1.6.0"
    ramsize = "1.3.6.1.2.1.25.2.2.0"

    oidarray = []
    oidarray.append(uptime)
    oidarray.append(contact)
    oidarray.append(name)
    oidarray.append(location)
    oidarray.append(systemdescription)
    oidarray.append(processnumber)
    oidarray.append(ramsize)

    oidname=[]
    oidname.append("uptime: ")
    oidname.append("contact: ")
    oidname.append("name: ")
    oidname.append("location: ")
    oidname.append("systemdescription: ")
    oidname.append("processnumber: ")
    oidname.append("ramsize: ")

    print("Willkommen im SNMP-Tool von Simon Penn!")
    print("Geben Sie /help ein um zu sehen welche Befehle für sie verfügbar sind!\n")


    while True:

        command=input("Geben Sie einen Befehl ein: ")

        if(command=="/get"):
            ip=input("Geben Sie eine IP-Adresse ein: ")
            try:
                communitystr=input("Geben Sie den Communitystring ein (Bei keiner Eingabe wird 'public' verwendet (ENTER)): ")
                if(communitystr==""):
                    communitystr="public"

                resultarray = snmp.getMoreOIDs(ip, oidarray, communitystr)

                counter=0
            
                for i in oidarray:
                    print(oidname[counter] + str(resultarray[i]))
                    counter=counter+1
            except pysnmp.smi.error.PySnmpError: 
                print("ERROR: Can't find informations for this address and/or communitystring\n")
            except IndexError:
                print("ERROR: Can't find informations for this address and/or communitystring\n")

            input("Drücken Sie ENTER um fortzufahren\n")
        elif(command=="/scan"):
            network=input("Geben Sie das Netzwerk (mit Subnetzmaske) ein was sie scannen möchten: ")
            oid=input("Geben Sie eine OID ein, die von den einzelnen Hosts ausgelesen werden soll (Bei keiner Eingabe wird der Hostname ausgelesen (ENTER))")
            print("Bitte warten, diese Operation kann ein bisschen dauern...")
            if(oid==""):
                oid="1.3.6.1.2.1.1.5.0"

            threads=[]
            for ip in ipaddress.IPv4Network(network):
                
                thread=Thread(target=thread_function, args=(ip, oid, 1,))
                thread.start()
                threads.append(thread)
                
            
            for t in threads:
                t.join()
            

            print("Done!")
            input("Drücken Sie ENTER um fortzufahren\n")
        elif(command=="/getbyoid"):
            oid=input("Geben Sie die OID ein: ")
            ip=input("Geben Sie eine IP-Adresse ein: ")
            try:
                communitystr=input("Geben Sie den Communitystring ein (Bei keiner Eingabe wird 'public' verwendet (ENTER)): ")
                if(communitystr==""):
                    communitystr="public"
                result=snmp.get(ip, oid, communitystr)
                
                print(str(result))
            except pysnmp.smi.error.MibNotFoundError:
                print("ERROR: OID not valid!")
            except pysnmp.smi.error.PySnmpError: 
                print("ERROR: Can't find informations for this address and/or communitystring\n")
            input("Drücken Sie ENTER um fortzufahren\n")
        elif(command=="/help"):
            print("Ihre verfügbaren Befehle sind:\n/get --> mehrere Informationen (uptime, contact, name, location, systemdescription, processnumber, ramsize) über einen bestimmten Host\n/scan --> Sie erhalten alle Namen der Hosts in ihrem Netzwerk, die SNMP aktiviert/konfiguriert haben\n/getbyoid --> Sie erhalten eine bestimmte Information von einem bestimmten Host\n")
        else:
            print("Ungültiger Befehl\nGeben Sie '/help' ein um zu sehen welche Befehle für Sie verfügbar sind.")

