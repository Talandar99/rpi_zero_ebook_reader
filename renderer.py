#!/usr/bin/python3
import sys
import os
import time
import logging
import subprocess
from PIL import Image

logging.basicConfig(level=logging.INFO)
libdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
try:
    from waveshare_epd import epd7in5_V2
except:
    pass

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, 'screen.bmp')
TEMP_PATH = '/tmp/screen_raw.bmp'
CHECK_INTERVAL = 1
HIST_DIFF_THRESHOLD = 20


def ensure_xorg_and_i3():
    try:
        result = subprocess.run(['pgrep', '-x', 'Xorg'],
                                stdout=subprocess.DEVNULL)
        if result.returncode != 0:
            logging.info(
                "Xorg is not running. Starting fake display session...")
            subprocess.run(['sudo', 'killall', 'Xorg'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.Popen([
                'sudo', 'Xorg', ':0', '-config', '/etc/X11/xorg.conf.d/10-dummy.conf',
                '-novtswitch', '-nolisten', 'tcp'
            ])
            time.sleep(3)
            env = os.environ.copy()
            env["DISPLAY"] = ":0"
            env["HOME"] = "/home/user"
            subprocess.Popen(['i3'], env=env)

            time.sleep(3)
            subprocess.Popen(['zathura', '/home/user/book.pdf'], env=env)
        else:
            logging.info("Xorg is already running.")
    except Exception as e:
        logging.error(f"Failed to start or check Xorg: {e}")


def capture_and_prepare_screenshot():
    try:
        subprocess.run(['import', '-display', ':0', '-window',
                       'root', TEMP_PATH], check=True)
        subprocess.run(['convert', TEMP_PATH, '-rotate',
                       '180', IMAGE_PATH], check=True)
        os.remove(TEMP_PATH)
        logging.info("Screenshot captured and rotated to screen.bmp")
    except subprocess.CalledProcessError as e:
        logging.error(f"Screenshot capture failed: {e}")


def hist_diff(im1, im2):
    h1 = im1.histogram()
    h2 = im2.histogram()
    return sum(abs(a - b) for a, b in zip(h1, h2))


def main():
    ensure_xorg_and_i3()

    subprocess.run(['sudo', 'rm', '-f', '/tmp/screen_raw.bmp'])
    epd = epd7in5_V2.EPD()
    logging.info("Initializing e-Paper")
    epd.init()
    epd.Clear()
    time.sleep(1)

    last_image = None
    epd.init_fast()

    while True:
        capture_and_prepare_screenshot()

        try:
            current_image = Image.open(IMAGE_PATH).convert('L').convert('1')
        except Exception as e:
            logging.error(f"Failed to open : {e}")
            time.sleep(CHECK_INTERVAL)
            continue

        if last_image is None:
            epd.display_Partial(epd.getbuffer(current_image),
                                0, 0, epd.width, epd.height)
            last_image = current_image
            logging.info("Initial display")
        else:
            difference = hist_diff(current_image, last_image)
            logging.info(f"Histogram difference: {difference}")
            if difference > HIST_DIFF_THRESHOLD:
                epd.display_Partial(epd.getbuffer(
                    current_image), 0, 0, epd.width, epd.height)
                last_image = current_image
                logging.info("Partial update applied")
            else:
                logging.debug("No significant change detected")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Interrupted. Clearing annd sleeping e-Paper")
        epd = epd7in5_V2.EPD()
        epd.init()
        epd.Clear()
        epd.sleep()
        sys.exit()
