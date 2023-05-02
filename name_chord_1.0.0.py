notes=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
note=''


def name_chord():
    note=''
    chord=[]
    while note !=str(0):
        note=input("Input note (0 to end chord, q to quit): ")
        if note=="q":
            quit()
        for item in notes:
            if note==item:
                chord.append(note)
                chordstring=''
                for n in chord:
                    chordstring=chordstring+n+" "
                print ("Chord so far: ",chordstring)
                print ("\n")
        
    chordname=[]
    chordname_string=""

    chord_notes=[]


    chord_length=len(chord)
    chordname_string=''
    for n in range (0,12):
        if chord[0]==notes[n]:
            index=n
            for i in range (0,12):
                chord_notes.append(notes[index])
                index=index+1
                if index>11:
                    index=0

    chordname.append(chord[0])

    sus=False
    sus_index=999
    ninth=False
    ninth_index=999
    seventh_maj=False
    seventh_maj_index=999
    seventh=False
    seventh_index=999
    sixth=False
    sixth_index=999
    eleventh=False
    eleventh_index=999
    ninth_maj=False
    ninth_maj_index=999
    thirteenth=False
    maj=False
    minr=False
    plusninth=False
    mincheck=False
    bfive=False
    fifth=False
    dim=False
    aug=False
    add_fifth=False
    minr_index=999
    for n in range (1,chord_length):
        step=chord_notes.index(chord[n])+1
        #print (step)
        if step==5:
            maj=True
            minr=False
        if step==4:
            minr=True
            maj=False
        if maj==True and minr==True and plusninth==False:
            plusninth=True
            minr=False
            chordname.append(" 9+")
            plusninth_index=len(chordname)
        elif minr==True and mincheck==False:
            chordname.append("m ")
            minr_index=len(chordname)
            mincheck=True
        if step==8:
            fifth=True

    for n in range (1,chord_length):
        step=chord_notes.index(chord[n])+1
        if step==6 and sus==False:
            sus=True
            chordname.append(" Sus")
            sus_index=len(chordname)
        if minr==True and step==7 and dim==False and fifth==False:
            dim=True
            chordname.append(" Dim")
            dim_index=len(chordname)
            if minr_index!=999:
                chordname[minr_index-1]='delete'
        if dim==False and step==7 and bfive==False:
            bfive=True
            chordname.append(" Add5b")
            bfive_index=len(chordname)
        if step==9 and fifth==False and aug==False:
            aug=True
            chordname.append(" Aug")
            aug_index=len(chordname)-1
        if step==9 and fifth==True and add_fifth==False:
            add_fifth_plus=True
            chordname.append(" Add5+")
            add_fifth_plus_index=len(chordname)
        if step==10:
            sixth=True
            chordname.append(" 6")
            sixth_index=len(chordname)
        if step==11:
            seventh=True
            chordname.append(" 7")
            seventh_index=len(chordname)

        if step==12:
            seventh_maj=True
            chordname.append(" 7maj")
            seventh_maj_index=len(chordname)
        if step==3 and seventh==True:
            ninth=True
            chordname.append(" 9")
            ninth_index=len(chordname)
            if seventh_index!=999: 
                chordname[seventh_index-1]='delete'
        if step==3 and sus==False and seventh_maj==True:
            ninth_maj=True
            chordname.append(" 9maj")
            ninth_maj_index=len(chordname)
            if seventh_maj_index!=999:
                chordname[seventh_maj_index-1]='delete'
        if step==3 and seventh_maj==False and seventh==False:
            add_ninth=True
            chordname.append(" Add9")
            ninth_maj_index=len(chordname)
            if seventh_maj_index!=999:
                chordname[seventh_maj_index-1]='delete'        
        if step==2:
            ninthb=True
            chordname.append(" Add9b")
            ninthb_index=len(chordname)
        if ninth==True and sus==True and sixth==False and(seventh==True or seventh_maj==True):
            eleventh=True
            chordname.append(" 11")
            eleventh_index=len(chordname)

            chordname[ninth_index-1]='delete'
            chordname[sus_index-1]='delete'

        if ninth==True and sus==True and sixth==True and(seventh==True or seventh_maj==True):
            thirteenth=True
            chordname.append(" 13")
            thirteenth_index=len(chordname)
            if ninth_index!=999:
                chordname[ninth_index-1]='delete'
            if sixth_index!=999:
                chordname[sixth_index-1]='delete'
            if sus_index!=999:

                chordname[sus_index-1]='delete'
            if seventh_index!=999:

                chordname[seventh_index-1]='delete'
            if eleventh_index!=999:
                chordname[eleventh_index-1]='delete'
            

    length=len(chordname)           
    for x in range(0,length):

        if chordname[x]!='delete':
            chordname_string=chordname_string+chordname[x]

    print ("\n")
    print ("Chord: ",chordstring)
    print ("\n")
    print ("Chord name: ",chordname_string)
    print ("\n")
    note=''

while True:
    
    name_chord()

