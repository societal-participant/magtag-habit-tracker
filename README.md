---


---

<h1 id="magtag-habit-tracker">MagTag Habit Tracker</h1>
<p>This repository contains a Habit Tracker app for the Adafruit Magtag (written for the 2025 version MagTag).</p>
<h2 id="about-the-habit-tracker">About the Habit Tracker</h2>
<p>This habit tracker is designed to track 6 or fewer daily habits that you want to keep track of. You can easily scroll and complete daily habits using the onboard buttons. Different sound and light effects are used for each button action.</p>
<p>It also uses Wifi to synchronize the date and time so you can track daily streaks for each habit. No Adafruit IO account is needed for this.</p>
<p>As you complete your daily habits, the MagTag lights a blue light for each completed habit to indicate your progress. When you complete all your daily habits, the blue lights all turn to gold to help boost your feeling of success for the day.</p>
<h3 id="required-parts">Required Parts</h3>
<p>To build this habit tracker, the following products are needed:</p>
<ul>
<li><a href="https://www.adafruit.com/product/4819">Adafruit MagTag Starter Kit</a></li>
<li><a href="https://www.adafruit.com/product/4685">Black Nylon Machine Screw and Stand-off Set – M3 Thread</a></li>
</ul>
<p>Alternatively, you can purchase parts of the MagTag Starter Kit separately:</p>
<ul>
<li><a href="https://www.adafruit.com/product/4800">Adafruit MagTag - 2.9" Grayscale E-Ink WiFi Display</a></li>
<li><a href="https://www.adafruit.com/product/4631">Mini Magnet Feet for RGB LED Matrices (Pack of 4)</a></li>
<li><a href="https://www.adafruit.com/product/6433">Adafruit MagTag Enclosure &amp; Buttons Kit</a></li>
<li><a href="https://www.adafruit.com/product/1578">Lithium Ion Polymer Battery - 3.7v 500mAh</a></li>
</ul>
<h2 id="installing-the-habit-tracker">Installing the Habit Tracker</h2>
<p>The habit tracker was written using CircuitPython 10.0.2 and is supported on MagTag 2025 and later.</p>
<blockquote>
<p>Note: This habit tracker has not been tested on pre-2025 MagTags.</p>
</blockquote>
<p>Prior to installing the habit tracker, CircuitPython 10.0.2 must be installed on your MagTag.</p>
<h3 id="installing-required-libraries">Installing Required Libraries</h3>
<p>The following libraries are required for the habit tracker. Copy and paste the folders and files from the latest CircuitPython 10.0.2 installation bundle into the <code>CIRCUITPY</code> device’s <code>/lib</code> folder.</p>
<blockquote>
<p>Note: Several libraries related to Adafruit IO are required in order to use NTP for Wifi syncing, although Adafruit IO is not actually called by the code.</p>
</blockquote>
<ul>
<li>adafruit_bitmap_font</li>
<li>adafruit_bus_device</li>
<li>adafruit_display_shapes</li>
<li>adafruit_display_text</li>
<li>adafruit_epd</li>
<li>adafruit_imageload</li>
<li>adafruit_io</li>
<li>adafruit_magtag</li>
<li>adafruit_minimqtt</li>
<li>adafruit_portalbase</li>
<li>adafruit_connection_manager.mpy</li>
<li>adafruit_fakerequests.mpy</li>
<li>adafruit_il0373.mpy</li>
<li>adafruit_ntp.mpy</li>
<li>adafruit_requests.mpy</li>
<li>adafruit_ticks.mpy</li>
<li>neopixel.mpy</li>
<li>simpleio.mpy</li>
</ul>
<p>Copy and paste these folders and files from the latest CircuitPython 10.0.2 installation bundle into the <code>CIRCUITPY</code> device’s <code>/lib</code> folder.</p>
<h3 id="installing-project-files">Installing Project Files</h3>
<h2 id="configuring-the-habit-tracker">Configuring the Habit Tracker</h2>
<h3 id="configuring-wi-fi-date-and-time-sync">Configuring Wi-Fi Date and Time Sync</h3>
<h3 id="configuring-your-time-zone">Configuring Your Time Zone</h3>
<p>The default time zone used is UTC. To configure the time zone:</p>
<ol>
<li>Find the <code>TZ_OFFSET_HOURS</code> setting.</li>
<li>After the equals sign, add or change the number for your time zone.<br>
If the time zone is west of UTC, add a minus sign before the number.<br>
For example, for the Eastern time zone during July, the value would equal <code>-4</code>.</li>
</ol>
<h3 id="configuring-sound-volume">Configuring Sound Volume</h3>
<h3 id="configuring-habits">Configuring Habits</h3>
<h2 id="using-the-habit-tracker">Using the Habit Tracker</h2>
<h3 id="turning-it-on">Turning It On</h3>
<h3 id="syncing-the-date-and-time">Syncing the Date and Time</h3>
<h3 id="completing-a-habit">Completing a Habit</h3>
<h3 id="uncompleting-a-habit">Uncompleting a Habit</h3>
<h3 id="advancing-to-a-new-day">Advancing to a New Day</h3>
<blockquote>
<p>Written with <a href="https://stackedit.io/">StackEdit</a>.</p>
</blockquote>

