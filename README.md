# Maggie’s MagTag Habit Tracker

This repository contains a Habit Tracker app I created for the Adafruit MagTag (written for the 2025 version MagTag).

See the following topics for information on installing, configuring, and using Maggie’s MagTag Habit Tracker.

## About the Habit Tracker

This habit tracker is designed to track 5 daily habits that you want to keep track of. You can easily scroll and complete daily habits using the onboard buttons. Different sound and light effects are used for each button action.

It also uses Wi-Fi to synchronize the date and time to track daily streaks for each habit. No Adafruit IO account is needed.

As you complete your daily habits, the MagTag lights a blue light for each completed habit to indicate your progress. When you complete all of your daily habits, the blue lights all turn to gold to help boost your feeling of success for the day. Each habit also has a daily streak counter for even more fun.

### Required Parts

To build this habit tracker, the following products are needed:

-   [Adafruit MagTag Starter Kit](https://www.adafruit.com/product/4819)

Alternatively, you can purchase parts of the MagTag Starter Kit separately:

-   [Adafruit MagTag - 2.9" Grayscale E-Ink WiFi Display](https://www.adafruit.com/product/4800)
-   [Mini Magnet Feet for RGB LED Matrices (Pack of 4)](https://www.adafruit.com/product/4631)
-   [Adafruit MagTag Enclosure & Buttons Kit](https://www.adafruit.com/product/6433)
-   [Lithium Ion Polymer Battery - 3.7v 500mAh](https://www.adafruit.com/product/1578)
-   [Black Nylon Machine Screw and Stand-off Set – M3 Thread](https://www.adafruit.com/product/4685)

## Installing the Habit Tracker Files

The habit tracker was written using CircuitPython 10.0.2 and is supported on MagTag 2025 and later.

> Note: This habit tracker has not been tested on pre-2025 MagTags.

Prior to installing the habit tracker, CircuitPython 10.0.2 must be installed on your MagTag. See [Adafruit's page on installing CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) for information.

### Installing Required Libraries

The following libraries are required for the habit tracker.

> Note: Several libraries related to Adafruit IO are required in order to use NTP for Wi-Fi syncing, although Adafruit IO is not actually called by the code.

-   adafruit\_bitmap\_font
-   adafruit\_bus\_device
-   adafruit\_display\_shapes
-   adafruit\_display\_text
-   adafruit\_epd
-   adafruit\_imageload
-   adafruit\_io
-   adafruit\_magtag
-   adafruit\_minimqtt
-   adafruit\_portalbase
-   adafruit\_connection\_manager.mpy
-   adafruit\_fakerequests.mpy
-   adafruit\_il0373.mpy
-   adafruit\_ntp.mpy
-   adafruit\_requests.mpy
-   adafruit\_ticks.mpy
-   neopixel.mpy
-   simpleio.mpy

Copy and paste these folders and files from the latest CircuitPython 10.0.2 installation bundle into the `CIRCUITPY` device’s `/lib` folder.

### Installing Project Files

To install the habit tracker, download the `code.py` file from the repository and save it to the root of your `CIRCUITPY` device.

## Configuring the Habit Tracker

To configure the habit tracker, open `code.py` in a CircuitPython editor, such as [Mu](https://codewith.mu/en/download).

The habit tracker is configured by editing values in `code.py`.

Optionally, `secrets.py` can be created and configured to enable Wi-Fi syncing of the date and time. See the following section.

### Configuring Wi-Fi Date and Time Sync

To enable Wi-Fi date and time sync, do the following:

1.  In Mu, create a file named `secrets.py`.
2.  Copy and paste the following code into the file:

```javascript
secrets = {
    "ssid": "YourWiFiName",
    "password": "YourWiFiPassword",
    "timezone": "",
}
```

3.  In the `ssid` field, enter your Wi-Fi name.
4.  In the `password` field, enter your Wi-Fi password.
5. Optionally, in the `timezone` field, enter the value for your time zone. If no value is entered, the default UTC is used.
Time zone values can be found on [this page](https://timeapi.io/documentation/iana-timezones). Copy and paste the **IANA Time Zone** value for your time zone. For example, `America/New_York`. 

> Note: If this file is not created, Wi-Fi syncing will not be enabled. To advance each day, you must hold down the D button for about 1.5 seconds.

### Configuring Your Time Zone

The default time zone used by the app is UTC. The numerical representation of your time zone is needed to ensure that the day changes at the correct time. To find your time zone, go to:  
[https://www.worldwideclock.com/my-time-zone](https://www.worldwideclock.com/my-time-zone)

To configure your time zone:

1.  Find the `TZ_OFFSET_HOURS` setting.
2.  After the equals sign, add or change the number for your time zone.
3.  If the time zone is west of UTC, add a minus sign before the number.

For example, for the Eastern time zone during July Daylight Savings time, the value would equal `-4`. In Autumn when the time changes again, you would change the value to `-5`.

### Configuring Sound Volume

To change the volume of the sounds played by the habit tracker, do the following:

1.  Find the `SPEAKER_VOLUME` setting.
2.  Change the value to your desired volume. 0.05 is the minimum, and 0.5 is the maximum.

### Configuring Habits

There are five preconfigured habits that you can change. You can also remove or add more habits so there are more or less than five. It is recommended to not add more than 6 habits due to the screen size.  
To edit the habits:

1.  Find the `HABITS` setting:

```
HABITS = ["Take Vitamins", "Drink Water", "Read", "Exercise", "Stretch"]
```

2.  To edit an existing habit, change the existing value between the quotes.
3.  To add a new habit, add an additional habit to the list ensuring you include a comma and quotes. The following example adds a “Take Out Trash” habit to the list:

```
HABITS = ["Take Vitamins", "Drink Water", "Take Out Trash", "Read", "Exercise", "Stretch"]
```

4.  To remove a habit, delete the quotes and comma associated with the habit you want to remove. The following example removes the “Read” habit from the list:

```
HABITS = ["Take Vitamins", "Drink Water", "Exercise", "Stretch"]
```

## Using the Habit Tracker

The following topics explain how to use the habit tracker.

### Turning It On

To turn on the habit tracker, toggle the **On/Off** switch to **On**.

### Syncing the Date and Time

To sync the date and time, press the **A** button. Syncing is typically only necessary if the date displayed on the habit tracker is incorrect.

If the habit tracker wasn’t configured to use Wi-Fi, then nothing happens.

### Completing a Habit

To complete a habit:

1.  Use the **B** or **C** buttons to select the habit you want to complete.
2.  Press the **D** button.  
    Green lights flash and a short sound plays. The checkbox to the left of the habit is filled in and the habit is completed.

### Uncompleting a Habit

To uncomplete a habit:

1.  Use the **B** or **C** buttons to select the habit you want to uncomplete.
2.  Press the **D** button.  
    Red lights flash and a short sound plays. The habit is no longer marked as completed.

### Advancing to a New Day

To advance the day to a new day, press and hold the **D** button.

This is only necessary when the habit tracker isn’t configured to sync with Wi-Fi.

### Resetting the Habit Tracker

To reset the habit tracker daily streaks back to 0, press and hold all four **A**, **B**, **C**, and **D** buttons for approximately 1.5 seconds. After the screen resets, the daily streaks are cleared.

> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbMjEyMTg1NTA5MywtMTc4Njg0MjE0MywtMT
c2MDAyNDQxMl19
-->