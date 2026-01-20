import cv2
import numpy as np
import mss
import vgamepad as vg
import time

# 1. إعداد اليد الوهمية
gamepad = vg.VX360Gamepad()
AIM_STRENGTH = 0.6  # قوة سحب الأيم (زيديها إذا كان السحب ضعيفاً)
FOV_SIZE = 300      # مساحة الدائرة وسط الشاشة

def start_raven_engine():
    sct = mss.mss()
    # إحداثيات البحث لمنتصف الشاشة (دقة 1080p)
    monitor = {"top": 390, "left": 810, "width": FOV_SIZE, "height": FOV_SIZE}
    
    print("نظام ريڤن AI يعمل.. تأكدي من ملء الشاشة")

    while True:
        # التقاط الشاشة
        img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        # تحويل الألوان لرصد شريط الدم الأحمر
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 150, 150])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        
        # --- نافذة الرؤية (تريكِ ماذا يرى البرنامج الآن) ---
        cv2.imshow("Raven Vision - Live", frame) 
        if cv2.waitKey(1) & 0xFF == ord('q'): break
        
        # حساب مكان العدو
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 30:
                M = cv2.moments(c)
                if M["m00"] != 0:
                    target_x = (int(M["m10"] / M["m00"]) - FOV_SIZE/2) / (FOV_SIZE/2)
                    target_y = (int(M["m01"] / M["m00"]) - FOV_SIZE/2) / (FOV_SIZE/2)

                    # تحريك الأيم
                    gamepad.right_joystick_float(x_value_float=target_x * AIM_STRENGTH, 
                                               y_value_