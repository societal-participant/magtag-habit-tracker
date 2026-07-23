# SPDX-FileCopyrightText: 2026 Maggie Giles
#
# SPDX-License-Identifier: MIT

"""
MagTag Habit Tracker
=====================
Onboard hardware:
  - 4 buttons (A, B, C, D)
  - 4 NeoPixels (feedback flash + daily progress)
  - Piezo speaker (feedback tones)
  - E-ink display (custom drawn UI)
  - Built-in WiFi (ESP32-S2) for optional date sync via NTP

Controls:
  Button A - Manual refresh / re-sync time
  Button B - Move cursor up
  Button C - Move cursor down
  Button D - short press: Toggle selected habit done/not-done for today
             long press (~1.5s): manually advance to a new day
                                  (a fallback if you don't set up WiFi)
  All 4 buttons together, held ~1.5s - wipe all streaks/completion state
                                        back to zero (factory reset)

Persistence: streaks and today's completion state are stored in
microcontroller.nvm, so they survive power loss and reboots.

Required libraries (from the Adafruit CircuitPython version 10
Library Bundle), copied into /lib:
  adafruit_bitmap_font, adafruit_bus_device, adafruit_display_shapes,
  adafruit_display_text, adafruit_epd, adafruit_imageload, adafruit_io,
  adafruit_magtag, adafruit_minimqtt, adafruit_portalbase, adafruit_connection_manager.mpy,
  adafruit_fakerequests.mpy, adafruit_il0373.mpy, adafruit_ntp.mpy, adafruit_requests.mpy,
  adafruit_ticks.mpy, neopixel.mpy, simpleio.mpy


Note: date/time sync uses direct NTP (adafruit_ntp), not Adafruit IO, so no
Adafruit IO account or aio_username/aio_key is needed. The adafruit_io/
adafruit_minimqtt/adafruit_portalbase libraries above are still required
only because MagTag() imports them internally, even though this code
never calls into that part of the library.

Optional: create secrets.py on CIRCUITPY with your WiFi credentials to
enable automatic date-based streak resets:
    secrets = {
        "ssid": "YourWiFiName",
        "password": "YourWiFiPassword",
    }
If secrets.py is missing, the tracker still works fully — just use the
Button D long-press to advance days manually.
"""

import time
import math
import microcontroller
import displayio
import terminalio
import board
import pwmio
import wifi
import socketpool
import rtc
import adafruit_ntp
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_magtag.magtag import MagTag

# NTP returns UTC; there's no timezone database on the board, so the local
# offset is just a fixed number of hours you flip by hand for DST.
# Eastern time: -4 during EDT (roughly Mar-Nov), -5 during EST.
TZ_OFFSET_HOURS = 0

# magtag.peripherals.play_tone() always uses a 50% PWM duty cycle internally
# (hardcoded in the simpleio.tone() helper it calls) - that's max volume with
# no way to turn it down. Driving board.SPEAKER ourselves with a lower duty
# cycle gets a real volume knob. 0.5 = old max volume; try 0.05-0.2 for quiet.
SPEAKER_VOLUME = 0.05

# ---------- Configuration ----------
HABITS = ["Take Vitamins", "Drink Water", "Read", "Exercise", "Stretch"]

BLACK = 0x000000
WHITE = 0xFFFFFF
RED = 0xFF0000  # only visible on tri-color MagTag displays; harmless otherwise

DISPLAY_W = 296
DISPLAY_H = 128
HEADER_H = 20
FOOTER_H = 12
ROW_AREA_H = DISPLAY_H - HEADER_H - FOOTER_H
ROW_H = ROW_AREA_H // len(HABITS)

DISPLAY_MIN_INTERVAL = 8  # seconds between e-ink refreshes
IDLE_TIMEOUT_SECONDS = 60  # hide the selection bar after this long with no button press

# ---------- NVM layout ----------
# bytes 0-1          -> day marker (day-of-year, or manual counter), 2 bytes
#                       wide so it can hold up to 65535 with no collisions
#                       (day-of-year alone only needs up to 366, but this
#                       leaves headroom and avoids ever needing to change
#                       this again)
# byte 2 + 2*i       -> streak count for habit i (0-255)
# byte 3 + 2*i       -> done-today flag for habit i (0/1)
nvm = microcontroller.nvm
NVM_SIZE_NEEDED = 2 + 2 * len(HABITS)


def load_state():
    raw = nvm[0:NVM_SIZE_NEEDED]
    day_marker = (raw[0] << 8) | raw[1]
    streaks = []
    done_today = []
    for i in range(len(HABITS)):
        streaks.append(raw[2 + 2 * i])
        done_today.append(bool(raw[3 + 2 * i]))
    return day_marker, streaks, done_today


