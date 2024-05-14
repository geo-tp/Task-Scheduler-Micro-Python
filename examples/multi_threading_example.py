import _thread
from machine import Pin
from task_scheduler import TaskScheduler, Task

class Blink(Task):
    """
    Task to blink an LED at a specified interval.
    """
    def __init__(self, pin, interval):
        super().__init__(interval)
        self.led = Pin(pin, Pin.OUT)

    def loop(self):
        """
        Toggle the LED state, called at each interval in ms
        """
        self.led.value(not self.led.value())

class Button(Task):
    """
    Task to read the button state and print the result.
    """
    def __init__(self, pin, interval):
        super().__init__(interval)
        self.button = Pin(pin, Pin.IN, Pin.PULL_UP)

    def loop(self):
        print(f"Button state : {self.button.value()}")

class Render(Task):
    """
    Task to print something at a specified interval.
    """

    def loop(self):
        print("RENDER LOOP : Hello World")


#---------------------------------------------------------#
#           CREATE A SCHEDULER FOR EACH CORE              #
#---------------------------------------------------------#

# Create two separate schedulers
schedulerCore0 = TaskScheduler()
schedulerCore1 = TaskScheduler()

#---------------------------------------------------------#
#                     CREATE TASKS                        #
#---------------------------------------------------------#

# TODO:Change accordingly to your board
LED_BUILTIN_PIN = "LED"
LED_PIN         = 20
BUTTON_PIN      = 18

# Create blink tasks
blink_task1 = Blink(LED_BUILTIN_PIN, 1000) # ms
blink_task2 = Blink(LED_PIN, 500) # ms

# Create button and render tasks
button_task = Button(BUTTON_PIN, 100) # ms
render_task = Render(10000) # ms

#---------------------------------------------------------#
#                    REGISTER TASKS                       #
#---------------------------------------------------------#

# Register blink tasks for schedulerCore0
schedulerCore0.register(blink_task1)
schedulerCore0.register(blink_task2)

# Register button and render tasks for schedulerCore1
schedulerCore1.register(button_task)
schedulerCore1.register(render_task)

#---------------------------------------------------------#
#                   START SCHEDULERS                      #
#---------------------------------------------------------#

# Start the schedulerCore0 on the main thread
schedulerCore0.start()

# Start the schedulerCore1 on a new thread
_thread.start_new_thread(schedulerCore1.start, ())