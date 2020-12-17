import snmp
import pysnmp
import socket
from threading import Thread
import ipaddress

def thread_function(ip, name):

    try:
        resultarray=snmp.get(str(ip), oidarray, "public", True)

        counter=0
        for i in oidarray:
            print(oidname[counter]+ str(resultarray[i]))
            counter=counter+1
    except pysnmp.smi.error.PySnmpError:
        pass


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


    while True:

        command=input("Geben Sie einen Befehl ein: ")

        if(command=="/get"):
            ip=input("Geben Sie eine IP-Adresse an: ")
            try:
                communitystr=input("Geben Sie den Communitystring ein (Bei keiner Eingabe wird 'public' verwendet (ENTER)): ")
                if(communitystr==""):
                    communitystr="public"

                resultarray = snmp.get(ip, oidarray, communitystr)

                counter=0
            
                for i in oidarray:
                    print(oidname[counter] + str(resultarray[i]))
                    counter=counter+1
            except pysnmp.smi.error.PySnmpError: 
                print("ERROR: Can't find informations for this address and/or communitystring\n")

            input("Drücken Sie ENTER um fortzufahren\n")
        elif(command=="/scan"):
            network=input("Geben Sie das Netzwerk (mit Subnetzmaske) ein was sie scannen möchten: ")
            print("...")

            threads=[]
            for ip in ipaddress.IPv4Network(network):
                thread=Thread(target=thread_function, args=(ip, 1,))
                thread.start()
                threads.append(thread)
            
            for t in threads:
                t.join()
            

            print("Done!")
            input("Drücken Sie ENTER um fortzufahren\n")

