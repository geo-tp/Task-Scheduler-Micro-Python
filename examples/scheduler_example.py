from machine import Pin
from task_scheduler import TaskScheduler, Task

class Blink(Task):
    """
    Task to blink an LED at a specified interval in ms.
    """
    def __init__(self, pin, interval):
        super().__init__(interval)
        self.led = Pin(pin, Pin.OUT)

    def loop(self):
        """
        Toggle the LED state, called at each interval in ms
        """
        self.led.value(not self.led.value())


#---------------------------------------------------------#
#                     CREATE TASKS                        #
#---------------------------------------------------------#

# TODO:Change accordingly to your board
LED_BUILTIN_PIN = "LED"
LED_PIN = 20

# Create blink tasks
blink_task1 = Blink(LED_BUILTIN_PIN, 1000) # ms
blink_task2 = Blink(LED_PIN, 500) # ms

#---------------------------------------------------------#
#                    REGISTER TASKS                       #
#---------------------------------------------------------#

# Register blink tasks
TaskScheduler.register(blink_task1)
TaskScheduler.register(blink_task2)

#---------------------------------------------------------#
#                   START SCHEDULER                       #
#---------------------------------------------------------#

# Start the scheduler loop
TaskScheduler.start()