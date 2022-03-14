from PIL import Image,ImageFilter,ImageEnhance
import numpy as np
def sort_boxes(boxes):
    boxes = sorted(boxes, key=lambda x: sum([x[1], x[3], x[5], x[7]]))
    boxes = [b for b in boxes if (b[5]-b[3])>13]
    boxes_order = []
    boxes_order.append(boxes[0])
    boxes_order += sorted(boxes[1:3], key=lambda x: sum([x[0], x[2], x[4], x[6]]))
    boxes_order += sorted(boxes[3:6], key=lambda x: sum([x[0], x[2], x[4], x[6]]))
    boxes_order += boxes[6:]
    return boxes_order
def result_read(image_path,txt_path):
    img = Image.open(image_path).convert('RGB')
    #img = ImageEnhance.Sharpness(img).enhance(1.5)
    #img = img.filter(ImageFilter.SHARPEN)
    boxes = []
    with open(txt_path,'r') as f:
        lines = f.readlines()
    for line in lines:
        boxes.append([int(i) for i in line.strip('\n').split(',')[:8]])
    return np.array(img),boxes
if __name__ == '__main__':
    image_path = './6002_2.jpg'
    txt_path = './6002_2_total.txt'
    i , b = result_read(image_path,txt_path)
    print(b)
