import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipids=[4,8,12,16,20]

# Define a function to count fingers
def count_fingers(image,hand_landmarks,handNo=0):
    if hand_landmarks:
        landmarks=hand_landmarks[handNo].landmark
        fingers=[]
        for lmindex in tipids:
            finger_tip_y=landmarks[lmindex].y
            finger_bottom_y=landmarks[lmindex-2].y
            thumb_tip_y=landmarks[lmindex].y
            thumb_bottom_y=landmarks[lmindex-2].y
            if lmindex!=4:
                if finger_tip_y<finger_bottom_y:
                    fingers.append(1)
                if finger_tip_y>finger_bottom_y:
                    fingers.append(0)
            else:
                if thumb_tip_y<thumb_bottom_y:
                    fingers.append(0)
                    print('Thumb',lmindex,'is closed')
                    cv2.putText(image,"Like",(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),2)
                if thumb_tip_y>thumb_bottom_y:
                    fingers.append(1)
                    print('Thumb',lmindex,'is open')
                    cv2.putText(image,"Dislike",(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),2)
        total_fingers=fingers.count(1)
        text=f'Fingers:{total_fingers}'
   


# Define a function to 
def drawHandLanmarks(image, hand_landmarks):

    # Darw connections between landmark points
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
         mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)


while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detect the Hands Landmarks 
    results = hands.process(image)

    # Get landmark position from the processed result
    hand_landmarks = results.multi_hand_landmarks

    # Draw Landmarks
    drawHandLanmarks(image, hand_landmarks)

    # Get Hand Fingers Position        
    count_fingers(image,hand_landmarks)

    cv2.imshow("Media Controller", image)

    # Quit the window on pressing Sapcebar key
    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()
