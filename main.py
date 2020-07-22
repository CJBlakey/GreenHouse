import RPi.GPIO as GPIO
from time import sleep
from w1thermsensor import W1ThermSensor
import coloredlogs, logging, os, threading


def init():
    # Setup static variables for later use here.
    # Motor variables
    global in1
    in1 = 24
    global in2
    in2 = 23
    global en
    en = 25
    global temp1
    temp1 =1

    # Temp reader variables
    global stasis_temp
    stasis_temp = 29
    global high_temp
    high_temp = 35
    global low_temp
    low_temp = 23

    global sensor_array
    sensor_array = []
    global number_of_sensors
    number_of_sensors= 5
    global temp_readings
    temp_readings = []
    global average_temperature
    average_temperature = 0
    try:
        for i in range(number_of_sensors):
            sensor_array[i] = W1ThermSensor
            logging.info(sensor_array[i])
    except Exception as e:
        logging.error(e)

def motor_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.setup(en,GPIO.OUT)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    p=GPIO.PWM(en,1000)
    p.start(25)
    logging.info("The default speed & direction of motor is LOW & Forward.....")
    logging.info("r-run s-stop f-forward b-backward e-exit")


def temp_average():
    for i in range(number_of_sensors):
        temp_readings.append(sensor_array[i].get_temperature())
        logging.info(sensor_array[i].get_temperature())

def forward():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    logging.info("Accelerated Motor")

def backward():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    logging.info("Reversed Motor")

def stop():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    logging.info("Stopped Motor")


def main():
        # instantiate a thread for the sermon instance.
    threading.current_thread().name = 'SerMon MK2'
    logging.basicConfig(level=logging.DEBUG, filemode="W")
    logParser = logging.Formatter(
        "[%(asctime)s - %(levelname)s] [%(filename)s:%(lineno)s - %(funcName)s()- %(threadName)s] %(message)s",
        "%Y-%m-%d %H:%M:S")
    coreLogger = logging.getLogger()
    coreLogger.handlers = []
    fileHandler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.log"))
    fileHandler.setFormatter(logParser)
    coreLogger.addHandler(fileHandler)
    coloredlogs.install(level="DEBUG",
                        fmt="[%(asctime)s - %(levelname)s] [%(filename)s:%(lineno)s - %(funcName)s() - %(threadName)s] %(message)s")
    init()
    motor_setup()
    while 1:
        temp_average()

        if average_temperature > high_temp:
            forward()
        elif average_temperature < low_temp:
            backward()


if __name__ == '__main__':
    main()
