import time
import subprocess
import getopt, sys
import json


mac_addresses = []
mac_vendors = []
ip_addresses = []
isp_info =[]

isp_clean = ""

def main():

    argumentList = sys.argv[1:]
    options = "hmioa:"

    long_options = ["HELP", "IP", "MAC", "Output ="]


    if bool(argumentList) == True:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        
        # checking each argument
        for currentArgument, currentValue in arguments:
        
            #displays help prompt
            if currentArgument in ("-h", "--HELP"):
                print("""MAC Address lookup tool: \n
        COMMANDS:\n
        -m --MAC : Lookup an individual mac address \n
        EX: connections.py -m <arg>\n
        -i -IP : Find the IP Address and ISP Info of the current machine.\n
        EX: connections.py -i\n
        DEFAULT : If no argument given, the script will run with DEFAULT settings,
        which finds all MAC addresses on system and finds IP/ISP info.""")

            #lookup for single mac address        
            elif currentArgument in ("-m", "--MAC"):
                single_mac = [sys.argv[2]]
                single_lookup = maclookup(single_mac)
                print (single_lookup)
            #looks up just the IP
            elif currentArgument in ('-i', "--IP"):
                onlyip = iplookup()
                clean_ip = cleandict(onlyip)

                print(onlyip)
                
                    
            #Prints error if no valid arg given
            else:
                print ("Invalid Argument! please see --HELP file for list of commands!")

    else:
        print("Finding connections in defaul configuration...\n\n")
        time.sleep(1)

        mac_stdout = subprocess.check_output(['arp', '-e'])
        
        mac_split = str(mac_stdout).split()
        maddresses = []
        for arps in mac_split:
            if ":" in arps:
                maddresses.append(arps)

        
        maclookup(maddresses)
        
        
        isp_finder = iplookup()
        clean_ip = cleandict(isp_finder)


        print("Connected network devices:\n")
        for macs in mac_vendors:
            print(macs)
        print("\n\nCurrent IP Information: \n")
        print(clean_ip)

       

def cleandict(dict):

    pOne = dict.replace("{", "")

    pTwo = pOne.replace("}", "")

    pThree = pTwo.replace("u'", "")

    pFour = pThree.replace("'", "")

    pFive = pFour.replace(",", "\n")

    return pFive


def cleantext(txt):
    part_one = txt.replace("b'", "")
    part_two = part_one.replace("'", "")
    return part_two        

#looks up vendor and appends as a list of dictionaries
def maclookup(mac):
    
    for macs in mac:
        url = "https://api.maclookup.app/v2/macs/" + macs
        
        lookup = subprocess.check_output(['curl', '-s', str(url)])
        mac_result = json.loads(lookup)
        
        
        time.sleep(0.5)
        mac_vendors.append({macs:mac_result['company']})
    
    return mac_vendors
        

#looks up IP and appends to list of dictionaries
def iplookup():

    findip = subprocess.check_output(['curl', '-s', 'ifconfig.me'])
    ip_found = cleantext(str(findip))
    url = "http://ip-api.com/json/%s?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,query" %ip_found
    ip_info = subprocess.check_output(['curl', '-s', url])
    cleaninfo = cleantext(str(ip_info))
    ip_results = json.loads(cleaninfo)
    isp_info.append(ip_results)

    str_isp_info = str(isp_info)
    clean_isp = cleandict(str_isp_info)
    

    return clean_isp




if __name__ == "__main__":
    main()