def save_state(day_marker, streaks, done_today):
    buf = bytearray(NVM_SIZE_NEEDED)
    buf[0] = (day_marker >> 8) & 0xFF
    buf[1] = day_marker & 0xFF
    for i in range(len(HABITS)):
        buf[2 + 2 * i] = min(streaks[i], 255)
        buf[3 + 2 * i] = 1 if done_today[i] else 0
    nvm[0:NVM_SIZE_NEEDED] = buf


day_marker, streaks, done_today = load_state()

# ---------- Setup ----------
magtag = MagTag()
magtag.peripherals.neopixel_disable = False
magtag.peripherals.speaker_disable = True  # beep() enables/disables this per-tone now
magtag.peripherals.neopixels.brightness = 0.2

time_synced = False


def try_sync_time():
    """Attempt WiFi + direct NTP sync (no Adafruit IO account needed).
    Safe to call even with no secrets.py."""
    global time_synced
    try:
        import secrets  # noqa: F401  (presence implies WiFi is configured)
    except ImportError:
        return False
    try:
        if not wifi.radio.connected:
            wifi.radio.connect(secrets.secrets["ssid"], secrets.secrets["password"])
        pool = socketpool.SocketPool(wifi.radio)
        ntp = adafruit_ntp.NTP(pool, tz_offset=TZ_OFFSET_HOURS)
        rtc.RTC().datetime = ntp.datetime
        time_synced = True
        return True
    except Exception as e:  # broad on purpose: many failure modes here
        print("Time sync failed:", e)
        return False


def current_day_marker():
    """Day-of-year if we have real time, else the stored manual marker."""
    if time_synced:
        return time.localtime().tm_yday
    return day_marker


try_sync_time()

# ---------- Handle day rollover ----------
new_marker = current_day_marker()
if new_marker != day_marker:
    for i in range(len(HABITS)):
        if not done_today[i]:
            streaks[i] = 0  # missed day breaks the streak
        done_today[i] = False
    day_marker = new_marker
    save_state(day_marker, streaks, done_today)

# ---------- Build the display UI ----------
main_group = displayio.Group()

# Full-screen white background (without this, undrawn pixels render black
# on the e-ink display, which also hides any black text drawn on top of it)
# NOTE: stroke=0 avoids a real quirk in adafruit_display_shapes.Rect: if you
# don't pass stroke=0 or an explicit outline, the 1px border is still drawn
# using the palette's default (opaque black) color even though outline=None.
background_rect = Rect(0, 0, DISPLAY_W, DISPLAY_H, fill=WHITE, stroke=0)
main_group.append(background_rect)

# Header bar (inverted: black fill, white text)
header_rect = Rect(0, 0, DISPLAY_W, HEADER_H, fill=BLACK, stroke=0)
main_group.append(header_rect)

