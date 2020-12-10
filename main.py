import snmp

if __name__ == "__main__":
    oidarray = []
    oidarray.append(".1.3.6.1.2.1.1.1.0")
    oidarray.append(".1.3.6.1.2.1.1.5.0")
    oidarray.append(".1.3.6.1.2.1.1.4.0")
    oidarray.append(".1.3.6.1.2.1.25.2.2.0")

    resultarray = snmp.get("localhost", oidarray, "public")
    print("Seoo")

    print(resultarray[1])