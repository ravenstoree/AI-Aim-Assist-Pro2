import cv2
import numpy as np
import mss
import vgamepad as vg
import time

# تشغيل يد التحكم الوهمية
gamepad = vg.VX360Gamepad()
AIM_STRENGTH = 0.6  # قوة السحب
FOV_SIZE = 300      # كبرنا دائرة البحث لتسهيل الرصد

def start_raven_pro():
    sct = mss.mss()
    # إحداثيات البحث (تعتمد على أن اللعبة ملء الشاشة 1080p)
    monitor = {"top": 390, "left": 810, "width": FOV_SIZE, "height": FOV_SIZE}
    
    print("جاري تشغيل محرك ريڤن... تأكدي أن اللعبة ملء الشاشة")

    while True:
        img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # تتبع اللون الأحمر الفاقع لشريط الدم
        lower_red = np.array([0, 150, 150])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        
        # --- نافذة الرؤية (للتأكد من اشتغال البرنامج) ---
        cv2.imshow("Raven Vision - White means Target Found", mask)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 30:
                M = cv2.moments(c)
                if M["m00"] != 0:
                    # حساب الهدف
                    target_x = (int(M["m10"] / M["m00"]) - FOV_SIZE/2) / (FOV_SIZE/2)
                    target_y = (int(M["m01"] / M["m00"]) - FOV_SIZE/2) / (FOV_SIZE/2)

                    # إرسال الحركة لليد
                    gamepad.right_joystick_float(x_value_float=target_x * AIM_STRENGTH, 
                                               y_value_float=target_y * AIM_STRENGTH)
                    gamepad.update()
                    print("🎯 تم رصد هدف!")
        else:
            gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
            gamepad.update()

        time.sleep(0.01)

if __name__ == "__main__":
    start_raven_pro() 