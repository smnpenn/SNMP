import snmp

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

    ip=input("Geben Sie eine IP-Adresse an: ")

    resultarray = snmp.get(ip, oidarray, "public")

    counter=0

    for i in oidarray:
        print(oidname[counter] + str(resultarray[i]))
        counter=counter+1