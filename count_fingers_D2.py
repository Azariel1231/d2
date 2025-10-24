import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

def countFingers(image, hand_landmarks, handNo=0):

    if hand_landmarks:
        #obtener los puntos de referencia de la mano
        landmarks = hand_landmarks[handNo].landmark
        #print(landmarks)

        #contar los d2
        fingers = []
        
        for lm_index in tipIds:
            #obtener la posicion de los d2
            finger_tip_y = landmarks[lm_index].y
            finger_bottom_y = landmarks[lm_index - 2].y

            #verificar si el d2 esta abierto o cerrado
            if lm_index != 4:
                if finger_tip_y < finger_bottom_y:
                    fingers.append(1)
                    print("El dedo con id", lm_index, "esta abierto")

                if finger_tip_y > finger_bottom_y:
                    fingers.append(0)
                    print("el dedo con id",lm_index, "esta cerrado. ")
        
        totalFingers = fingers.count(1)

        text = f'Dedos: {totalFingers}'

        cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


def drawHandLandmarks(image, hand_landmarks):
    #dibuja las conexiones y puntos de la mano
    if hand_landmarks:

        for landmarks in hand_landmarks:
            
            mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)

while True:
    success, image = cap.read()
    if not success:
        print("No se pudo acceder a la cámara.")
        break

    image = cv2.flip(image, 1)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #detectar los puntos/manos
    results = hands.process(image_rgb)

    #resultados
    #hand_landmarks = (image, results.multi_hand_landmarks)

    #drawHandLandmarks(image,hand_landmarks)
    drawHandLandmarks(image, results.multi_hand_landmarks)

    countFingers(image, results.multi_hand_landmarks)


    cv2.imshow("Controlador de medios", image)

    key = cv2.waitKey(1)
    if key == 32:
        break

    
cap.release()
cv2.destroyAllWindows()
        