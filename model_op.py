import torch
import cv2
import os
import pandas as pd
import math
import itertools

classes = []
img = cv2.VideoCapture(0)


model = torch.hub.load("yolov5", 'custom', path="315_Image_99.5_best.pt", source='local')
"""
image_product_map_count = {'person': 0, 'bicycle': 0, 'car': 0, 'motorcycle': 0, 
                    'airplane': 0, 'bus': 0, 'train': 0, 'truck': 0, 'boat': 0, 'traffic light': 0, 
                    'fire hydrant': 0, 'stop sign': 0, 'parking meter': 0, 'bench': 0, 'bird': 0, 
                    'cat': 0, 'dog': 0, 'horse': 0, 'sheep': 0, 'cow': 0, 'elephant': 0, 'bear': 0, 
                    'zebra': 0, 'giraffe': 0, 'backpack': 0, 'umbrella': 0, 'handbag': 0, 'tie': 0, 
                    'suitcase': 0, 'frisbee': 0, 'skis': 0,'snowboard': 0, 'sports ball': 0, 'kite': 0, 
                    'baseball bat': 0, 'baseball glove': 0, 'skateboard': 0, 'surfboard': 0, 
                    'tennis racket': 0, 'bottle': 0, 'wine glass': 0, 'cup': 0, 'fork': 0, 'knife': 0, 
                    'spoon': 0, 'bowl': 0, 'banana': 0, 'apple': 0, 'sandwich': 0, 'orange': 0, 'broccoli': 0, 
                    'carrot': 0, 'hot dog': 0, 'pizza': 0, 'donut': 0, 'cake': 0, 'chair': 0, 'couch': 0, 
                    'potted plant': 0, 'bed': 0, 'dining table': 0, 'toilet': 0, 'tv': 0, 'laptop': 0, 
                    'mouse': 0, 'remote': 0, 'keyboard': 0, 'cell phone': 0, 'microwave': 0, 'oven': 0, 
                    'toaster': 0, 'sink': 0, 'refrigerator': 0, 'book': 0, 'clock': 0, 'vase': 0, 'scissors': 0, 
                    'teddy bear': 0, 'hair drier': 0, 'toothbrush': 0}

"""
image_product_map_count = {'Safekeeper': 0, 'SPA': 0, 'Superstar': 0}

keys_list = list(image_product_map_count.keys())
target = ""
product_location_mid = []
for i in range(80):
    product_polar_radius = []
    product_location_mid.append(product_polar_radius)

def send_command(weight):
    pass

def estimate_location(coords, image_product_map_count, direction):
    if direction == 'lr':
        pass
    
    elif direction == 'rl':
        location = []
        for index, row in coords.iterrows():
            x_mid = (row['xmin'] + row['xmax'])/2
            y_mid = (row['ymin'] + row['ymax'])/2
            polar_radius = math.sqrt(x_mid**2 + y_mid**2)
            class_id = int(row['class'])
            product_location_mid[class_id].append(polar_radius)
            #print(product_location_mid)
        
        for inner_list in range(0, len(product_location_mid)):
            
            try:
                avg = sum(product_location_mid[inner_list])/len(product_location_mid[inner_list])
                product_location_mid[inner_list] = [avg]
                
                #print(avg, keys_list[inner_list])
                #print()
            except Exception as e:
                pass
            
        copy_product_location_mid = product_location_mid
        products = list(itertools.chain.from_iterable(product_location_mid))
        #print(len(copy_product_location_mid))
        print(products)
        
        for item in products:
            product = copy_product_location_mid.index([item])
            location.append(keys_list[product])
        
        print(location)
    
    #location = max(image_product_map_count, key=image_product_map_count.get)
    #near_left_location = list(image_product_map_count.values())
    #near_left_location = near_left_location.sort()[-2]
    #near_right_location =
    #return location


def path_weight(location,target):
    weight = location    
    return weight


def product_counter(img,coords):
    counter = 1
    
    for index, row in coords.iterrows():
        start_point = (int(row['xmin']), int(row['ymin']))
        end_point = (int(row['xmax']), int(row['ymax']))
        class_name = row['name']
        print(class_name)
        img = cv2.rectangle(img, start_point, end_point,(0,255,255),2)
        cv2.putText(img, str(counter), start_point, cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1)
        counter +=1

        if class_name in image_product_map_count:
            image_product_map_count[class_name] = image_product_map_count.get(class_name) + 1

        #print(image_product_map_count)
    
    return img, image_product_map_count    


def bbox_generator(img):
    results = model(img)
    coords = pd.DataFrame(results.pandas().xyxy[0])
    coords.sort_values(by=['xmin'], inplace=True)

    return coords


while True:
    ret, frame = img.read()
    coords = bbox_generator(frame)
    frame, _ = product_counter(frame, coords)
    estimate_location(coords, image_product_map_count, "rl")

    frame = cv2.flip(frame, 1)
    cv2.imshow('Frame', frame)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

img.release()
cv2.destroyAllWindows()