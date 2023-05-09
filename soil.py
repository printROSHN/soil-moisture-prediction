import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

	
time.sleep(30)

 

username = "29bc81b0-e987-11ed-8485-5b7d3ef089d0"

password = "a693ac14a843151de72620980d3e2c8dfb5a2f5c"

clientid = "1c2fcf60-ec44-11ed-9ab8-d511caccfe8c"

 

mqttc = mqtt.Client(client_id=clientid)

mqttc.username_pw_set(username, password=password)

mqttc.connect("mqtt.mydevices.com", port=1883, keepalive=60)

mqttc.loop_start()

soil_sense = "v1/" + username + "/things/" + clientid + "/data/1"

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pin for soil moisture sensor
moisture_sensor_pin = 14

# Set GPIO pin as input
GPIO.setup(moisture_sensor_pin, GPIO.IN)

# Define function to read sensor value
def read_sensor():
    # Read sensor value
    sensor_value = GPIO.input(moisture_sensor_pin)
    # Return sensor value
    return sensor_value

def write_to_cloud(val):
	try:
		if val is not None:
			temp11 = "temp,c=" + str(val)
			mqttc.publish(soil_sense, payload=val, retain=True)
			
		time.sleep(5)
	except (EOFError, SystemExit, KeyboardInterrupt):
		mqttc.disconnect()
		sys.exit()

# Main loop
c = False
while True:
	value = read_sensor()
	if value == 1:
		print("No Water")
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(27,GPIO.OUT)
		print ("LED on")
		GPIO.output(27,GPIO.HIGH)
		time.sleep(1)
		if(c == False):
			c = True
			write_to_cloud(value)
		print ("LED off")
		GPIO.output(27,GPIO.LOW)
	else:
		print("Water")
		if(c):
			c = False
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(17,GPIO.OUT)
		print ("LED on")
		GPIO.output(17,GPIO.HIGH)
		time.sleep(1)
		write_to_cloud(value)
		print ("LED off")
		GPIO.output(17,GPIO.LOW)

	time.sleep(3)
	
