---

<h1 id="maggies-magtag-habit-tracker">Maggie’s MagTag Habit Tracker</h1>
<p>This repository contains a Habit Tracker app I created for the Adafruit MagTag (written for the 2025 version MagTag).</p>
<p>See the following topics for information on installing, configuring, and using Maggie’s MagTag Habit Tracker.</p>
<h2 id="about-the-habit-tracker">About the Habit Tracker</h2>
<p>This habit tracker is designed to track 5 daily habits that you want to keep track of. You can easily scroll and complete daily habits using the onboard buttons. Different sound and light effects are used for each button action.</p>
<p>It also uses Wifi to synchronize the date and time so you can track daily streaks for each habit. No Adafruit IO account is needed for this.</p>
<p>As you complete your daily habits, the MagTag lights a blue light for each completed habit to indicate your progress. When you complete all your daily habits, the blue lights all turn to gold to help boost your feeling of success for the day. Each habit also has a daily streak counter for more fun.</p>
<h3 id="required-parts">Required Parts</h3>
<p>To build this habit tracker, the following products are needed:</p>
<ul>
<li><a href="https://www.adafruit.com/product/4819">Adafruit MagTag Starter Kit</a></li>
</ul>
<p>Alternatively, you can purchase parts of the MagTag Starter Kit separately:</p>
<ul>
<li><a href="https://www.adafruit.com/product/4800">Adafruit MagTag - 2.9" Grayscale E-Ink WiFi Display</a></li>
<li><a href="https://www.adafruit.com/product/4631">Mini Magnet Feet for RGB LED Matrices (Pack of 4)</a></li>
<li><a href="https://www.adafruit.com/product/6433">Adafruit MagTag Enclosure &amp; Buttons Kit</a></li>
<li><a href="https://www.adafruit.com/product/1578">Lithium Ion Polymer Battery - 3.7v 500mAh</a></li>
<li><a href="https://www.adafruit.com/product/4685">Black Nylon Machine Screw and Stand-off Set – M3 Thread</a></li>
</ul>
<h2 id="installing-the-habit-tracker">Installing the Habit Tracker</h2>
<p>The habit tracker was written using CircuitPython 10.0.2 and is supported on MagTag 2025 and later.</p>
<blockquote>
<p>Note: This habit tracker has not been tested on pre-2025 MagTags.</p>
</blockquote>
<p>Prior to installing the habit tracker, CircuitPython 10.0.2 must be installed on your MagTag.</p>
<h3 id="installing-required-libraries">Installing Required Libraries</h3>
<p>The following libraries are required for the habit tracker.</p>
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
<p>To install the habit tracker, download the <code>code.py</code> file from the repository and save it to the root of your <code>CIRCUITPY</code> device.</p>
<h2 id="configuring-the-habit-tracker">Configuring the Habit Tracker</h2>
<p>To configure the habit tracker, open <code>code.py</code> in a CircuitPython editor, such as <a href="https://codewith.mu/en/download">Mu</a>.</p>
<p>The habit tracker is configured by editing values in <code>code.py</code>.</p>
<p>Optionally, <code>secrets.py</code> can be configured to enable Wifi syncing of the date and time. See the following section.</p>
<h3 id="configuring-wi-fi-date-and-time-sync">Configuring Wi-Fi Date and Time Sync</h3>
<p>To enable Wi-Fi date and time sync, do the following:</p>
<ol>
<li>In Mu, create a file named <code>secrets.py</code>.</li>
<li>Copy and paste the following code into the file:</li>
</ol>
<pre class=" language-javascript"><code class="prism  language-javascript">secrets <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string">"ssid"</span><span class="token punctuation">:</span> <span class="token string">"YourWiFiName"</span><span class="token punctuation">,</span>
    <span class="token string">"password"</span><span class="token punctuation">:</span> <span class="token string">"YourWiFiPassword"</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>
