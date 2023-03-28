"""Text to Chord 1.1.0 - Convert text to chords.
Copyright (C) 2023  Fonazza-Stent

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""


import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import *
import os
import io
import pyperclip
import math
from tkinter import messagebox

#init
def init():
    global c
    global rc
    global bc
    global gc
    global blue
    global red
    global green
    global lettern
    global numbersum
    global redsum
    global greensum
    global bluesum
    global redlength
    global greenlength
    global bluelength
    global notes
    global rgb_scale
    global cmyk_scale
    c=9.84
    rc=28.44
    bc=23.27
    gc=42.5
    blue=0
    red=0
    green=0
    lettern=1
    numbersum=0
    redsum=0
    greensum=0
    bluesum=0
    redlength=0
    greenlength=0
    bluelength=0
    notes=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    rgb_scale = 255
    cmyk_scale = 100

def rgb_to_cmyk(r,g,b):
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / float(rgb_scale)
    m = 1 - g / float(rgb_scale)
    y = 1 - b / float(rgb_scale)

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) 
    m = (m - min_cmy) 
    y = (y - min_cmy) 
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    cmyk=[ int(c*cmyk_scale), int(m*cmyk_scale), int(y*cmyk_scale), int(k*cmyk_scale)]
    return cmyk
    
#Create app window
def create_app_window():
    global top
    global root
    img=b'iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAAxHpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjabVBbDsMgDPvPKXYEEqc8jkPXTtoNdvwFAlOZaimOIWBC6Py8X/RoEFbSLeVYYgwGLVqkmsjBUTtz0M4TPHjZp58Uy7AML+Q4bs19XmwCV1PbxSg/R2FfC0U9S/4zEk9oHTV9DKMyjCBe4GFQ/VshlpyuX9jPsCJ7UCOuXPqMMNte15psesdm70DkBCMYA+oNoAUI1QSMBckOMrTraMyYndhA7uY0QV8L2Vl3OGnLvAAAAYRpQ0NQSUNDIHByb2ZpbGUAAHicfZE9SMNAHMVfU6UqFQc7iDpkqE52sSKOpYpFsFDaCq06mFz6BU0akhQXR8G14ODHYtXBxVlXB1dBEPwAcXVxUnSREv+XFFrEeHDcj3f3HnfvAKFZZarZEwNUzTLSibiYy6+KgVf4MYYg+hGVmKknM4tZeI6ve/j4ehfhWd7n/hyDSsFkgE8kjjHdsIg3iGc3LZ3zPnGIlSWF+Jx4yqALEj9yXXb5jXPJYYFnhoxsep44RCyWuljuYlY2VOIZ4rCiapQv5FxWOG9xVqt11r4nf2GwoK1kuE5zHAksIYkURMioo4IqLERo1Ugxkab9uId/1PGnyCWTqwJGjgXUoEJy/OB/8LtbsxiddpOCcaD3xbY/JoDALtBq2Pb3sW23TgD/M3Cldfy1JjD3SXqjo4WPgKFt4OK6o8l7wOUOMPKkS4bkSH6aQrEIvJ/RN+WB4VtgYM3trb2P0wcgS10t3wAHh8BkibLXPd7d193bv2fa/f0Auf9yw7XjgYwAAA12aVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+CiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiCiAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICB4bWxuczpHSU1QPSJodHRwOi8vd3d3LmdpbXAub3JnL3htcC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOjQ3Y2JkYTEwLTMwMjQtNDJjYi04ODEwLWZiZmE2M2VkYTAzNCIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo5YTg5OTU3NS01MDMwLTQ3NTktYWE5NC0zYmUyZjI3ZmM3MzYiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDozMmUwOWYyZC0xMTQ2LTQ3NzktYThhNC1jZmI0NGRjNWEzNmMiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3JtPSJXaW5kb3dzIgogICBHSU1QOlRpbWVTdGFtcD0iMTY3OTkxOTk3NDYzODg3NCIKICAgR0lNUDpWZXJzaW9uPSIyLjEwLjM0IgogICB0aWZmOk9yaWVudGF0aW9uPSIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCIKICAgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMzowMzoyN1QxNDoyNjoxNCswMjowMCIKICAgeG1wOk1vZGlmeURhdGU9IjIwMjM6MDM6MjdUMTQ6MjY6MTQrMDI6MDAiPgogICA8eG1wTU06SGlzdG9yeT4KICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo1MGE4NmM5Ni01Zjc1LTQyODAtYTUzMi1kMjU3ZmJhZGQzNzEiCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoV2luZG93cykiCiAgICAgIHN0RXZ0OndoZW49IjIwMjMtMDMtMjdUMTQ6MjY6MTQiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+DecNIAAAAAZiS0dEAP8AAAAAMyd88wAAAAlwSFlzAAAOwAAADsABataJCQAAAAd0SU1FB+cDGwwaDlmiBWwAACAASURBVHja7X07jKTrUXbN9P1+n9mLZdkIybLAQjKHCIHsAAkiBCJDQHASEIhLYGGnEBA4OQRAQmCLAAIjLolFAogEWQSAxJEtHYx89uxlZvp+ne6e7p4/4H9enq/m/S4907M7e06V9Gl2Z2e6++vtet6qp6qeOrq+vr4WMzOzT6Qd21tgZmYAYGZmZgBgZmZmAGBmZmYAYGZmZgBgZmZmAGBmZmYAYGZmZgBgZmZmAGBmZmYAYGZmZgBgZmZmAGBmZmYAYGZmZgBgZmZmAGBmZmYAYGZmZgBgZmZmAGBmZmYAYGZmZgBgZmZmAGBmZmYAYGZmZgBgZmZmAGBmZmYAYGZmZgBgZmZmAGBmZmYAYGZmZgBgZma2p6XtLTC7vr6WfbfE65+PeoyjoyPvV34c/l3+97CfCXsO3+9E/b7vNYX9Oep34t6jsPcL3z86OgpcSR4/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'

    root= tk.Tk()
    top= root
    #top.geometry("588x409+428+131")
    top.geometry("600x410")
    top.resizable(0,0)
    top.title("Text to Chord")
    favicon=tk.PhotoImage(data=img) 
    root.wm_iconphoto(True, favicon)

#Textbox
def create_textbox():
    global textbox
    textbox = Text(top)
    textbox.place(x=20, y=20, height=340, width=400)
    scroll_1=Scrollbar (top)
    scroll_1.place(x=421, y=20, height=340, anchor='n')
    textbox.configure(yscrollcommand=scroll_1.set)
    scroll_1.configure(command=textbox.yview)
    textbox.focus_set()
    textbox.bind("<Button-3>", context_menu)



#ChordDisplay
def chord_display():
    global chord_one
    chord_one_label=Label(top)
    chord_one_label.place(x=450,y=20,height=30,width=100)
    chord_one_label.configure(text="Chord n. 1")
    chord_one=Text(top)
    chord_one.place(x=450,y=60,height=30,width=120)
    chord_one.configure(state='disabled')
    global chord_two
    chord_two_label=Label(top)
    chord_two_label.place(x=450,y=120,height=30,width=100)
    chord_two_label.configure(text="Chord n. 2")
    chord_two=Text(top)
    chord_two.place(x=450,y=170,height=30,width=120)
    chord_two.configure(state='disabled')
    global chord_three
    chord_three_label=Label(top)
    chord_three_label.place(x=450,y=230,height=30,width=100)
    chord_three_label.configure(text="Chord n. 3")
    chord_three=Text(top)
    chord_three.place(x=450,y=280,height=30,width=120)
    chord_three.configure(state='disabled')



#Create menu
def create_menu():
    global menubar
    global sub_menu
    menubar=tk.Menu(top, tearoff=0)
    top.configure(menu=menubar)
    sub_menu=tk.Menu(top, tearoff=0)
    menubar.add_cascade(menu=sub_menu,compound="left", label="File")
    sub_menu.add_command(compound="left", label="Paste", command=paste, accelerator="Alt+P")
    sub_menu.add_command(compound="left",label="Clear", command=ClearTextBox, accelerator="Alt+C")
    sub_menu.add_command(compound="left",label="Generate Chord", command=GenerateChord,accelerator="Alt+G")
    sub_menu.add_command(compound="left",label="Quit", command=QuitApp, accelerator="Alt+Q")
    top.bind_all("<Alt-p>",paste_hotkey)
    top.bind_all("<Alt-c>",ClearTextBox_hotkey)
    top.bind_all("<Alt-g>",GenerateChord_hotkey)
    top.bind_all("<Alt-q>",Quit_hotkey)
    menubar.bind_all("<Alt-f>",menubar.invoke(1))


#PasteMenu
def paste_text():
    textbox
    textbox.event_generate(("<<Paste>>"))

def context_menu(event):
    menu = Menu(root, tearoff = 0)
    menu.add_command(label="Paste", command=paste_text)
    try: 
        menu.tk_popup(event.x_root, event.y_root)
    finally: 
        menu.grab_release()


#GenerateColor

def sine(value, letternumber):
    global blue
    blue=blue+value
    global bluelength
    bluelength=bluelength+1
    global bluesum
    bluesum=bluesum+letternumber

def triangle (value, letternumber):
    global red
    red=red+value
    global redlength
    redlength=redlength+1
    global redsum
    redsum=redsum+letternumber

def square (value, letternumber):
    global green
    green=green+value
    global greenlength
    greenlength= greenlength+1
    global greensum
    greensum=greensum+letternumber

def sine2(value, letternumber):
    global blue
    blue=blue+value
    global lettern
    lettern=letternumber
    global numbersum
    numbersum=numbersum+lettern

def triangle2 (value, letternumber):
    global red
    red=red+value
    global lettern
    lettern=letternumber
    global numbersum
    numbersum=numbersum+lettern    

def square2 (value, letternumber):
    global green
    green=green+value
    global lettern
    lettern=letternumber
    global numbersum
    numbersum=numbersum+lettern

    
def rgb_hack(rgb):
    return "#%02x%02x%02x" % rgb

def GenerateChord():
    global blue
    blue=0
    global red
    red=0
    global green
    green=0
    global numbersum
    global redsum
    global redlength
    global greensum
    global greenlength
    global bluesum
    global bluelength
    numbersum=0
    text=textbox.get(1.0,END)
    textvalidate=0
    length=len(text)-1
    for letters in range (0,length):
        char=text[letters]
        asciicode=ord(char)
        if (asciicode>64 and asciicode<91) or (asciicode>96 and asciicode<123):
            textvalidate=1
    if textvalidate==0:
        text="Hello"
    length=len(text)-1
    for letters in range (0,length):
        char=text[letters]
        asciicode=ord(char)
        if (asciicode>64 and asciicode<91) or (asciicode>96 and asciicode<123):
            if char=="A" or char=="a":
                triangle(int(1*rc), 1)
            if char=="B" or char=="b":
                sine (int(1*bc), 1)
            if char=="C" or char=="c":
                sine(int(2*bc), 2)
            if char=="D" or char=="d":
                sine(int(3*bc),3)
            if char=="E" or char=="e":
                square(int(1*gc),1)
            if char=="F" or char=="f":
                square(int(2*gc),2)
            if char=="G" or char=="g":
                sine(int(4*bc),4)
            if char=="H" or char=="h":
                square(int(3*gc),3)
            if char=="i" or char=="I":
                square(int(4*gc),4)
            if char=="J" or char=="j":
                sine(int(5*bc),5)
            if char=="K" or char=="k":
                triangle(int(2*rc),2)
            if char=="L" or char=="l":
                square(int(5*gc),5)
            if char=="M" or char=="m":
                triangle(int(3*rc),3)
            if char=="N" or char=="n":
                triangle(int(4*rc),4)
            if char=="O" or char=="o":
                sine(int(6*bc),6)
            if char=="P" or char=="p":
                sine(int(7*bc),7)
            if char=="Q" or char=="q":
                sine(int(8*bc),8)
            if char=="R" or char=="r":
                sine(int(9*bc),9)
            if char=="S" or char=="s":
                sine(int(10*bc),10)
            if char=="T" or char=="t":
                square(int(6*gc),6)
            if char=="U" or char=="u":
                sine(int(11*bc),11)
            if char=="V" or char=="v":
                triangle(int(5*rc),5)
            if char=="W" or char=="w":
                triangle(int(6*rc),6)
            if char=="X" or char=="x":
                triangle(int(7*rc),7)
            if char=="Y" or char=="y":
                triangle(int(8*rc),8)
            if char=="Z" or char=="z":
                triangle(int(9*rc),9)
    if bluelength>0:
        blue=int(blue/bluelength)
        bluevalue=int(blue*bluelength)
    else:
        blue=0
        bluevalue=0
    if redlength>0:
        red=int(red/redlength)
        redvalue=int(red*redlength)
    else:
        red=0
        redvalue=0
    if greenlength>0:
        green=int(green/greenlength)
        greenvalue=int(green*greenlength)
    else:
        green=0
        greenvalue=0
    RGB=[redvalue,greenvalue,bluevalue]
    RGB2=[red,green,blue]
    maxvalue=max(RGB)
    maxvalue2=max(RGB2)
    R=int(maxvalue2/maxvalue*redvalue)
    G=int(maxvalue2/maxvalue*greenvalue)
    B=int(maxvalue2/maxvalue*bluevalue)
    cmyk=rgb_to_cmyk(R,G,B)
    chord=[]
    rootvalue=0
    for chars in text:
        rootvalue=rootvalue+1
        if rootvalue>11:
            rootvalue=0
    root=notes[rootvalue]
    chord.append(root)
    notevalue=rootvalue        
        
    for value in cmyk:
        try:
            interval=int(value/16.66)+3
        except:
            interval=3
        notevalue=notevalue+interval
        if notevalue>11:
            notevalue=notevalue-11
        chord.append(notes[notevalue])
    chord_one.configure(state='normal')
    chord_one.delete(1.0,END)
    chord_one.insert(INSERT,chord)
    chord_one.configure(state='disabled')
    notevalue=0


#algorithm 2
    blue=0
    red=0
    green=0
    numbersum=0
    text=textbox.get(1.0,2000.0)
    textvalidate=0
    length=len(text)-1
    for letters in range (0,length):
        char=text[letters]
        asciicode=ord(char)
        if (asciicode>64 and asciicode<91) or (asciicode>96 and asciicode<123):
            textvalidate=1
    if textvalidate==0:
        text="Hello"
    length=len(text)
    for letters in range (0,length):
        char=text[letters]
        asciicode=ord(char)
        if (asciicode>64 and asciicode<91) or (asciicode>96 and asciicode<123):
            if char=="A" or char=="a":
                triangle2(int(1*rc), 1)
            if char=="B" or char=="b":
                sine2 (int(1*bc), 1)
            if char=="C" or char=="c":
                sine2(int(2*bc), 2)
            if char=="D" or char=="d":
                sine2(int(3*bc),3)
            if char=="E" or char=="e":
                square2(int(1*gc),1)
            if char=="F" or char=="f":
                square2(int(2*gc),2)
            if char=="G" or char=="g":
                sine2(int(4*bc),4)
            if char=="H" or char=="h":
                square2(int(3*gc),3)
            if char=="i" or char=="I":
                square2(int(4*gc),4)
            if char=="J" or char=="j":
                sine2(int(5*bc),5)
            if char=="K" or char=="k":
                triangle2(int(2*rc),2)
            if char=="L" or char=="l":
                square2(int(5*gc),5)
            if char=="M" or char=="m":
                triangle2(int(3*rc),3)
            if char=="N" or char=="n":
                triangle2(int(4*rc),4)
            if char=="O" or char=="o":
                sine2(int(6*bc),6)
            if char=="P" or char=="p":
                sine2(int(7*bc),7)
            if char=="Q" or char=="q":
                sine2(int(8*bc),8)
            if char=="R" or char=="r":
                sine2(int(9*bc),9)
            if char=="S" or char=="s":
                sine2(int(10*bc),10)
            if char=="T" or char=="t":
                square2(int(5*gc),6)
            if char=="U" or char=="u":
                sine2(int(11*bc),11)
            if char=="V" or char=="v":
                triangle2(int(5*rc),5)
            if char=="W" or char=="w":
                triangle2(int(6*rc),6)
            if char=="X" or char=="x":
                triangle2(int(7*rc),7)
            if char=="Y" or char=="y":
                triangle2(int(8*rc),8)
            if char=="Z" or char=="z":
                triangle2(int(9*rc),9)
    if bluelength>0:
        blue=int(blue/bluelength)
        blue=int(blue*bluelength)
    else:
        blue=0
    if redlength>0:
        red=int(red/redlength)
        red=int(red*redlength)
    else:
        red=0
    if greenlength>0:
        green=int(green/greenlength)
        green=int(green*greenlength)
    else:
        green=0
    RGB=[red,green,blue]
    maxvalue=max(RGB)
    if red>0:
        R=int(255/maxvalue*red)
    else:
        R=0
    if green>0:
        G=int(255/maxvalue*green)
    else:
        G=0
    if blue>0:
        B=int(255/maxvalue*blue)
    else:
        B=0
    maxredlightness=redlength*9
    maxgreenlightness=greenlength*6
    maxbluelightness=bluelength*11
    if maxredlightness>0:
        redlightness=int(100*redsum/maxredlightness)
    else:
        redlightness=0
    if maxgreenlightness>0:
        greenlightness=int(100*greensum/maxgreenlightness)
    else:
        greenlightness=0
    if maxbluelightness>0:
        bluelightness=int(100*bluesum/maxbluelightness)
    else:
        bluelightness=0
    redvalue=int(redlightness*R/100)
    greenvalue=int(greenlightness*G/100)
    bluevalue=int(bluelightness*B/100)
    cmyk=rgb_to_cmyk(R,G,B)
    chord=[]
    rootvalue=0
    for chars in text:
        rootvalue=rootvalue+1
        if rootvalue>11:
            rootvalue=0
    root=notes[rootvalue]
    chord.append(root)
    notevalue=rootvalue        
        
    for value in cmyk:
        try:
            interval=int(value/16.66)+3
        except:
            interval=3
        notevalue=notevalue+interval
        if notevalue>11:
            notevalue=notevalue-11
        chord.append(notes[notevalue])
    chord_two.configure(state='normal')
    chord_two.delete(1.0,END)
    chord_two.insert(INSERT,chord)
    chord_two.configure(state='disabled')
    notevalue=0

#algorithm 3

    blue=0
    red=0
    green=0
    numbersum=0
    text=textbox.get(1.0,2000.0)
    textvalidate=0
    length=len(text)
    for letters in range (0,length):
        char=text[letters]
        asciicode=ord(char)
        if (asciicode>64 and asciicode<91) or (asciicode>96 and asciicode<123):
            textvalidate=1
    if textvalidate==0:
        text="Hello"
    length=len(text)
    for letters in range (0,length):
        char=text[letters]
        asciicode=ord(char)
        if (asciicode>64 and asciicode<91) or (asciicode>96 and asciicode<123):
            if char=="A" or char=="a":
                triangle(int(1*rc), 1)
            if char=="B" or char=="b":
                sine (int(1*bc), 2)
            if char=="C" or char=="c":
                sine(int(2*bc), 3)
            if char=="D" or char=="d":
                sine(int(3*bc),4)
            if char=="E" or char=="e":
                square(int(1*gc),5)
            if char=="F" or char=="f":
                square(int(2*gc),6)
            if char=="G" or char=="g":
                sine(int(4*bc),7)
            if char=="H" or char=="h":
                square(int(3*gc),8)
            if char=="i" or char=="I":
                square(int(4*gc),9)
            if char=="J" or char=="j":
                sine(int(5*bc),10)
            if char=="K" or char=="k":
                triangle(int(2*rc),11)
            if char=="L" or char=="l":
                square(int(5*gc),12)
            if char=="M" or char=="m":
                triangle(int(3*rc),13)
            if char=="N" or char=="n":
                triangle(int(4*rc),14)
            if char=="O" or char=="o":
                sine(int(6*bc),15)
            if char=="P" or char=="p":
                sine(int(7*bc),16)
            if char=="Q" or char=="q":
                sine(int(8*bc),17)
            if char=="R" or char=="r":
                sine(int(9*bc),18)
            if char=="S" or char=="s":
                sine(int(10*bc),19)
            if char=="T" or char=="t":
                square(int(5*gc),20)
            if char=="U" or char=="u":
                sine(int(11*bc),21)
            if char=="V" or char=="v":
                triangle(int(5*rc),22)
            if char=="W" or char=="w":
                triangle(int(6*rc),23)
            if char=="X" or char=="x":
                triangle(int(7*rc),24)
            if char=="Y" or char=="y":
                triangle(int(8*rc),25)
            if char=="Z" or char=="z":
                triangle(int(9*rc),26)

    if bluelength>0:
        blue=int(blue/bluelength)
        blue=int(blue*bluelength)
    else:
        blue=0
    if redlength>0:
        red=int(red/redlength)
        red=int(red*redlength)
    else:
        red=0
    if greenlength>0:
        green=int(green/greenlength)
        green=int(green*greenlength)
    else:
        green=0
    RGB=[red,green,blue]
    maxvalue=max(RGB)
    R=int(255/maxvalue*red)
    G=int(255/maxvalue*green)
    B=int(255/maxvalue*blue)
    cmyk=rgb_to_cmyk(R,G,B)
    chord=[]
    rootvalue=0
    for chars in text:
        rootvalue=rootvalue+1
        if rootvalue>11:
            rootvalue=0
    root=notes[rootvalue]
    chord.append(root)
    notevalue=rootvalue        
        
    for value in cmyk:
        try:
            interval=int(value/16.66)+3
        except:
            interval=3
        notevalue=notevalue+interval
        if notevalue>11:
            notevalue=notevalue-11
        chord.append(notes[notevalue])
    chord_three.configure(state='normal')
    chord_three.delete(1.0,END)
    chord_three.insert(INSERT,chord)
    chord_three.configure(state='disabled')
    notevalue=0

#Generate color hotkey
def GenerateChord_hotkey(event):
    GenerateChord()

#Paste From Button
def paste():
        textbox.event_generate(("<<Paste>>"))

#paste hotkey
def paste_hotkey(event):
    paste()

#Clear
def ClearTextBox():
    textbox.delete(1.0,2000.0)

def ClearTextBox_hotkey(event):
    ClearTextBox()

#Quit
def QuitApp():
    okcancel= messagebox.askokcancel("Quit?","Do you want to quit the app?",default="ok")
    if okcancel== True:
        top.destroy()

def Quit_hotkey (event):
    QuitApp()


        
#main
def main():
    init()
    create_app_window()
    create_textbox()
    chord_display()
    create_menu()

main()
root.mainloop()
