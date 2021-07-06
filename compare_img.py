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

def get_screen_resolution():
    screen_height = 900
    screen_width = 1024
    return screen_height, screen_width




def global_counter_both(val):
    global def_value
    print(def_value)
    if val == "next":
        def_value  += 1
    elif val == "prev":
       def_value  -= 1






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
        if os.path.exists(values["-FOLDER1-"]):
            folder_pth1 = values["-FOLDER1-"]

            try:
                img_list1 = os.listdir(folder_pth1)
            except:
                img_list1 = []
            
            fnames1 = []
            for f in range(0,len(img_list1)):
                if img_list1[f].split('.')[-1] in ["png",]: #supports only png
                    fnames1.append(os.path.join(folder_pth1,img_list1[f]))
            fnames1 = natsorted(fnames1)
            
            if len(fnames1)>0:
                

                window["-IMAGE1-"].update(fnames1[def_value])

    #pick filenames from second
    elif event == "-FOLDER2-" :
        if os.path.exists(values["-FOLDER2-"]):

            folder_pth2 = values["-FOLDER2-"]
            try:
                img_list2 = os.listdir(folder_pth2)
            except:
                img_list2 = []
            
            fnames2 = []
            print("length",len(img_list2))
            for f in range(0,len(img_list2)):
                if img_list2[f].split('.')[-1] in ["png",]:
                    fnames2.append(os.path.join(folder_pth2,img_list2[f]))
            fnames2 = natsorted(fnames2)

            if len(fnames2)>0:
                window['Previous'].update(disabled=False)
                window['Next'].update(disabled=False)
                window["-IMAGE2-"].update(fnames2[def_value])
                window["TOTAL-IMGS"].update("Total No. of Images: "+str(len(fnames2))+f" Current Number :{def_value} ",text_color="green")
        
    elif event == "Previous":
        print(os.path.exists(values["-FOLDER1-"]))
        print(os.path.exists(values["-FOLDER2-"]))
        print("len1",len(fnames1)>0)
        print("len",len(fnames2)>0)
        # print(T)
        if os.path.exists(values["-FOLDER1-"]) & os.path.exists(values["-FOLDER2-"]) & len(fnames1)>0 & len(fnames2)>0:
            print("Passs")
            global_counter_both("prev")
            if def_value>=0:
                # print(def_value)
                window["-IMAGE1-"].update(fnames1[def_value])
                window["-IMAGE2-"].update(fnames2[def_value])
            elif def_value <0:
                def_value = (len(fnames1)-1)
                window["-IMAGE1-"].update(fnames1[def_value])
                window["-IMAGE2-"].update(fnames2[def_value])

        else:
            txt = "Please select a folder which contains images."
            window["warning_text"].update(txt,text_color="red")

    elif event == "Next":

        if os.path.exists(values["-FOLDER1-"]) & os.path.exists(values["-FOLDER2-"]) & len(fnames1)>0 & len(fnames2)>0:
            global_counter_both("next")
            if def_value<len(fnames1):
                window["-IMAGE1-"].update(fnames1[def_value])
                window["-IMAGE2-"].update(fnames2[def_value])
            elif def_value == len(fnames1):
                    def_value =0
                    window["-IMAGE1-"].update(fnames1[def_value])
                    window["-IMAGE2-"].update(fnames2[def_value])
        else:
            txt = "Please select a folder which contains images."
            window["warning_text"].update(txt,text_color="red")

window.close()