import cv2
import numpy as np
import mss
import vgamepad as vg
import time

# إعداد اليد الوهمية
gamepad = vg.VX360Gamepad()
AIM_STRENGTH = 0.5  # قوة السحب
FOV_SIZE = 250      # دائرة البحث

def start_engine():
    sct = mss.mss()
    monitor = {"top": 415, "left": 835, "width": FOV_SIZE, "height": FOV_SIZE}
    print("نظام AI Aim Assist يعمل.. بانتظار الهدف")

    while True:
        img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([0, 150, 150]), np.array([10, 255, 255]))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 40:
                M = cv2.moments(c)
                if M["m00"] != 0:
                    target_x = (int(M["m10"] / M["m00"]) - FOV_SIZE/2) / (FOV_SIZE/2)
                    target_y = (int(M["m01"] / M["m00"]) - FOV_SIZE/2) / (FOV_SIZE/2)
                    gamepad.right_joystick_float(x_value_float=target_x * AIM_STRENGTH, y_value_float=target_y * AIM_STRENGTH)
                    gamepad.update()
        else:
            gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
            gamepad.update()
        time.sleep(0.01)

if __name__ == "__main__":
    start_engine() 