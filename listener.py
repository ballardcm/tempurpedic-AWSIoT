#!/usr/bin/env python

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import socket

AllowedActions = ['both', 'publish', 'subscribe']

BED1_IP = "10.0.1.177"
BED2_IP = "10.0.1.178"

UDP_PORT = 50007

flat = "3305320A945C0400CC"
pos1 = "33053203945C0000C8"
pos2 = "33053203945C0100C9"
pos3 = "33053203945c0100CA"
pos4 = "33053203945c0100CB"

# Custom MQTT message callback
def customCallback(client, userdata, message):
#    print("Received a new message: ")
	print(message.payload)
#    print("from topic: ")
#    print(message.topic)
#    print("--------------\n\n")
	bed_pos = flat
	arg = int(message.payload)
	if arg == 1:
		bed_pos = pos1
	elif arg == 2:
     		bed_pos = pos2
	elif arg == 3:
        	bed_pos = pos3
	elif arg == 4:
        	bed_pos = pos4

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	sock.sendto(bed_pos.decode("hex"), (BED1_IP, UDP_PORT))
	sock.sendto(bed_pos.decode("hex"), (BED2_IP, UDP_PORT))


# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
                    help="Operation modes: %s"%str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                    help="Message to publish")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic

if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, 443)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
if args.mode == 'both' or args.mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
#loopCount = 0
while True:
#    if args.mode == 'both' or args.mode == 'publish':
#        message = {}
#        message['message'] = args.message
#        message['sequence'] = loopCount
#        messageJson = json.dumps(message)
#        myAWSIoTMQTTClient.publish(topic, messageJson, 1)
#        if args.mode == 'publish':
#            print('Published topic %s: %s\n' % (topic, messageJson))
#        loopCount += 1
    time.sleep(1)
