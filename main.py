import cv2
import numpy as np
import mss
import vgamepad as vg
import time

# إعداد يد التحكم الوهمية (Virtual Controller)
gamepad = vg.VX360Gamepad()

# إعدادات التتبع - نسخة اليد الذكية
AIM_STRENGTH = 0.5  # قوة السحب (بين 0.1 و 1.0)
FOV_SIZE = 250      # مساحة الدائرة وسط الشاشة التي يراقبها البرنامج

def start_joypad_engine():
    sct = mss.mss()
    # تحديد منطقة البحث وسط الشاشة (تعدل حسب دقة شاشتك)
    monitor = {"top": 415, "left": 835, "width": FOV_SIZE, "height": FOV_SIZE}

    print("نظام AI Aim Assist يعمل.. بانتظار رصد الهدف")

    try:
        while True:
            # التقاط صورة لمنطقة البحث
            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # تحديد لون شريط الدم الأحمر (العدو)
            lower_red = np.array([0, 150, 150])
            upper_red = np.array([10, 255, 255])
            mask = cv2.inRange(hsv, lower_red, upper_red)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                c = max(contours, key=cv2.contourArea)
                if cv2.contourArea(c) > 40:
                    M = cv2.moments(c)
                    if M["m00"] != 0:
                        # حساب المسافة وتحويلها لقيم تناسب عصا التحكم (-1.0 إلى 1.0)
                        target_x = (int(M["m10"] / M["m00"]) - FOV_SIZE/2) / (FOV_SIZE/2)
                        target_y = (int(M["m01"] / M["m00"]) - FOV_SIZE/2) / (FOV_SIZE/2)

                        # تحريك العصا اليمنى (Right Joystick) تلقائياً
                        gamepad.right_joystick_float(x_value_float=target_x * AIM_STRENGTH, 
                                                   y_value_float=target_y * AIM_STRENGTH)
                        gamepad.update()
            else:
                # تصفير حركة العصا عند عدم وجود هدف
                gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
                gamepad.update()

            time.sleep(0.01)
    except KeyboardInterrupt:
        print("تم إيقاف النظام.")

if __name__ == "__main__":
    start_joypad_engine()
