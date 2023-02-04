import cv2
import mediapipe as mp

from pynput.keyboard import Key,Controller

state=None

keyBoard=Controller()


cap= cv2.VideoCapture(0)

drawing= mp.solutions.drawing_utils
hands= mp.solutions.hands

width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

hands_object= hands.Hands(max_num_hands=3)

def count_figures(d):
    global state
    count=0
    threshScore= (d.landmark[0].y*100 -d.landmark[9].y*100)/2

    if(d.landmark[5].y*100-d.landmark[8].y*100)>threshScore:
        count+=1

    if(d.landmark[9].y*100-d.landmark[12].y*100)>threshScore:
        count+=1

    if(d.landmark[13].y*100-d.landmark[16].y*100)>threshScore:
        count+=1

    if(d.landmark[17].y*100-d.landmark[20].y*100)>threshScore:
        count+=1

    # if(d.landmark[5].x*100 -d.landmark[4].x*100)>5:
    #     count+=1

    totalFingers= count
    if totalFingers ==4:
        state="play"
    if totalFingers== 0 and state=="play":
        state="pause"
        keyBoard.press(Key.space)
 
# move tje video forward and backward
    finger_tip_x=(d.landmark[8].x)*width
    if totalFingers == 1:
        if finger_tip_x<width-350:         
            print("play backward") 
            keyBoard.press(Key.left)
        if finger_tip_x>width-80:
            print("PLay foreard")
            keyBoard.press(Key.right)


    print("what is video state: ", state)
    return totalFingers



while True:
    dummy,image= cap.read()
    image=cv2.flip(image,1)

    result=hands_object.process(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))

    if result.multi_hand_landmarks:
        hand_keyPoints= result.multi_hand_landmarks[0]

        c=count_figures(hand_keyPoints)
        print(c)
        cv2.putText(image,"Figures: "+str(c),(200,200),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
        drawing.draw_landmarks(image,hand_keyPoints,hands.HAND_CONNECTIONS)
  
    cv2.imshow("Gestures",image)

    key= cv2.waitKey(1)
    if key==27:
        break
cv2.destroyAllWindows()