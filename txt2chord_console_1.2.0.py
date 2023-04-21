"""Text to Chord 1.2.0 - Convert text to chords.
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
import os
import io
import math


notes=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
rgb_scale = 255
cmyk_scale = 100
steps=[[0, 1, 3, 4, 6, 8, 10, 0], [0, 1, 3, 5, 6, 8, 10, 0], [0, 1, 3, 5, 7, 8, 10, 0], [0, 1, 3, 5, 7, 9, 10, 0], [0, 2, 3, 5, 6, 8, 10, 0], [0, 2, 3, 5, 7, 8, 10, 0], [0, 2, 3, 5, 7, 9, 10, 0], [0, 2, 3, 5, 7, 9, 11, 0], [0, 2, 4, 5, 7, 8, 10, 0], [0, 2, 4, 5, 7, 9, 10, 0], [0, 2, 4, 5, 7, 9, 11, 0], [0, 2, 4, 6, 7, 9, 10, 0], [0, 2, 4, 6, 7, 9, 11, 0], [0, 2, 4, 6, 8, 9, 11, 0]]
stepsitem=[]
stepscale=[]
stepscales=[]

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
    global text
    global notevalue
    global stepstransposed
    global chordsteps
    global scale
    global scales
    chordsteps=[]
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
    text=''
    notevalue=0
    scale=[]
    scales=[]
    stepstransposed=[]

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

def GenerateChord(text):
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
    global chord
    global rootvalue
    global chordsteps
    numbersum=0
    textvalidate=0
    length=len(text)
    for letters in range (0,length):
        char=text[letters]
        asciicode=ord(char)
        if (asciicode>64 and asciicode<91) or (asciicode>96 and asciicode<123):
            textvalidate=1
    if textvalidate==0:
        text="Hello"
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
    root=notes[rootvalue-1]
    chord.append(root)
    chordsteps.append(rootvalue-1)
    notevalue=rootvalue-1
    #print (notevalue,root)
        
    for value in cmyk:
        try:
            interval=int(value/16.66)+3
        except:
            interval=3
        notevalue=notevalue+interval
        if notevalue>11:
            notevalue=notevalue-11
        chord.append(notes[notevalue])
        chordsteps.append(notevalue)
    chorddisplay=''
    for item in chord:
        chorddisplay= chorddisplay+item+" "
    print ("\n")
    print ("Chord n. 1: ",chorddisplay)
    guess_scale()
    init()


#algorithm 2
    blue=0
    red=0
    green=0
    numbersum=0
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
    root=notes[rootvalue-1]
    chord.append(root)
    chordsteps.append(rootvalue-1)
    notevalue=rootvalue-1        
        
    for value in cmyk:
        try:
            interval=int(value/16.66)+3
        except:
            interval=3
        notevalue=notevalue+interval
        if notevalue>11:
            notevalue=notevalue-11
        chord.append(notes[notevalue])
        chordsteps.append(notevalue)
    chorddisplay=''
    for item in chord:
        chorddisplay= chorddisplay+item+" "
    print ("\n")
    print ("Chord n. 2: ",chorddisplay)
    guess_scale()
    init()
    
#algorithm 3

    blue=0
    red=0
    green=0
    numbersum=0
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
    root=notes[rootvalue-1]
    chord.append(root)
    chordsteps.append(rootvalue-1)
    notevalue=rootvalue-1        
        
    for value in cmyk:
        try:
            interval=int(value/16.66)+3
        except:
            interval=3
        notevalue=notevalue+interval
        if notevalue>11:
            notevalue=notevalue-11
        chord.append(notes[notevalue])
        chordsteps.append(notevalue)
    chorddisplay=''
    for item in chord:
        chorddisplay= chorddisplay+item+" "
    print ("\n")
    print ("Chord n. 3: ",chorddisplay)
    guess_scale()
    init()

def guess_scale():
    global match
    global matchlist
    global scale
    global scales
    global stepstransposed
    global stepsitem
    global root
    global stepscale
    global stepscales
    global chord
    global rootvalue
    global scale
    global chordsteps
    match=0
    matchlist=[]
    stepscale=[]
    stepscales=[]
    chordlen=len(chordsteps)
    stepslen=len(steps)
    for n in range (0, stepslen):
        for m in range (0,7):
            transpose=steps[n][m]+(rootvalue-1)
            if transpose>11:
                transpose=transpose-12
            stepsitem.append(transpose)
            transpose=0
        stepstransposed.append(stepsitem)
        stepsitem=[]
    #print (stepstransposed)
    #print ("chordsteps ", chordsteps)
    for n in range (0, stepslen):
        for m in range (0,7):
            for o in range (0,chordlen):
                #print (chordsteps[o],steps[n][m])
                if chordsteps[o]==stepstransposed[n][m]:
                    match=match+1
                    
        matchlist.append(match)
        match=0
    #print (matchlist)


    for n in range (0,stepslen):
        if matchlist[n]==max(matchlist):
            #print (steps[n])
            #print (stepstransposed[n])
            for x in range (0,7):
                noteindex=stepstransposed[n][x]
                scalenote=notes[noteindex]
                scale.append(scalenote)
                stepscale.append(noteindex)
        if scale!=[]:
            scales.append(scale)
            stepscales.append(stepscale)
        scale=[]
        stepscale=[]
    scalestring=''
    print ("\n")
    print ("Scales:")
    guess=1
    for item in scales:
        for note in item:
            scalestring=scalestring+note+" "
        print ("Match",str(guess)+": ",scalestring)
        guess=guess+1
        scalestring=''
    guess=0
    print ("\n")


#main
def main():
    global text
    init()
    while text!="q":
        text=input("Input text (q to quit): ")
        if text!='' and text!="q":
            GenerateChord(text)

main()
