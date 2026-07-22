# MagTag Habit Tracker
This repository contains a Habit Tracker app for the Adafruit Magtag (written for the 2025 version MagTag). 

## About the Habit Tracker
This habit tracker is designed to track 6 or fewer daily habits that you want to keep track of. You can easily scroll and complete actions using the onboard buttons. The habit tracker uses different sound and light effects for each button action. It also uses Wifi to synchronize the date and time so you can track daily streaks for each habit. No Adafruit IO account is needed for this. 

### Required Parts
To build this habit tracker, the following products are needed:

 - [Adafruit MagTag Starter Kit](https://www.adafruit.com/product/4819)

## Installing the Habit Tracker

### Installing Required Libraries

## Configuring the Habit Tracker

### Configuring Wi-Fi Date and Time Sync

### Configuring Your Time Zone
The default time zone used is UTC. To configure the time zone:

 1. Find the `TZ_OFFSET_HOURS` setting. 
 2. After the equals sign, add or change the number for your time zone. 
If the time zone is west of UTC, add a minus sign before the number.
For example, for the Eastern time zone during July, the value would equal `-4`. 

### Configuring Sound Volume

### Configuring Habits

## Using the Habit Tracker

### Turning It On

### Syncing the Date and Time

### Completing a Habit

### Uncompleting a Habit

### Advancing to a New Day
