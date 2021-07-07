from tkinter.ttk import Scrollbar
import PySimpleGUI as sg
import os
from PySimpleGUI.PySimpleGUI import FolderBrowse, HorizontalSeparator
from natsort import natsorted
sg.theme('DarkAmber')   # Add a touch of color
import tkinter as tk

def_value  = 0
col1_width = 480
col2_width = 480

col1_height = 480
col2_height = 480

input_height = 50
input_width = col1_width
def global_counter_both(val):
    global def_value   
    if val == "Next":
        def_value  += 1
    elif val == "Previous":
       def_value  -= 1

def get_screen_resolution():
    screen_height = 900
    screen_width = 1024
    return screen_height, screen_width

def update_img_win(folder_path:str,window_name:str):
    fnames=[]
    if os.path.exists(folder_path):
        try:
            img_list = os.listdir(folder_path)
        except:
            img_list = []
        fnames = []
        for f in range(0,len(img_list)):
            if img_list[f].split('.')[-1] in ["png",]: #supports only png
                fnames.append(os.path.join(folder_path,img_list[f]))
        fnames = natsorted(fnames)
        if len(fnames)>0:
            window_name.update(fnames[def_value])
    return fnames

def update_nxt_prev_btn(window_name:str):
    global f1_len
    global f2_len 
    if (f1_len == f2_len) & (f1_len>0):
        window['Previous'].update(disabled=False)
        window['Next'].update(disabled=False)
        window["TOTAL-IMGS"].update(f" {def_value+1}/ "+str(f1_len),text_color="green")

def win_update(fnames1,fnames2,def_value:int):
    window["-IMAGE1-"].update(fnames1[def_value])
    window["-IMAGE2-"].update(fnames2[def_value])










height,width = get_screen_resolution()



img_folder1 = [
    [
        # sg.Text("Browse"),
        sg.In(size=(55,2),enable_events=True,key="-FOLDER1-"),
        sg.FolderBrowse(),
    ]
] 

img_folder2 = [
    [
        # sg.Text("Browse"),
        sg.In(size=(55,2),enable_events=True,key="-FOLDER2-"),
        sg.FolderBrowse(),
    ]
] 


preview_img1 = [
    [
      sg.Image(key="-IMAGE1-",size=(1024,1024))  
    ]
]


preview_img2 = [
    [
      sg.Image(key="-IMAGE2-",size=(1024,1024))  
    ]
]


# All the stuff inside your window.
layout = [  
    
    [
        sg.Column(img_folder1,size=(input_width,input_height)),
        
        sg.Column(img_folder2,size=(input_width,input_height)),

        
    ],


    [
        sg.Column(preview_img1,scrollable=True,size=(col1_width,col1_height)),
        
        sg.Column(preview_img2,scrollable=True, size=(col2_width,col2_height)),
    ],
    
    [
        sg.Column([
            [sg.Text(size=(50,1),key="warning_text"),]
            
        ]),

        sg.Column([
            [sg.Text(size=(50,1),key="TOTAL-IMGS"),]
            
        ])
       
    ],

    [
        sg.Button('Previous' ,enable_events=True,disabled=True),
        sg.Button('Next',enable_events=True,disabled=True)
    ],
    
    [
        sg.Button('Quit',target=(0,-1))
    ]
    
   
]


# /home/nabu/Desktop/aug_img



f1_len = 0
f2_len = 0


# Create the Window
window = sg.Window('Preview Images', layout, size =(1024,700),location=(5,5),finalize=True,auto_size_buttons=True,)
window.Maximize()
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Quit': # if user closes window or clicks cancel
        values["-FOLDER2-"] = ""
        values["-FOLDER1-"] = ""
        break
    # pick filenames from first
    elif event == "-FOLDER1-" :
        fnames1 = update_img_win(values["-FOLDER1-"],window["-IMAGE1-"])
        f1_len = len(fnames1)
        update_nxt_prev_btn(window["-IMAGE1-"])
        

    #pick filenames from second
    elif event == "-FOLDER2-" :
        fnames2 = update_img_win(values["-FOLDER2-"],window["-IMAGE2-"])
        f2_len = len(fnames2)
        update_nxt_prev_btn(window["-IMAGE2-"])
        
        
    elif event == "Previous":
        if os.path.exists(values["-FOLDER1-"]) & os.path.exists(values["-FOLDER2-"]) & (f1_len>0) & (f2_len>0):
            global_counter_both("Previous")
            if def_value>=0:
                win_update(fnames1,fnames2,def_value)
                
            elif def_value <0:
                def_value = (len(fnames1)-1)
                win_update(fnames1,fnames2,def_value)
            window["warning_text"].update("",text_color="red")
            
        else:
            txt = "Please select a folder which contains images."
            window["warning_text"].update(txt,text_color="red")
        window["TOTAL-IMGS"].update(f" {def_value+1}/ "+str(len(fnames2)),text_color="green")

    elif event == "Next":
        
        if os.path.exists(values["-FOLDER1-"]) & os.path.exists(values["-FOLDER2-"]) & (f1_len>0) & (f2_len>0):
            global_counter_both("Next")
            if def_value<len(fnames1):
                win_update(fnames1,fnames2,def_value)
                
            elif def_value == len(fnames1):
                def_value =0
                win_update(fnames1,fnames2,def_value)
                    

            window["warning_text"].update("",text_color="red")   
        else:
            print("Next button failed")
            txt = "Please select a folder which contains images."
            window["warning_text"].update(txt,text_color="red")
        
        window["TOTAL-IMGS"].update(f" {def_value+1}/ "+str(len(fnames2)),text_color="green")

window.close()