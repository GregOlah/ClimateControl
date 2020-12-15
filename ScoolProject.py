import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import io

GPIO.setmode(GPIO.BCM) 
GPIO.setup(22, GPIO.OUT)
sensor = Adafruit_DHT.DHT11
temp_sensor_pin = 4
GPIO.setup(17, GPIO.IN, GPIO.PUD_UP)
GPIO.setwarnings(False)
starttempfloat = 25.0
stoptempfloat = 22.0
starttemp = str(starttempfloat)
stoptemp = str(stoptempfloat)

prev_input = 1
BUTTON=17
input = GPIO.input(BUTTON)
GPIO.cleanup()


running = True

file = open('/mnt/tempdata/temp_over_time.txt', 'w')
file.write('time and date, temperature (C),temperature (F), humidity\n')

while running:
    while prev_input != input:
        print ("Window is closed")
    

        try:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, temp_sensor_pin)

            temperature_f = temperature * 9/5.0 + 32

            if humidity is not None and temperature is not None:

                #print temperature and humidity
                print('Temperature = ' + str(temperature) +','+ 'Temperature Fahrenheit = ' + str(temperature_f) +',' + 'Humidity = ' + str(humidity))
                #save time, date, temperature in Celsius, temperature in Fahrenheit and humidity in .txt file
                file.write(time.strftime('%H:%M:%S %d/%m/%Y') + ', ' + str(temperature) + ', '+ str(temperature_f)+',' + str(humidity) + '\n')
                if str(temperature)>starttemp:
                    GPIO.output(22, GPIO.LOW)
                if str(temperature)<stoptemp:
                    GPIO.output(22, GPIO.HIGH)
                time.sleep(1)

            else:
                print('Failed to get reading. Try again!')
                time.sleep(1)

        except KeyboardInterrupt:
            print ('Program stopped')
            running = False
            file.close()
