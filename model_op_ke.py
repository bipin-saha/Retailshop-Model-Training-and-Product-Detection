import torch
import cv2
import pandas as pd
import json
from serialRW import *

target = "Safekeeper"
baudrate = 115200
port = '/dev/ttyACM0'

classes = []
img = cv2.VideoCapture(0)


model = torch.hub.load("yolov5", 'custom', path="315_Image_99.5_best.pt", source='local')
image_product_map_count = {'Safekeeper': 0, 'Spa': 0, 'Superstar': 0}


def product_counter(img,coords,target):
    view_classes = set([])
    for index, row in coords.iterrows():
        counter = 1
        start_point = (int(row['xmin']), int(row['ymin']))
        end_point = (int(row['xmax']), int(row['ymax']))
        
        class_name = row['name']
        view_classes.add(class_name)
        
        img = cv2.rectangle(img, start_point, end_point,(0,255,255),2)
        cv2.putText(img, str(counter), start_point, cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1)

        if class_name in image_product_map_count:
            image_product_map_count[class_name] = image_product_map_count.get(class_name) + 1

        counter = counter+1
    
    print(list(view_classes))
    
    
    if len(list(view_classes)) == 0:
        message = {
        "instruction" : "Forward",
        "product_map" : image_product_map_count,
        "reamrks" : "No Product Found, Check Position"}
        message = json.dumps(message, indent=4)
        message = str(message) + "#"

    elif len(list(view_classes)) > 0:
        if list(view_classes)[0] == target:
            message = {
            "instruction" : "Collect Product",
            "product_map" : image_product_map_count,
            "reamrks" : "Product Found"}
            message = json.dumps(message, indent=4)
            message = str(message) + "#"
        else:
            message = {
            "instruction" : "Correct Position",
            "product_map" : image_product_map_count,
            "reamrks" : "No Product Found, Check Position"}
            message = json.dumps(message, indent=4)
            message = str(message) + "#"
    
    elif len(list(view_classes)) > 1:
        if target in view_classes:
            message = {
            "instruction" : "Adjust Position",
            "product_map" : image_product_map_count,
            "reamrks" : "Product Found, Adjust Position Slightly"}
            message = json.dumps(message, indent=4)
            message = str(message) + "#"

        else:
            message = {
            "instruction" : "Correct Position",
            "product_map" : image_product_map_count,
            "reamrks" : "No Product Found, Check Position"}
            message = json.dumps(message, indent=4)
            message = str(message) + "#"
    else:
        message = {
        "instruction" : "Default Instruction",
        "product_map" : image_product_map_count,
        "reamrks" : "Default Remarks"}
        message = json.dumps(message, indent=4)
        message = str(message) + "#"

    return img, image_product_map_count,message  


def bbox_generator(img):
    results = model(img)
    coords = pd.DataFrame(results.pandas().xyxy[0])
    coords.sort_values(by=['xmin'], inplace=True)

    return coords



while True:
    boardAcessRequest = False    
    
    try:
        board_message = read_line(baudrate, port)
    except Exception as e:
        board_message = "Reading Error"
        print(board_message)
    
    if board_message == "OpenCamera":
        boardAcessRequest = True
        if boardAcessRequest == True:
            try:
                ret, frame = img.read()
                frame = frame[10:470, 230:370]
                coords = bbox_generator(frame)
                frame, count, message = product_counter(frame, coords, target)
    
                frame = cv2.flip(frame, 1)
    
                cv2.imshow('Frame', frame)
                
                 
                try:
                    write_line(baudrate, port, message)
                except Exception as e:
                    print("Error in message wrtiting")
                
                print(count)
                print(message)
                if cv2.waitKey(0) & 0xFF == ord('q'):
                    break
            except Exception as e:
                print("Overall Error")
            
            

img.release()
cv2.destroyAllWindows()