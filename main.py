import cv2  
import mediapipe as mp 
import numpy as np  
from collections import deque  

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Camera not work")
    exit()  

frame_width = 640  
frame_height = 480  

cam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)  
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

actual_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
canvas = np.zeros((actual_height, actual_width, 3), dtype=np.uint8)


prev_x, prev_y = 0, 0
color = (255, 0, 0) 

point_history = deque(maxlen=5)
min_movement = 3
is_drawing = False

with mp_hands.Hands(
    model_complexity=1,  
    min_detection_confidence=.75,  
    min_tracking_confidence=0.75 
) as hands:
   
    while cam.isOpened():
        
        success, image = cam.read()
        if not success:
            print("Error")
            continue  

       
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,  
                    hand_landmarks,  
                    mp_hands.HAND_CONNECTIONS, 
                    mp_drawing_styles.get_default_hand_landmarks_style(), 
                    mp_drawing_styles.get_default_hand_connections_style()  
                )

                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                h, w, _ = image.shape
                tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)
                ix, iy = int(index_tip.x * w), int(index_tip.y * h)

                distance = ((tx - ix) ** 2 + (ty - iy) ** 2) ** 0.5

                print(f"Distance: {distance}, Thumb: ({tx}, {ty}), Index: ({ix}, {iy})")
                if distance < 40: 
                 
                    point_history.append((ix, iy))
                    
                   
                    if len(point_history) == point_history.maxlen:
                      
                        smoothed_x = sum(p[0] for p in point_history) // len(point_history)
                       
                        smoothed_y = sum(p[1] for p in point_history) // len(point_history)
                        
                        
                        if not is_drawing:
                           
                            prev_x, prev_y = smoothed_x, smoothed_y
                            is_drawing = True
                        else:
                            movement = ((smoothed_x - prev_x) ** 2 + (smoothed_y - prev_y) ** 2) ** 0.5
                            if movement >= min_movement:
                                cv2.line(
                                    canvas, 
                                    (prev_x, prev_y), 
                                    (smoothed_x, smoothed_y), 
                                    color,  7
                                )
                                prev_x, prev_y = smoothed_x, smoothed_y
                else:
                    is_drawing = False
                    point_history.clear()

       
        gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
       
        mask = cv2.threshold(gray_canvas, 1, 255, cv2.THRESH_BINARY)[1]
     
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        
     
        result = image.copy()
      
        result = np.where(mask > 0, canvas, result)

   
        cv2.imshow('proooject', result)

    
        key = cv2.waitKey(5) & 0xFF
        if key == ord('q'): 
            break
        elif key == ord('c'):  
            canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        elif key == ord('r'):
            color = (0, 0, 225)
        elif key == ord('g'):
            color = (0, 225, 0)
        elif key == ord('b'):
            color = (225, 0, 0)
cam.release()
cv2.destroyAllWindows()
