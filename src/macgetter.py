import subprocess
import requests
import nmap
import os
from nicegui import ui

### FOR REFERENCE ONLY ###

# Set up columns
columns = [
    {'name': 'ip', 'label': 'IP ADDRESS', 'field': 'ip', 'required': True, 'align': 'left'},
    {'name': 'mac', 'label': 'MAC ADRRESS', 'field': 'mac', 'required': True, 'align': 'left'},
    {'name': 'hw', 'label': 'HARDWARE ID', 'field': 'hw', 'required': True, 'align': 'left'},
    {'name': 'copy', 'label': '', 'align': 'center', 'required': True},
]


def copy_to_clipboard(mac):
    """Uses browser clipboard API (client-side JS)."""
    ui.run_javascript(f"navigator.clipboard.writeText('{mac}')")
    ui.notify(f"Copied {mac} to clipboard!", type='positive')



def scan_subnet(subnet, output_file):
    """ Run a subnet scan and write results to NiceGUI table element."""
    # Create a new nmap scanner
    nm = nmap.PortScanner()

    print(f"Scanning subnet: {subnet} ... This may take a few seconds.")

    # Perform a ping scan (-sn) to find active hosts
    nm.scan(hosts=subnet, arguments='-sn')

    # Open file for writing results
    with open(output_file, 'w') as file:
        file.write("IP Address\tMAC Address\n")
        file.write("="*40 + "\n")

        for host in nm.all_hosts():
            ip = host
            mac = nm[host]['addresses'].get('mac', 'N/A')
            

            if not mac in ignoreList:
                hardware_id = requests.get("https://10.164.169.173/licensing/product/hardwareid", verify = False)
                table.add_row({f'ip': ip, 'mac': mac, 'hw': hardware_id.text})     # Adds row for each new entry
                file.write(f"{ip}\t{mac}\t{hardware_id.text}\n")
                
    
    print(f"Scan complete. Results saved to {output_file}")



table = ui.table(columns=columns, rows=[], row_key='ip')

table.add_slot('body-cell-copy', '''
    <q-td :props="props">
        <q-btn label="Copy" @click="() => $parent.$emit('copy', props.row)" flat />
    </q-td>
''')

table.on('copy', lambda e: copy_to_clipboard(e.args['mac']))

ui.dark_mode(True)
ui.run()

if __name__ == "__main__":
    subnet = "10.164.169.1/24"
    output_file = "C:\\Users\\Manufacturing\\Desktop\\Mac Getter\\MAC Addresses.txt" 
    ignoreList= ["AC:8B:A9:B2:2C:83","N/A", "B8:AE:ED:7D:12:A8"]
    
    # Check if nmap is installed
    if os.system("nmap -v >nul 2>&1") != 0:
        print("⚠️ Nmap is not installed. Please install it first.")
        print("Windows: https://nmap.org/download.html")
        print("Linux: sudo apt install nmap")
    else:
        scan_subnet(subnet, output_file)

