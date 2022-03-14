import os

def ospathjoin(dir_list: list):
    return os.path.join(*dir_list)


def walk_file(find_dir='./', find_str=".xml"):
    for root, dirs, files in os.walk(find_dir, topdown=False):
        for name in files:
            file_str = os.path.join(root, name)
            if file_str.endswith(find_str):
                yield file_str
    return



if __name__=="__main__":
    print(ospathjoin(["./", "images", "1.jpg"]))