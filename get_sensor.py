#!/usr/bin/python3

import requests
import json
import paho.mqtt.client as mqtt
import sys


#################################################
#
#   STATIC VARIABLES
#
#################################################
_deconzApiCode = ""
_deconzIPAddress = ""
_deconzPort = ""
_deconzUrl = "http://" + _deconzIPAddress + ":" + _deconzPort + "/api/" + _deconzApiCode + "/sensors"

_brokerIP = ""
_brokerPort = 
_brokerUsername = ""
_brokerPassword = ""


#################################################
#
#   FUNCTIONS
#
#################################################
def on_publish( client, userdata, mid ):             #create function for callback
  print ( "data published" )
  pass

##################################################
#
#    MAIN
#
##################################################
try:
  response = requests.get( _deconzUrl )
except :
  print ( "Error. Deconz Api is unreachable" )
  sys.exit( 1 )

if response.status_code == 200:
  try:
    dictObj = response.json()
  except Exception as err:
    print ( response.json( ) )
    print ( err )
else:
  print ( 'Erreur lors de la recuperation sur l\'api {}. Code retour : {}'.format( _url, response.status_code ) )


client= mqtt.Client("control1")                            #create client object
client.on_publish = on_publish                             #assign function to callback
client.username_pw_set( _brokerUsername, _brokerPassword ) #set username and password to connection

try:
  client.connect( _brokerIP, _brokerPort )                 #establish connection
except Exception as err:
  print ( err )
  print ( "Connection failed" )

battery = []
for key in dictObj:
  if dictObj[key]["name"] not in battery:
    battery.append( dictObj[key]["name"] )
    topic = dictObj[key]["name"] + '/battery'
    try:
      ret = client.publish( topic, dictObj[key]["config"]["battery"] ) 
    except Exception as err:
      pass
  if dictObj[key]["type"] == "ZHAHumidity":
    topic = dictObj[key]["name"] + '/humidity'
    ret = client.publish( topic, dictObj[key]["state"]["humidity"] / 100 )
  elif dictObj[key]["type"] == "ZHATemperature":
    topic = dictObj[key]["name"] + '/temperature'
    ret = client.publish( topic, dictObj[key]["state"]["temperature"] / 100 )
  elif dictObj[key]["type"] == "ZHAPressure":
    topic = dictObj[key]["name"] + '/pressure'
    ret = client.publish( topic, dictObj[key]["state"]["pressure"] )
 
