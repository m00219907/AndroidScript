import cv2
import numpy as np
import shutil
import os.path
import time
import re
import imutils
from auto_adb import auto_adb

adb = auto_adb()

pic_count = 1


def _get_screen_height():
    size_str = adb.get_screen()
    m = re.search(r'(\d+)x(\d+)', size_str)
    if m:
        return int(m.group(2))
    return 1920


def take_screenshot(pic_count):
    adb.run('shell screencap -p /sdcard/autojump.png')
    cmd = 'pull /sdcard/autojump.png ./pic/{x1}.png'.format(x1=pic_count)
    adb.run(cmd)


def pull_screenshot():
    adb.run('shell screencap -p /sdcard/autojump.png')
    adb.run('pull /sdcard/autojump.png .')
    return cv2.imread('./autojump.png')


def find_position(template, appicon):
    (height, width) = template.shape[:2]
    # open the main image and convert it to gray scale image
    main_image = pull_screenshot()
    gray_image = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    temp_found = None
    cur_scale = 0
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        # resize the image and store the ratio
        resized_img = imutils.resize(gray_image, width=int(gray_image.shape[1] * scale))
        ratio = gray_image.shape[1] / float(resized_img.shape[1])
        if resized_img.shape[0] < height or resized_img.shape[1] < width:
            break
        # Convert to edged image for checking
        e = cv2.Canny(resized_img, 10, 25)
        match = cv2.matchTemplate(e, template, cv2.TM_CCOEFF)
        (_, val_max, _, loc_max) = cv2.minMaxLoc(match)
        if temp_found is None or val_max > temp_found[0]:
            temp_found = (val_max, loc_max, ratio)
            cur_scale = scale
    # Get information from temp_found to compute x,y coordinate
    (_, loc_max, r) = temp_found
    (x_start, y_start) = (int(loc_max[0]), int(loc_max[1]))
    (x_end, y_end) = (int((loc_max[0] + width)), int((loc_max[1] + height)))
    x_start_origin = int(x_start / cur_scale)
    y_start_origin = int(y_start / cur_scale)
    get_color_y_start = y_start_origin + 42
    if (appicon == qrscan):
        get_color_y_start = y_start_origin + 3
    color = main_image[get_color_y_start, x_start_origin + 3]
    print(color)
    sum = 10000
    if (appicon == qrscan):
        sum = (color[2] - 32) * (color[2] - 32) + (color[1] - 131) * (color[1] - 131) + (color[0] - 255) * (
                    color[0] - 255)
    elif (appicon == fatburning):
        sum = (color[2] - 255) * (color[2] - 255) + (color[1] - 180) * (color[1] - 180) + (color[0] - 41) * (
                    color[0] - 41)
    elif (appicon == workout30day):
        sum = (color[2] - 254) * (color[2] - 254) + (color[1] - 171) * (color[1] - 171) + (color[0] - 44) * (
                    color[0] - 44)
    elif (appicon == menloseweight):
        sum = 0
        #sum = (color[2] - 251) * (color[2] - 251) + (color[1] - 24) * (color[1] - 33) + (color[0] - 38) * (
                    #color[0] - 38)
    elif (appicon == hddownloader):
        sum = (color[2] - 254) * (color[2] - 254) + (color[1] - 172) * (color[1] - 172) + (color[0] - 5) * (
                    color[0] - 5)
    elif (appicon == statussaver):
        sum = (color[2] - 0) * (color[2] - 0) + (color[1] - 134) * (color[1] - 134) + (color[0] - 120) * (
                    color[0] - 120)
    elif (appicon == increaseheight):
        sum = (color[2] - 237) * (color[2] - 237) + (color[1] - 29) * (color[1] - 29) + (color[0] - 34) * (
                    color[0] - 34)
    print(sum)
    if (sum < 600):
        return x_start_origin, y_start_origin
    else:
        print('not found...')
        return -1, -1


cur_dir = os.path.dirname(os.path.realpath(__file__))
folder = os.path.exists(os.path.join(cur_dir, 'pic'))
if folder:
    shutil.rmtree(os.path.join(cur_dir, 'pic'))
    time.sleep(3)
os.makedirs('pic')

qrscan_screenshot = False
fatburning_screenshot = False
workout30day_screenshot = False
menloseweight_screenshot = False
hddownloader_screenshot = False
statussaver_screenshot = False
increaseheight_screenshot = False


