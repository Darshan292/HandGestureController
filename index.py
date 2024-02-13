import cv2
import mediapipe as mp
import pyautogui, ctypes
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

screen_width, screen_height = pyautogui.size()
index_x = 0
index_y = 0
thumb_x = 0
thumb_y = 0

#double click
prev_click = 0

#scroll
prev_scrlpoint_y = 0
prev_scrlpoint_x = 0

#volume
prev_volpoint_y = 0
prev_volpoint_x = 0
Volume_up = 0xAF
Volume_down = 0xAE

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_height, frame_width, _ = frame.shape
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]

        index_finger = hand_landmarks.landmark[8]  #Index
        thumb = hand_landmarks.landmark[4]  #Thumb
        middle_finger = hand_landmarks.landmark[12]#Middle
        ring_finger = hand_landmarks.landmark[16]#Ring

        ind_x = int(index_finger.x*frame_width)
        ind_y = int(index_finger.y*frame_height)
        ind_z = int(index_finger.z)

        mid_x = int(middle_finger.x*frame_width)
        mid_y = int(middle_finger.y*frame_height)
        mid_z = int(middle_finger.z)
       
        thu_x = int(thumb.x*frame_width)
        thu_y = int(thumb.y*frame_height)
        thu_z = int(thumb.z)

        rin_x = int(ring_finger.x*frame_width)
        rin_y = int(ring_finger.y*frame_height)
        rin_z = int(ring_finger.z)

        # Screen coordinates
        index_x = ((screen_width/frame_width)+1.7)*ind_x
        index_y = ((screen_height/frame_height)+1.7)*ind_y

        # Finger tips highlight
        cv2.circle(frame, center=(ind_x,ind_y), radius=10, color=(255, 0, 0))
        cv2.circle(frame, center=(thu_x, thu_y), radius=10, color=(255, 0, 0))
        cv2.circle(frame, center=(mid_x, mid_y), radius=10, color=(255, 0, 0))
        cv2.circle(frame, center=(rin_x, rin_y), radius=10, color=(255, 0, 0))

        # Move cursor
        if ((rin_x - thu_x)**2 + (rin_x - thu_x)**2 +(rin_z-thu_z)**2) > 60**2 and (((ind_x - thu_x)**2 + (ind_y - thu_y)**2+(ind_z-thu_z)**2)) > 60**2:
            pyautogui.moveTo(index_x, index_y)
        
        #click and double click
        if ((mid_x - thu_x)**2 + (mid_y - thu_y)**2+(mid_z-thu_z)**2) < 75**2 and ((rin_x - mid_x)**2 + (rin_y - mid_y)**2+(rin_z-mid_z)**2)>35**2:
            current_click = time.time()
            if current_click - prev_click < 1:
                print("Double click")
                pyautogui.doubleClick()
                pyautogui.sleep(0.5)
            else:
                print("click")
                pyautogui.click()

            prev_click = current_click

        #to scroll
        if ((rin_x - thu_x)**2 + (rin_y - thu_y)**2+(rin_z-thu_z)**2) < 35**2 and ((rin_x - mid_x)**2 + (rin_y - mid_y)**2+(rin_z-mid_z)**2)>35**2:
            print("scroll ",str(((rin_x - thu_x)**2 + (rin_y - thu_y)**2+(rin_z-thu_z)**2)))
            if index_y-prev_scrlpoint_y<index_y and index_y-prev_scrlpoint_y>0:
                pyautogui.scroll(100)
            elif index_y-prev_scrlpoint_y<index_y and index_y-prev_scrlpoint_y<0:
                pyautogui.scroll(-100)        
            prev_scrlpoint_y=index_y
            prev_scrlpoint_x=index_x
        
        #to controll volume
        if ((ind_x - thu_x)**2 + (ind_y - thu_y)**2+(ind_z-thu_z)**2) < 45**2 and ((ind_x - mid_x)**2 + (ind_y - mid_y)**2+(ind_z-mid_z)**2)>50**2:
            if index_x-prev_volpoint_x<index_x and index_x-prev_volpoint_x>0:
                print("Volume up")
                ctypes.windll.user32.keybd_event(Volume_up, 0, 0, 0)
                time.sleep(0.2)
            elif index_x-prev_volpoint_x<index_x and index_x-prev_volpoint_x<0:
                print("Volume down")
                ctypes.windll.user32.keybd_event(Volume_down, 0, 0, 0)
            prev_volpoint_x = index_x

    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
