from openpyxl.styles import Font
from openpyxl import Workbook
import subprocess
import requests
import winapps
import nmap
import os

# Constants
SUBNET = "10.164.169.1/24"
IGNORE_LIST = ["AC:8B:A9:B2:2C:83","N/A", "B8:AE:ED:7D:12:A8"]

# Search for Nmap on PC
for _ in winapps.search_installed('Nmap'):
    nmap_installed = True


if (nmap_installed == False):
    print("!!! Nmap is not installed. Please install it first !!!")
    print("Windows: https://nmap.org/download.html")

else:

    wb = Workbook()         # Create a Workbook
    ws = wb.active          # Get the active worksheet
    ft = Font(bold=True)    # Create bold font styler

    nm = nmap.PortScanner() # Create a new nmap scanner
    nm.scan(hosts=SUBNET, arguments='-sn')  # Performs a ping scan (-sn) for actice hosts

    recorder_data = [["IP", "MAC ADDRESS", "HARDWARE ID"]]

    for host in nm.all_hosts():
        ip = host
        mac = nm[host]['addresses'].get('mac', 'N/A')
        hardware_id = requests.get(f"https://{ip}/licensing/product/hardwareid", verify = False)   #This may need to be moved to inside if statement


        if not mac in IGNORE_LIST:
            recorder_data.append([ip, mac, hardware_id.text])

    for row in recorder_data:   # Add Recorder data to excel sheet
        ws.append(row)

    for row in ws["A1":"C1"]:   # Bold header row
        for cell in row:
            cell.font = ft

    wb.save("RecorderData.xlsx")