def lixing_with_keyword(appicon, keyword):
    adb.run('shell monkey -p com.android.vending 1')
    time.sleep(5)
    adb.run('shell input tap 360 120')
    time.sleep(1)
    cmd = 'shell input text {y1}'.format(y1=keyword)
    adb.run(cmd)
    adb.run('shell input keyevent 66')  # 66 -->  "KEYCODE_ENTER"
    time.sleep(5)

    global pic_count
    global qrscan_screenshot
    global fatburning_screenshot
    global workout30day_screenshot
    global menloseweight_screenshot
    global hddownloader_screenshot
    global statussaver_screenshot
    global increaseheight_screenshot

    template = cv2.imread(appicon)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 10, 25)
    try_count = 0
    while (True):
        xpos, ypos = find_position(template, appicon)
        if (xpos == -1):
            height = _get_screen_height()
            scroll_herght = (int)(height / 3 * 2)
            cmd = 'shell input swipe 500 {y1} 500 300'.format(y1=scroll_herght)
            adb.run(cmd)
            time.sleep(1)
            try_count = try_count + 1
            if (try_count > 25):
                break
        else:
            take_screenshot(pic_count)
            pic_count = pic_count + 1
            cmd = 'shell input tap {x1} {y1}'.format(x1=xpos, y1=ypos)
            print(cmd)
            adb.run(cmd)
            time.sleep(3)
            if (appicon == qrscan and qrscan_screenshot == False):
                qrscan_screenshot = True
                take_screenshot(pic_count)
                pic_count = pic_count + 1
            if (appicon == fatburning and fatburning_screenshot == False):
                fatburning_screenshot = True
                take_screenshot(pic_count)
                pic_count = pic_count + 1
            if (appicon == workout30day and workout30day_screenshot == False):
                workout30day_screenshot = True
                take_screenshot(pic_count)
                pic_count = pic_count + 1
            if (appicon == menloseweight and menloseweight_screenshot == False):
                menloseweight_screenshot = True
                take_screenshot(pic_count)
                pic_count = pic_count + 1
            if (appicon == hddownloader and hddownloader_screenshot == False):
                hddownloader_screenshot = True
                take_screenshot(pic_count)
                pic_count = pic_count + 1
            if (appicon == statussaver and statussaver_screenshot == False):
                statussaver_screenshot = True
                take_screenshot(pic_count)
                pic_count = pic_count + 1
            if (appicon == increaseheight and increaseheight_screenshot == False):
                increaseheight_screenshot = True
                take_screenshot(pic_count)
                pic_count = pic_count + 1
            break
    adb.run('shell input keyevent 4')  # 4 -->  "KEYCODE_BACK"
    adb.run('shell input keyevent 4')  # 4 -->  "KEYCODE_BACK"
    adb.run('shell input keyevent 4')  # 4 -->  "KEYCODE_BACK"
    adb.run('shell input keyevent 4')  # 4 -->  "KEYCODE_BACK"
    adb.run('shell input keyevent 4')  # 4 -->  "KEYCODE_BACK"


qrscan = 'qrscan.png'
fatburning = 'fatburning.png'
workout30day = 'workout30day.png'
menloseweight = 'menloseweight.png'
hddownloader = 'hddownloader.png'
statussaver = 'statussaver.png'
increaseheight = 'increaseheight.png'


lixing_with_keyword(qrscan, 'free%sqr%sscanner')
lixing_with_keyword(qrscan, 'free%sqr%scode%sreader')
lixing_with_keyword(qrscan, 'qr%sscanner')
lixing_with_keyword(qrscan, 'qr%scode%sreader')
lixing_with_keyword(qrscan, 'qr%scode%sscanner')
lixing_with_keyword(qrscan, 'barcode%sscanner')
lixing_with_keyword(qrscan, 'barcode%sscanner%sapp%sfree')

lixing_with_keyword(fatburning, 'fat%sburning')

lixing_with_keyword(workout30day, 'abs%sworkout%s30%sday')
lixing_with_keyword(workout30day, 'abs%sworkout')

lixing_with_keyword(menloseweight, 'lose%sweight%sapp')

lixing_with_keyword(hddownloader, 'hd%svideo%sdownloader%sapp%s2019')

lixing_with_keyword(statussaver, 'Status%sDownloader%s-%sStatus%sSaver%sfor%sWhatsapp')

lixing_with_keyword(increaseheight, 'increase%sheight%sworkout')
lixing_with_keyword(increaseheight, 'increase%sheight')
lixing_with_keyword(increaseheight, 'height%sincrease')
lixing_with_keyword(increaseheight, 'grow%staller')
lixing_with_keyword(increaseheight, 'taller%sexercise')
