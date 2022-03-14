from lxml import etree
import tensorflow as tf
from object_detection.utils import dataset_util
import os
from tqdm import tqdm
xml_path = ''
output_txt_path = ''
list_xml = os.listdir(xml_path)
def get_box(path,output_name):
    with tf.gfile.GFile(path, 'r') as fid:
        xml_str = fid.read()
    xml = etree.fromstring(xml_str)
    data = dataset_util.recursive_parse_xml_to_dict(xml)['annotation']
    #width = int(data['size']['width'])
    #height = int(data['size']['height'])
    with open(output_txt_path+output_name,'w') as f:
        if 'object' in data:
            for obj in data['object']:
                f.write(str(obj['name']))
                f.write(',')
                f.write(str(int(obj['bndbox']['xmin'])))
                f.write(',')
                f.write(str(int(obj['bndbox']['ymin'])))
                f.write(',')
                f.write(str(int(obj['bndbox']['xmax'])))
                f.write(',')
                f.write(str(int(obj['bndbox']['ymax'])))
for xml in tqdm(list_xml):
    get_box(xml_path+xml,xml.split('.')[0]+'.txt')