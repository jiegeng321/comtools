import PySimpleGUI as sg
import os
import sys, stat
import uuid
import time
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #??Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
num_per_page = 20
key_dir = ".key"
key_file_dir = os.path.join(key_dir,'userkey')
#base_path = os.path.abspath(".")
ppt_dir = resource_path(os.path.join(".src","ppt"))
video_dir = resource_path(os.path.join(".src","video"))
ico_file = resource_path(os.path.join(".src","images","logo.ico"))

ppt_list = sorted(os.listdir(ppt_dir))[:13]
ppt_num = len(ppt_list)
max_title_len = max([len(i) for i in ppt_list])
sg.theme('DarkAmber')   # Add a touch of color
#sg.theme_previewer()

def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #??Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])
def check_key():
    if os.path.exists(os.path.join(".",key_dir)) and not os.path.exists(os.path.join(".",key_file_dir)):
        mac = get_mac_address()
        key_file = os.path.join(".",key_file_dir)
        with open(key_file,"w") as w:
            w.write(mac)
        os.chmod(key_file, stat.S_IREAD)
    elif os.path.exists(os.path.join(".",key_dir)) and os.path.exists(os.path.join(".",key_file_dir)):
        mac = get_mac_address()
        key_file = os.path.join(".",key_file_dir)
        with open(key_file,"r") as w:
            mac_read = w.read()
        if mac!=mac_read:
            return False
    else:
        return False
    return True





    sys.exit()

if not check_key():
    sg.popup_timed('无法在其他地方使用哦！',auto_close_duration=5,no_titlebar=False,line_width=50,icon=ico_file)
    sys.exit()

layout = []
layout.append([sg.Text('------广告位------',text_color="green"),sg.Button('call me')])
if ppt_num<=num_per_page:
    for index,ppt in enumerate(ppt_list):
        layout.append([sg.Text(ppt.split(".")[0],size=(max_title_len-10,None),font='None 16 italic'),sg.Button('ppt of '+str(index+1)+"'s",size=(10,None)),sg.Button('video of '+str(index+1)+"'s",size=(10,None))])
else:
    for index in range(ppt_num//2):
        left = [sg.Text(ppt_list[index*2].split(".")[0],size=(max_title_len-10,None),font='None 16 italic'),sg.Button('ppt of '+str(index*2+1)+"'s",size=(10,None)),sg.Button('video of '+str(index*2+1)+"'s",size=(10,None))]
        right = [sg.Text(ppt_list[index*2+1].split(".")[0],size=(max_title_len-10,None),font='None 16 italic'),sg.Button('ppt of '+str(index*2+1+1)+"'s",size=(10,None)),sg.Button('video of '+str(index*2+1+1)+"'s",size=(10,None))]
        layout.append(left+right)
    if ppt_num%2 != 0:
        final = [sg.Text(ppt_list[-1].split(".")[0],size=(max_title_len-10,None),font='None 16 italic'),sg.Button('ppt of '+str(ppt_num)+"'s",size=(10,None)),sg.Button('video of '+str(ppt_num)+"'s",size=(10,None))]
        layout.append(final)

# Create the Window
window = sg.Window("Welcome to teacher Cai's original work", layout,icon=ico_file)#icon
#print(window.get_screen_size())
#window2 = sg.Window('Window 2', [[sg.Text('Some text on Row 2',text_color="green")]])
#window.layout([[sg.Text('Some text on Row 1',text_color="green")]])
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    #event, values = window2.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'ppt1':
        print('what')
        # window.add_row([sg.Text('Some text on Row 2',text_color="green")])
        # window.Hide
        #window.layout([[sg.Text('Some text on Row 2',text_color="green")]])
        #sg.popup('ok')

    #print('You entered ', values[0])

window.close()
