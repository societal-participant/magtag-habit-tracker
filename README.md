# Maggie's MagTag Habit Tracker
This repository contains a Habit Tracker app I created for the Adafruit Magtag (written for the 2025 version MagTag). 

## About the Habit Tracker
This habit tracker is designed to track 5 daily habits that you want to keep track of. You can easily scroll and complete daily habits using the onboard buttons. Different sound and light effects are used for each button action. 

It also uses Wifi to synchronize the date and time so you can track daily streaks for each habit. No Adafruit IO account is needed for this. 

As you complete your daily habits, the MagTag lights a blue light for each completed habit to indicate your progress. When you complete all your daily habits, the blue lights all turn to gold to help boost your feeling of success for the day.

### Required Parts
To build this habit tracker, the following products are needed:

 - [Adafruit MagTag Starter Kit](https://www.adafruit.com/product/4819)

Alternatively, you can purchase parts of the MagTag Starter Kit separately:

 - [Adafruit MagTag - 2.9" Grayscale E-Ink WiFi Display](https://www.adafruit.com/product/4800)
 - [Mini Magnet Feet for RGB LED Matrices (Pack of 4)](https://www.adafruit.com/product/4631)
 - [Adafruit MagTag Enclosure & Buttons Kit](https://www.adafruit.com/product/6433)
 - [Lithium Ion Polymer Battery - 3.7v 500mAh](https://www.adafruit.com/product/1578)
 - [Black Nylon Machine Screw and Stand-off Set – M3 Thread](https://www.adafruit.com/product/4685)


## Installing the Habit Tracker
The habit tracker was written using CircuitPython 10.0.2 and is supported on MagTag 2025 and later. 

> Note: This habit tracker has not been tested on pre-2025 MagTags.

Prior to installing the habit tracker, CircuitPython 10.0.2 must be installed on your MagTag.

### Installing Required Libraries
The following libraries are required for the habit tracker. Copy and paste the folders and files from the latest CircuitPython 10.0.2 installation bundle into the `CIRCUITPY` device's `/lib` folder.

> Note: Several libraries related to Adafruit IO are required in order to use NTP for Wifi syncing, although Adafruit IO is not actually called by the code.

     - adafruit_bitmap_font
     - adafruit_bus_device
     - adafruit_display_shapes
     - adafruit_display_text
     - adafruit_epd
     - adafruit_imageload
     - adafruit_io
     - adafruit_magtag
     - adafruit_minimqtt
     - adafruit_portalbase
     - adafruit_connection_manager.mpy
     - adafruit_fakerequests.mpy
     - adafruit_il0373.mpy
     - adafruit_ntp.mpy
     - adafruit_requests.mpy
     - adafruit_ticks.mpy
     - neopixel.mpy
     - simpleio.mpy

Copy and paste these folders and files from the latest CircuitPython 10.0.2 installation bundle into the `CIRCUITPY` device's `/lib` folder.

### Installing Project Files
To install the habit tracker, download the following project files and save them to the root of your `CIRCUITPY` device:

 - `code.py`
 - `secrets.py`

## Configuring the Habit Tracker
To configure the habit tracker, open `code.py` in a CircuitPython editor, such as [Mu](https://codewith.mu/en/download). 

The habit tracker is configured by editing the values in `code.py`. 

Optionally, `secrets.py` can be configured to enable Wifi syncing of the date and time. See the following section.

### Configuring Wi-Fi Date and Time Sync
To enable Wi-Fi date and time sync, do the following:

 1. In Mu, create a file named `secrets.py`.
 2. Copy and paste the following code into the file:

```javascript
secrets = {
    "ssid": "YourWiFiName",
    "password": "YourWiFiPassword",
}
```

 3. In the `ssid` field, enter your Wi-Fi name.
 4. In the `password` field, enter your Wi-Fi password.

> Note: If this file is not created, Wi-Fi syncing will not be enabled. To advance each day, you must hold down the D button for about 1.5 seconds. 

### Configuring Your Time Zone
The default time zone used by the app is UTC. The numerical representation of your time zone is needed to ensure that the day changes at the correct time. To find your time zone, go to:
https://www.worldwideclock.com/my-time-zone

To configure your time zone:

 1. Find the `TZ_OFFSET_HOURS` setting. 
 2. After the equals sign, add or change the number for your time zone.
 3. If the time zone is west of UTC, add a minus sign before the number.

For example, for the Eastern time zone during July Daylight Savings time, the value would equal `-4`. In Autumn when the time changes again, you would change the value to `-5`.

### Configuring Sound Volume
To change the volume of the sounds played by the habit tracker, do the following:

 1. Find the `SPEAKER_VOLUME` setting.
 2. Change the value to your desired volume. 0.05 is the minimum, and 0.5 is the maximum.

### Configuring Habits
There are five preconfigured habits that you can change. You can also remove or add more habits so there are more or less than five. It is recommended to not add more than 6 habits due to the screen size.
To edit the habits: 
1. Find the `HABITS` setting:
```
HABITS = ["Take Vitamins", "Drink Water", "Read", "Exercise", "Stretch"]
```
2. To edit an existing habit, change the existing value between the quotes.
3. To add a new habit, add an additional habit to the list ensuring you include a comma and quotes. The following example adds a "Take Out Trash" habit to the list:
```
HABITS = ["Take Vitamins", "Drink Water", "Take Out Trash", "Read", "Exercise", "Stretch"]
```
4. To remove a habit, delete the quotes and comma associated with the habit you want to remove. The following example removes the "Read" habit from the list:
 ```
HABITS = ["Take Vitamins", "Drink Water", "Exercise", "Stretch"]
```

## Using the Habit Tracker

### Turning It On

### Syncing the Date and Time

### Completing a Habit

### Uncompleting a Habit

### Advancing to a New Day


> Written with [StackEdit](https://stackedit.io/).