</code></pre>
<ol start="3">
<li>In the <code>ssid</code> field, enter your Wi-Fi name.</li>
<li>In the <code>password</code> field, enter your Wi-Fi password.</li>
</ol>
<blockquote>
<p>Note: If this file is not created, Wi-Fi syncing will not be enabled. To advance each day, you must hold down the D button for about 1.5 seconds.</p>
</blockquote>
<h3 id="configuring-your-time-zone">Configuring Your Time Zone</h3>
<p>The default time zone used by the app is UTC. The numerical representation of your time zone is needed to ensure that the day changes at the correct time. To find your time zone, go to:<br>
<a href="https://www.worldwideclock.com/my-time-zone">https://www.worldwideclock.com/my-time-zone</a></p>
<p>To configure your time zone:</p>
<ol>
<li>Find the <code>TZ_OFFSET_HOURS</code> setting.</li>
<li>After the equals sign, add or change the number for your time zone.</li>
<li>If the time zone is west of UTC, add a minus sign before the number.</li>
</ol>
<p>For example, for the Eastern time zone during July Daylight Savings time, the value would equal <code>-4</code>. In Autumn when the time changes again, you would change the value to <code>-5</code>.</p>
<h3 id="configuring-sound-volume">Configuring Sound Volume</h3>
<p>To change the volume of the sounds played by the habit tracker, do the following:</p>
<ol>
<li>Find the <code>SPEAKER_VOLUME</code> setting.</li>
<li>Change the value to your desired volume. 0.05 is the minimum, and 0.5 is the maximum.</li>
</ol>
<h3 id="configuring-habits">Configuring Habits</h3>
<p>There are five preconfigured habits that you can change. You can also remove or add more habits so there are more or less than five. It is recommended to not add more than 6 habits due to the screen size.<br>
To edit the habits:</p>
<ol>
<li>Find the <code>HABITS</code> setting:</li>
</ol>
<pre><code>HABITS = ["Take Vitamins", "Drink Water", "Read", "Exercise", "Stretch"]
</code></pre>
<ol start="2">
<li>To edit an existing habit, change the existing value between the quotes.</li>
<li>To add a new habit, add an additional habit to the list ensuring you include a comma and quotes. The following example adds a “Take Out Trash” habit to the list:</li>
</ol>
<pre><code>HABITS = ["Take Vitamins", "Drink Water", "Take Out Trash", "Read", "Exercise", "Stretch"]
</code></pre>
<ol start="4">
<li>To remove a habit, delete the quotes and comma associated with the habit you want to remove. The following example removes the “Read” habit from the list:</li>
</ol>
<pre><code>HABITS = ["Take Vitamins", "Drink Water", "Exercise", "Stretch"]
</code></pre>
<h2 id="using-the-habit-tracker">Using the Habit Tracker</h2>
<p>The following topics explain how to use the habit tracker.</p>
<h3 id="turning-it-on">Turning It On</h3>
<p>To turn on the habit tracker, toggle the <strong>On/Off</strong> switch to <strong>On</strong>.</p>
<h3 id="syncing-the-date-and-time">Syncing the Date and Time</h3>
<p>To sync the date and time, press the <strong>A</strong> button. Syncing is typically only necessary if the date displayed on the habit tracker is incorrect.</p>
<p>If the habit tracker wasn’t configured to use Wi-Fi, then nothing happens.</p>
<h3 id="completing-a-habit">Completing a Habit</h3>
<p>To complete a habit:</p>
<ol>
<li>Use the <strong>B</strong> or <strong>C</strong> buttons to select the habit you want to complete.</li>
<li>Press the <strong>D</strong> button.<br>
Green lights flash and a short sound plays. The checkbox to the left of the habit is filled in and the habit is completed.</li>
</ol>
<h3 id="uncompleting-a-habit">Uncompleting a Habit</h3>
<p>To uncomplete a habit:</p>
<ol>
<li>Use the <strong>B</strong> or <strong>C</strong> buttons to select the habit you want to uncomplete.</li>
<li>Press the <strong>D</strong> button.<br>
Red lights flash and a short sound plays. The habit is no longer marked as completed.</li>
</ol>
<h3 id="advancing-to-a-new-day">Advancing to a New Day</h3>
<p>To advance the day to a new day, press and hold the <strong>D</strong> button.</p>
<p>This is only necessary when the habit tracker isn’t configured to sync with Wi-Fi.</p>
<h3 id="resetting-the-habit-tracker">Resetting the Habit Tracker</h3>
<p>To reset the habit tracker daily streaks back to 0, press and hold all four <strong>A</strong>, <strong>B</strong>, <strong>C</strong>, and <strong>D</strong> buttons for approximately 1.5 seconds. After the screen resets, the daily streaks are cleared.</p>
<blockquote>
<p>Written with <a href="https://stackedit.io/">StackEdit</a>.</p>
</blockquote>

