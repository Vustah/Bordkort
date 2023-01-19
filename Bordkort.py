#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import os
import sys
import time

def printText(sectioned_namelist,pagenr,farge=False):
    if farge:
        image = Image.open('bordkort_mal_farger.png')
    else:
        image = Image.open('bordkort_mal.png')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('ITCEDSCR.TTF', size=200)
    spots = {
        "1": (250, 1000),
        "2": (2300, 1000),
        "3": (250, 2450),
        "4": (2300,2450),
        "5": (250,3900),
        "6": (2300,3900),
        "7": (250,5350),
        "8": (2300,5350)
    }
    spot = 1
    for name in sectioned_namelist:
        (x, y) = spots[str(spot)]
        #name = checkNameLength(name)
        message = name
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), message, fill=color, font=font)
        spot+=1
        if spot >8:
            spot = 0

    draw.text((x, y), message, fill=color, font=font)
    # save the edited image
    image.save('greeting_card_'+str(pagenr)+'.png')

def checkNameLength(name):
    if len(name) >= 15:

        name = name.split(" ")
        if "" in name:
            name.remove("")
        firstName = name[0]
        lastName = name[-1]
        #print(firstName,lastName)
        if "-" in lastName:
            partial_name = lastName.split("-")
            partial_name = partial_name[0][0] + ".-" + partial_name[1]
            name = firstName + " " + partial_name
        else:

            name = firstName+" "+lastName


    return name

def getNames():
    f = open("Navn_til_bordkort.txt","r")
    namelist = []
    
    for line in f.readlines():
        try:
            name = line
            if name[-1] == "\n":
                name = name[0:-1]
            name = checkNameLength(name)
            #name = name.decode('unicode-escape')
            namelist.append(name)

            #whatisthis(line[0:-1])
        except LookupError as e:
            print(line)
            print(e)
            f.close()
            exit(1)

    f.close()
    return namelist

# Print iterations progress
def printProgressBar(iteration, total, prefix = 'Process: ', suffix = 'Complete', decimals = 1, length = 100, fill = '#'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write('\r%s |%s| %s%% %s ' % (prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration >= total:
        print(" ")
    else:
        sys.stdout.flush()

def makeSheets(namelist, farge):
    numberOfNames = len(namelist)
    remaindingNames = numberOfNames%8
    pagenr = 0
    printProgressBar(0, numberOfNames, prefix='Progress of creating greeting cards: ', suffix='Complete', length=50)
    for i in range(0,numberOfNames,8):
        partial_namelist = namelist[i:i+8]
        printText(partial_namelist,pagenr,farge)
        pagenr +=1

        printProgressBar(i + 8, numberOfNames, prefix='Progress of creating greeting cards: ', suffix='Complete', length=50)

    pagelist_names = ["greeting_card_"+str(i)+".png" for i in range(pagenr)]
    pagelist = [Image.open(page) for page in pagelist_names]
    printProgressBar(0, pagenr+1, prefix='Progress of combining greeting cards: ', suffix='Complete', length=50)

    if farge:
        pagelist_rgb = [Image.new('RGB', pagelist[i].size, (0, 0, 0)) for i in range(0,pagenr)]
    else:
        pagelist_rgb = [Image.new('RGB', pagelist[i].size, (255, 255, 255)) for i in range(0, pagenr)]

    for i in range(pagenr):
        pagelist_rgb[i].paste(pagelist[i],mask=pagelist[i].split()[-1])
        printProgressBar(i+1, pagenr+1, prefix='Progress of combining greeting cards: ', suffix='Complete', length=50)

    if farge:
        greeting_cards = "Bordkort_farge.pdf"
    else:
        greeting_cards = "Bordkort.pdf"

    first_page = pagelist_rgb[0]
    rest_of_pages = pagelist_rgb[1:]


    first_page.save(greeting_cards, "PDF", resolution=100.0, save_all=True, append_images=rest_of_pages)
    printProgressBar(pagenr + 1, pagenr + 1, prefix='Progress of combining greeting cards: ', suffix='Complete', length=50)

    printProgressBar(0, pagenr, prefix='Removing pages: ', suffix='Complete', length=50)
    for idx,page in enumerate(pagelist_names):
        os.remove(page)
        printProgressBar(idx + 1, pagenr , prefix='Removing pages: ', suffix='Complete', length=50)

if __name__ == '__main__':
    farge = False
    namelist = getNames()
    #for name in namelist:
    #    print(name)
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "farge":
            farge = True
    makeSheets(namelist, farge)