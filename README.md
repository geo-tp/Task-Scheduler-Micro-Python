# TaskScheduler in MicroPython

## Overview

`TaskScheduler` is a simple task scheduling library written in MicroPython. It allows you to create tasks that run at specified intervals, making it easy to manage repetitive actions.

## Features

- Schedule tasks at specified intervals.
- Run tasks on multiple cores.
- Easy-to-use API for creating and managing tasks.

## Installation

To use `TaskScheduler`, copy the `task_scheduler.py` file into your MicroPython project library using Thonny IDE, mpremote or others tools.

## Usage

### Example 1: Blinking LEDs

```python
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
        Toggle the LED state at every interval in ms
        """
        self.led.value(not self.led.value())

#---------------------------------------------------------#
#                     CREATE TASKS                        #
#---------------------------------------------------------#

# TODO:Change accordingly to your board
LED_BUILTIN_PIN = "LED"
LED_PIN         = 20

# Create blink tasks
blink1 = Blink(LED_BUILTIN_PIN, 1000)  # ms
blink2 = Blink(LED_PIN, 500)           # ms

#---------------------------------------------------------#
#                    REGISTER TASKS                       #
#---------------------------------------------------------#

# Register blink tasks
TaskScheduler.register(blink1)
TaskScheduler.register(blink2)

#---------------------------------------------------------#
#                   START SCHEDULER                       #
#---------------------------------------------------------#

# Start the scheduler loop
TaskScheduler.start()
```

### Example 2: Multi-core Scheduling
```python
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
        Toggle the LED state.
        """
        self.led.value(not self.led.value())

class Button(Task):
    """
    Task to read the button state and print the result.
    """
    def __init__(self, pin, interval):
        super().__init__(interval)
        self.pin = pin
        self.button = Pin(pin, Pin.IN, Pin.PULL_UP)

    def loop(self):
        print(f"Button state : {self.button.value()}")

class Render(Task):
    """
    Task to print something at a specified interval.
    """
    def loop(self):
        print("### Hello World ###")

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
blink_task1 = Blink(LED_BUILTIN_PIN, 1000)
blink_task2 = Blink(LED_PIN, 500)

# Create button and render tasks
button_task = Button(BUTTON_PIN, 100)  # ms
render_task = Render(10000)            # ms

#---------------------------------------------------------#
#                    REGISTER TASKS                       #
#---------------------------------------------------------#

# Register blink tasks for schedulerCore0
schedulerCore0.register(blink1)
schedulerCore0.register(blink2)

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

```

## API

### TaskScheduler

- `register(task)`: Registers a task with the scheduler.
- `start()`: Starts the scheduler loop.

### Task

- `__init__(self, period)`: Initializes a new task with the specified period (in milliseconds).
- `loop(self)`: The method to be overridden by subclasses to define the task's behavior.
