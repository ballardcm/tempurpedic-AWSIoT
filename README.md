
steps to get working.. 

set your bed positions with the bed remote (currently only Positions 1, 2, and flat (0) work) 

register local linux server or container as IOT device in AWS console

deploy lambda function

create alexa skill calling lambda function

edit listener to reflect your tempurpedic bed wifi module(s) IP address(es)

(my bed has two modules, each operate independently)

run listener on local IOT device with the following command:

./listener.py -e <Rest API endpoint (via "Interact" menu from IOT console) -r <path to>root-CA.crt -k <path to>private.key -c <path to>.cert.pem -t bedcommands -m subscribe


