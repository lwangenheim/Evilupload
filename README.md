# Evilupload
## Releasing as part of the Cyberisle conference for 2023

** This is an automated tool written to show how a vulnerability on a website can be exploited using automated tooling, it is not currently functional outside of that specific use case

use is really simple: simply run the python script and enter the url of the site you're attacking, your local ip, and the port to connect on, if an upload.php file is discovered, Evilupload will create a shell.php file using a meterpreter/reverse_tcp payload and make a post request to the upload.php page. It then creates a meterpreter listener and waits for you to visit the shell.php page that was uploaded. Once that happens you should gain a meterpreter session.

##Example: 
[Cyberisle-Kali-screen0.webm](https://github.com/lwangenheim/Evilupload/assets/3094546/89cb8377-189b-4379-aa06-f41fa8d827a7)
