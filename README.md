

register local linux server or container as IOT device in ASW console
run listener on local IOT device with the following command:

./listener.py -e <Rest API endpoint (via "Interact" menu from IOT console) -r <path to>root-CA.crt -k <path to>private.key -c <path to>.cert.pem -t bedcommands -m subscribe
