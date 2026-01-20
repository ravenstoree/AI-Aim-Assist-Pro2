import cv2
import numpy as np
import mss
import vgamepad as vg
import time

# إعداد اليد الوهمية
gamepad = vg.VX360Gamepad()
AIM_STRENGTH = 0.6  # قوة السحب (زيديها حسب رغبتك)
FOV_SIZE = 300      # مساحة الرصد وسط الشاشة

def start_raven_engine():
    sct = mss.mss()
    monitor = {"top": 390, "left": 810, "width": FOV_SIZE, "height": FOV_SIZE}
    print("نظام ريڤن AI يعمل بنجاح.. تأكدي من ملء الشاشة")

    try:
        while True:
            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, np.array([0, 150, 150]), np.array([10, 255, 255]))
            
            # نافذة الرؤية للتأكد من الرصد
            cv2.imshow("Raven Vision - Live", frame) 
            if cv2.waitKey(1) & 0xFF == ord('q'): break
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                c = max(contours, key=cv2.contourArea)
                if cv2.contourArea(c) > 30:
                    M = cv2.moments(c)
                    if M["m00"] != 0:
                        target_x = (int(M["m10"] / M["m00"]) - FOV_SIZE/2) / (FOV_SIZE/2)
                        target_y = (int(M["m01"] / M["m00"]) - FOV_SIZE/2) / (FOV_SIZE/2)
                        # تحريك الأيم (تم تصحيح القوس هنا)
                        gamepad.right_joystick_float(x_value_float=target_x * AIM_STRENGTH, y_value_float=target_y * AIM_STRENGTH)
                        gamepad.update()
            else:
                gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
                gamepad.update()
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("تم إيقاف النظام.")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    start_raven_engine() 