header_label = label.Label(
    terminalio.FONT,
    text="HABIT TRACKER",
    color=WHITE,
    scale=1,
    anchor_point=(0, 0.5),
    anchored_position=(6, HEADER_H // 2),
)
main_group.append(header_label)

date_label = label.Label(
    terminalio.FONT,
    text="",
    color=WHITE,
    scale=1,
    anchor_point=(1, 0.5),
    anchored_position=(DISPLAY_W - 6, HEADER_H // 2),
)
main_group.append(date_label)

# Habit rows
checkbox_size = 12
checkbox_rects = []
name_labels = []
streak_labels = []
selection_rects = []

for i, habit_name in enumerate(HABITS):
    row_top = HEADER_H + i * ROW_H
    row_center = row_top + ROW_H // 2

    # stroke=0: this rect is fill-only (the selection highlight is a solid
    # black bar behind white text, same trick as the header), so it needs
    # no border at all. See note above about Rect's outline=None quirk.
    sel_rect = Rect(0, row_top, DISPLAY_W, ROW_H, fill=None, stroke=0)
    main_group.append(sel_rect)
    selection_rects.append(sel_rect)

    cb = Rect(
        10,
        row_center - checkbox_size // 2,
        checkbox_size,
        checkbox_size,
        outline=BLACK,
        fill=WHITE,
        stroke=2,
    )
    main_group.append(cb)
    checkbox_rects.append(cb)

    name_lbl = label.Label(
        terminalio.FONT,
        text=habit_name,
        color=BLACK,
        scale=1,
        anchor_point=(0, 0.5),
        anchored_position=(30, row_center),
    )
    main_group.append(name_lbl)
    name_labels.append(name_lbl)

    streak_lbl = label.Label(
        terminalio.FONT,
        text="0d",
        color=BLACK,
        scale=1,
        anchor_point=(1, 0.5),
        anchored_position=(DISPLAY_W - 10, row_center),
    )
    main_group.append(streak_lbl)
    streak_labels.append(streak_lbl)

# Footer
footer_label = label.Label(
    terminalio.FONT,
    text="A: Sync  B/C:Move  D:Toggle (hold D = New Day)",
    color=BLACK,
    scale=1,
    anchor_point=(0, 0.5),
    anchored_position=(6, DISPLAY_H - FOOTER_H // 2),
)
main_group.append(footer_label)

magtag.display.root_group = main_group

# ---------- State ----------
cursor = 0
last_display_update = 0


def beep(freq, duration=0.08, volume=SPEAKER_VOLUME):
    pwm = None
    try:
        magtag.peripherals.speaker_disable = False  # enable the amp/speaker pin
        pwm = pwmio.PWMOut(board.SPEAKER, frequency=int(freq), variable_frequency=False)
        pwm.duty_cycle = int(max(0.0, min(0.5, volume)) * 65535)
        time.sleep(duration)
    except Exception:
        pass
    finally:
        # Always release the PWM pin and power down the amp, even if
        # something above raised - otherwise a failed tone can leave the
        # speaker stuck outputting (a constant buzz) with no way to stop it.
        if pwm is not None:
            try:
                pwm.duty_cycle = 0
                pwm.deinit()
            except Exception:
                pass
        magtag.peripherals.speaker_disable = True


def flash_pixels(color, times=1):
    pixels = magtag.peripherals.neopixels
    for _ in range(times):
        for i in range(NUM_PIXELS):
            pixels[i] = color
        pixels.show()
        time.sleep(0.08)
        for i in range(NUM_PIXELS):
            pixels[i] = (0, 0, 0)
        pixels.show()
        time.sleep(0.06)


BLUE = (0, 60, 120)
GOLD = (160, 110, 0)
NUM_PIXELS = 4  # MagTag has exactly 4 onboard NeoPixels - a hardware fact,
                # unrelated to how many habits are configured


def show_daily_progress():
    """Lights NeoPixels in proportion to the fraction of today's habits
    completed so far - scales correctly whether HABITS has 3 entries or 30.
    Completing every habit turns all pixels gold."""
    pixels = magtag.peripherals.neopixels
    total = len(HABITS)
    done_count = sum(done_today)

    if total == 0:
        for i in range(NUM_PIXELS):
            pixels[i] = (0, 0, 0)
        pixels.show()
        return

    if done_count >= total:
        for i in range(NUM_PIXELS):
            pixels[i] = GOLD
    else:
        # Proportional fill, rounded up: e.g. with 8 habits and 3 done,
        # that's 3/8 of the way there -> ceil(3/8 * 4) = 2 pixels lit.
        # Using ceil (instead of round) guarantees the very first
        # completed habit always lights at least one pixel, regardless
        # of how many total habits there are.
        fraction_done = done_count / total
        lit = min(NUM_PIXELS, math.ceil(fraction_done * NUM_PIXELS))
        for i in range(NUM_PIXELS):
            pixels[i] = BLUE if i < lit else (0, 0, 0)

    pixels.show()


def refresh_ui(force=False):
    global last_display_update
    now = time.monotonic()

    if time_synced:
        t = time.localtime()
        date_label.text = "{:04d}-{:02d}-{:02d}".format(t.tm_year, t.tm_mon, t.tm_mday)
    else:
        date_label.text = "offline"

    for i in range(len(HABITS)):
        selected = (i == cursor) and not selection_hidden
        streak_labels[i].text = "{}d".format(streaks[i])

        # Selected row: solid black bar behind white text (same visual
        # language as the header). Unselected row: plain white background,
        # black text. This reads clearly on both grayscale and tri-color
        # MagTag panels, unlike a colored outline.
        selection_rects[i].fill = BLACK if selected else None
        text_color = WHITE if selected else BLACK
        name_labels[i].color = text_color
        streak_labels[i].color = text_color

        if done_today[i]:
            # checked box: solid fill, always contrasts with its background
            checkbox_rects[i].fill = WHITE if selected else BLACK
            checkbox_rects[i].outline = WHITE if selected else BLACK
        else:
            # empty box: just an outline, transparent center so the row's
            # own background (black if selected, white otherwise) shows through
            checkbox_rects[i].fill = None
            checkbox_rects[i].outline = WHITE if selected else BLACK

    if not force and (now - last_display_update) < DISPLAY_MIN_INTERVAL:
        return
    try:
        magtag.display.refresh()
        last_display_update = now
    except RuntimeError:
        pass  # refreshed too recently, try again next loop


last_activity = time.monotonic()
selection_hidden = False

refresh_ui(force=True)
show_daily_progress()

# ---------- Main loop ----------
last_button_check = 0
d_press_start = None
d_long_fired = False

RESET_HOLD_SECONDS = 1.5  # hold all 4 buttons together this long to wipe streaks
reset_combo_start = None
reset_fired = False


def mark_activity():
    """Call whenever a button press is detected. Resets the idle clock, and
    if the selection bar was hidden from a prior idle timeout, restores it
    with an immediate refresh."""
    global last_activity, selection_hidden
    last_activity = time.monotonic()
    if selection_hidden:
        selection_hidden = False
        refresh_ui(force=True)


def factory_reset():
    """Wipe all streaks/completion state back to a fresh start."""
    global day_marker, streaks, done_today
    day_marker = 0
    streaks = [0] * len(HABITS)
    done_today = [False] * len(HABITS)
    save_state(day_marker, streaks, done_today)
    beep(200, 0.15)
    beep(150, 0.2)
    flash_pixels((200, 0, 0), times=3)
    refresh_ui(force=True)
    show_daily_progress()


while True:
    now = time.monotonic()

    if now - last_button_check > 0.05:
        last_button_check = now
        buttons = magtag.peripherals.buttons  # pressed == False (pull-up)

        if not (buttons[0].value and buttons[1].value and buttons[2].value and buttons[3].value):
            mark_activity()

        all_pressed = (
            not buttons[0].value
            and not buttons[1].value
            and not buttons[2].value
            and not buttons[3].value
        )

        if all_pressed:
            # Hold all 4 buttons together for RESET_HOLD_SECONDS to wipe
            # streaks/completion state back to zero. Takes priority over
            # the individual button actions below while held.
            if reset_combo_start is None:
                reset_combo_start = now
                reset_fired = False
            elif not reset_fired and (now - reset_combo_start) >= RESET_HOLD_SECONDS:
                reset_fired = True
                factory_reset()
        else:
            reset_combo_start = None
            reset_fired = False

            # Button A - manual refresh / re-sync time
            if not buttons[0].value:
                if try_sync_time():
                    beep(1000, 0.1)
                else:
                    beep(300, 0.1)
                refresh_ui(force=True)
                time.sleep(0.2)

            # Button B - cursor up
            elif not buttons[1].value:
                cursor = (cursor - 1) % len(HABITS)
                beep(500, 0.04)
                refresh_ui(force=True)
                time.sleep(0.15)

            # Button C - cursor down
            elif not buttons[2].value:
                cursor = (cursor + 1) % len(HABITS)
                beep(500, 0.04)
                refresh_ui(force=True)
                time.sleep(0.15)

            # Button D - short press: toggle done. long press: manual new day.
            if not buttons[3].value:
                if d_press_start is None:
                    d_press_start = now
                    d_long_fired = False
                elif not d_long_fired and (now - d_press_start) > 1.5:
                    # Long press: force a new day manually
                    d_long_fired = True
                    day_marker = (day_marker + 1) % 65536
                    for i in range(len(HABITS)):
                        if not done_today[i]:
                            streaks[i] = 0
                        done_today[i] = False
                    save_state(day_marker, streaks, done_today)
                    beep(300, 0.15)
                    beep(600, 0.15)
                    refresh_ui(force=True)
                    show_daily_progress()
            else:
                if d_press_start is not None and not d_long_fired:
                    # Short press released before long-press threshold: toggle done
                    if done_today[cursor]:
                        done_today[cursor] = False
                        streaks[cursor] = max(0, streaks[cursor] - 1)
                        beep(400, 0.1)
                        flash_pixels((150, 30, 0), times=1)
                    else:
                        done_today[cursor] = True
                        streaks[cursor] += 1
                        beep(900, 0.06)
                        beep(1300, 0.08)
                        flash_pixels((0, 150, 30), times=1)
                    save_state(day_marker, streaks, done_today)
                    refresh_ui(force=True)
                    show_daily_progress()
                d_press_start = None
                d_long_fired = False

        if not selection_hidden and (now - last_activity) > IDLE_TIMEOUT_SECONDS:
            selection_hidden = True
            refresh_ui(force=True)

    time.sleep(0.02)
