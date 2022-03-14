from torchvision import transforms
from PIL import Image
import numpy as np


def resize_and_pad_image(im, max_size=224):
    try:
        width, height = im.size
        max_length = max(width, height)
        new_im = Image.new("RGB", (max_size, max_size))
        if width > height:
            new_width = max_size
            new_height = int(new_width*height/width)
            top_x = 0
            top_y = (new_width-new_height)//2
            im_resized = im.resize((new_width, new_height))
            new_im.paste(im_resized, (top_x, top_y))
        else:
            new_height = max_size
            new_width = int(new_height*width/height)
            im_resized = im.resize((new_width, new_height))
            top_x = (new_height-new_width)//2
            top_y = 0
            new_im.paste(im_resized, (top_x, top_y))
        # else:
        #     new_im = im
        return new_im
    except Exception as e:
        print(e.message)
        return None


def torch_preprocess(im):
    resized_image = resize_and_pad_image(im)
    if type(resized_image) == None:
        return None
    transform = transforms.Compose([
        # transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]), ])
    image = transform(resized_image)
    image = image.view(1, image.size()[0], image.size()[1], image.size()[2])
    return image


def onnx_preprocess(im):
    resized_and_padded = resize_and_pad_image(im)
    img_data = np.array(resized_and_padded, dtype=np.float32)
    mean_vec = np.array([0.485, 0.456, 0.406],
                        dtype=np.float32).reshape((1, 1, 3))
    stddev_vec = np.array([0.229, 0.224, 0.225],
                          dtype=np.float32).reshape((1, 1, 3))
    norm_img_data = np.zeros(img_data.shape, dtype=np.float32)
    norm_img_data = img_data/255.0 - mean_vec
    norm_img_data /= stddev_vec
    return norm_img_data
