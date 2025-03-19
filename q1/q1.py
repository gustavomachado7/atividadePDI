### Aluno: Gustavo Iusi Machado da Silva
### RM: 95409 -> vídeo q1B.mp4

import cv2
import numpy as np

flag_ultrapassagem = False

def segmentacao(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    azul_claro_min = np.array([90, 50, 90])
    azul_claro_max = np.array([120, 255, 255])

    mascara_azul = cv2.inRange(hsv, azul_claro_min, azul_claro_max)

    salmao_claro_min = np.array([10, 50, 150])
    salmao_claro_max = np.array([20, 255, 255])

    mascara_salmao = cv2.inRange(hsv, salmao_claro_min, salmao_claro_max)
  
    frame = contorno(mascara_azul, mascara_salmao)
    
    return frame


def contorno(mascara_azul, mascara_salmao):
    global flag_ultrapassagem
    maior_contorno = None
    maior_area = 0


    contornos_img_azul, _ = cv2.findContours(mascara_azul, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contornos_img_salmao, _ = cv2.findContours(mascara_salmao, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    

    box_azul = None
    box_salmao = None

    
    if contornos_img_azul:
        maior_contorno_azul = max(contornos_img_azul, key = cv2.contourArea)
        box_azul = cv2.boundingRect(maior_contorno_azul)  # Equivalente a: x, y, w, h
        area_azul = cv2.contourArea(maior_contorno_azul)

        
        if area_azul > maior_area:
            maior_area = area_azul
            maior_contorno = maior_contorno_azul
            

    if contornos_img_salmao:
        maior_contorno_salmao = max(contornos_img_salmao, key = cv2.contourArea)
        box_salmao = cv2.boundingRect(maior_contorno_salmao) # Equivalente a: x, y, w, h
        area_salmao = cv2.contourArea(maior_contorno_salmao)

        
        if area_salmao > maior_area:
            maior_area = area_salmao
            maior_contorno = maior_contorno_salmao

    
    if maior_contorno is not None:
        x, y, w, h = cv2.boundingRect(maior_contorno)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        

    if box_azul and box_salmao:
        x1, y1, w1, h1 = box_azul
        x2, y2, w2, h2 = box_salmao

        
        if colisao(x1, y1, w1, h1, x2, y2, w2, h2):
            cv2.putText(frame, "COLISAO DETECTADA", (500, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            flag_ultrapassagem = True
           
            
        if flag_ultrapassagem and barreira_ultrapassada(y2, y1, h1):
            cv2.putText(frame, "PASSOU BARREIRA", (500, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            flag_ultrapassagem = False
               
                
        # Se quiser que a mensagem de "passou barreira" apareça apenas após
        # a colisão (num frame rápido), devo COMENTAR as linhas 80, 85 e 86
        if flag_ultrapassagem is False and barreira_ultrapassada(y2, y1, h1):
            cv2.putText(frame, "PASSOU BARREIRA", (500, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                

    return frame



def colisao(x1, y1, w1, h1, x2, y2, w2, h2):
  
    return  (x1 + w1 > x2 and x2 + w2 > x1 
             and y1 + h1 > y2 and y2 + h2 > y1)



def barreira_ultrapassada(y2, y1, h1):

    return y2 > y1 + h1 


cap = cv2.VideoCapture("q1/q1B.mp4")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Erro: Não foi possível capturar o frame.")
        break
    
    
    frame = cv2.resize(frame, (870, 600))


    processamento = segmentacao(frame)

   
    cv2.imshow("Movimentando Objetos", processamento)

    
    key = cv2.waitKey(5) & 0xFF
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()