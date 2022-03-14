import os
import glob
from .path import ospathjoin



def check_file(file):
    # Search for file if not found
    if os.path.isfile(file) or file == '':
        return file
    else:
        files = glob.glob('./**/' + file, recursive=True)  # find file
        assert len(files), 'File Not Found: %s' % file  # assert file was found
        assert len(files) == 1, "Multiple files match '%s', specify exact path: %s" % (file, files)  # assert unique
        return files[0]  # return file


def check_dir(dir):
    if os.path.exists(dir):
        return dir
    else:
        os.makedirs(dir)
    return dir




def check_labelImg_data(src_dir, Delete=False, fixstr = ""):
    files = os.listdir(src_dir)
    image_num = 0

    for img_file in files:
        img_file = img_file
        after_str = os.path.splitext(img_file)[-1]
        len_af = len(after_str)
        if after_str in ['.png', '.jpg', '.jpeg']:
            image_num+=1
            img_name = img_file[:-1*len_af] + '.xml'
        elif img_file.endswith('.xml'):
            img_name =img_file[:-4] + ".jpg"
        else:
            print("the file {} is not in ['.jpg', '.xml']".format(img_file))
            os_del_str = "rm " + ospathjoin([src_dir, img_file])
            print(os_del_str)
            os.system(os_del_str)
        if img_name not in files:
            if Delete:
                os_del_str = "rm " + ospathjoin([src_dir, img_file])
                print(os_del_str)
                os.system(os_del_str)
                image_num -=1
            else:
                print("check fail because of the file:", img_file)
                exit()
    if image_num != len(os.listdir(src_dir)) // 2:
        print("img_num: ", image_num)
        print("len(os.listdir(src_dir)):", len(os.listdir(src_dir)))
        print("image num is not equal to xml.")
    else:
        for file in os.listdir(src_dir):
            rename_str = "mv " + ospathjoin([src_dir, file.replace(' ', '\ ').replace('&', '\&').replace('=', '\=').replace( '!', '\!') \
                                            .replace("'", "\'").replace(",", "\,")]) + \
                         ' ' + ospathjoin([src_dir, fixstr + file.replace(' ', '_').replace('&', '_').replace('=', '_').replace( \
                                               '!', '_').replace("'", "_").replace(",", "_").replace('-', '_')])
            print(rename_str)
            os.system(rename_str)
        print(image_num)
        print(len(os.listdir(src_dir)))
    return


