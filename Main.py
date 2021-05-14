# Author: Robin Bachus

# This is a script to save website ID's based on user defined tags (language, author and page count --> maybe later)
# This example is used to filter SCP's based on tags
# This has to be run trough te external Python terminal for the visuals to properly work (Has been fixed, but still looks better in ext. shell)

# TODO: Add multithreading
# TODO: Add tags in results 
# TODO: Streamline DevMode 
# TODO: Add comments to source code

# ---Imports---
from random import choice
from os import system, name
import re
from bs4 import BeautifulSoup
import requests
import time
import os
import sys
import tkinter as tk
from datetime import date


# ---Functions---
# function to clear the terminal
def clear():    
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

# Tkinter button functions for turning on Dev_Mode
def Dev_Mode():
    global Devmode
    Devmode = True

# Tkinter function for executing multiple commands per button
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func


# ---Variables---
Tags_input = []
a = 0
Tag = ""
rounds = 0
loop = 0
Tags_Stripls = []
Devmode = False


# ---Main Code: TagList (1/2)---
# Print the date in Debug File
with open("debug.txt", "a+") as db:
    print("-------------- start program ------------", file=db)
    print("Date: ", date.today(), file=db)

clear()

# makes a list of Tags_input to look for in the page
while Tag != "" or a == 0:
    Tag = input("Enter your tag to the List: ")
    clear()
    if Tag != "" or a == 0:
        if Tag != "DevMode" and Tag != "devmode":
            Tags_input.append(Tag.lower())
            print(Tags_input)
            a = 1
        else:
            # Tkinter window to turn on Dev Mode
                # Setting up the tkinter window
            root = tk.Tk()
            root.title("Turn on Dev Mode?")

                    # positioning the window in the middle of the creen
                    # Gets the requested values of the height and widht.
            windowWidth = root.winfo_reqwidth()
            windowHeight = root.winfo_reqheight()
            print("Width",windowWidth,"Height",windowHeight)

                    # Gets both half the screen width/height and window width/height
            positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
            positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
            
                    # Positions the window in the center of the page.
            root.geometry("300x155+{}+{}".format(positionRight, positionDown))
            
            button_refresh = tk.Button(root, text="Yes ", command=combine_funcs(Dev_Mode, root.destroy))
            button_refresh.pack(fill='x')

            button_refresh = tk.Button(root, text="No ", command=root.destroy)
            button_refresh.pack(fill='x')

            root.call('wm', 'attributes', '.', '-topmost', '1')

            print(Tags_input)
    else:
        break

clear()
print("Your Tag List:")
print(Tags_input)

clear()

if Devmode:
    print ("How many scps would you like to find?")
    scps = input("scps: ")
    print ("How many files would you like to irtirate trough?")
    ittarations = input("ittarations: ")
    print('What would you like the resultfile to be called? (Do not add ".txt", default is "results.txt")')
    resFile = input("filename: ")
    if resFile == "":
        resFile = "results"
    print('What would you like the debug file to be called? (Do not add ".txt", default is "debug.txt")')
    DB_File = input("filename: ")
    if DB_File == "":
        DB_File = "debug"

    File = resFile, ".txt"
    File = ''.join(File)

    DB_File = DB_File, ".txt"
    DB_File = ''.join(DB_File)


else:
    scps = 10
    ittarations = 150
    File = "results.txt"
    DB_File = "debug.txt"


clear()

startTime = time.time()

# ---Main Code: URL genaration and tag comparing (2/2)---
# This code will generate urls and it will save the SCP's that have the user-given tags in an output file
try:
    with open(str(DB_File), "a+") as text_file:
        print("-------------- start scan --------------", file=text_file)
        print("result file: %s " % (str(File)) , file=text_file)
        print ("tags: {}".format(Tags_input), file=text_file)

        with open(File, "a+") as resultfile:
            print("Tags:", Tags_input, file=resultfile)
            print("Date: ", date.today(), file=resultfile)
            print("", file=resultfile)
            print("", file=resultfile)

            while loop < int(scps) and rounds < int(ittarations):

                Tags_Stripls = []
                Tags = []

                sequence = [i for i in range(5000)]
                A = choice(sequence)
                url = "http://www.scp-wiki.net/scp-{}".format(A)
                # print(url)

                # this takes the url and recives its html file

                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                results = soup.find(id='main-content')
                page_tags = results.find_all('div', class_='page-tags') # finding the element wich contains all the tags

                # finding the tag elements and putting them in a list as strings

                for page_tags in page_tags:
                    Tags = page_tags.find_all('a')
                    if None in Tags:
                        continue
                    list(Tags)
                    # print(Tags)
                    # print(len(Tags))

                    # getting the tag name from the element

                    for i in Tags:
                        var = str(i)
                        pattern = ">((.*?))<"
                        var = re.search(pattern, var)

                        var_tag = str(var.group(1))
                        # print(var_tag)

                        Tags_Stripls.append(var_tag)
                    print(Tags_Stripls)

                    elem = 0

                    for i in Tags_input:
                        if Tags_Stripls.count(i) > 0 :
                            print (i, "yes", file=text_file)

                            pageContent = soup.find(id='page-content')
                            rating_Temp = pageContent.find('span', class_='number prw54353')
                            rating_Temp = re.search('prw54353">((.*?))</span>', str(rating_Temp))
                            rating = str(rating_Temp.group(1))

                            # Print the ressults in the results file
                            elem = elem +1
                            if elem == len(Tags_input):
                                print(url, file=text_file) # URL in db file
                                print("scp-%d: %s" % (int(A), url),file=resultfile) # scp + URL in res file
                                print("rating: %s" % (rating), file=resultfile)
                                # print(Tags_Stripls, file=resultfile) # list of tags in res file   # TODO: Print the tags in a nice way
                                print("", file=resultfile) # new line in res file
                                loop = loop +1
                            
                        else:
                            print (i, "no", file=text_file)

                    print ("", file=text_file)
                    clear()
                    rounds = rounds + 1
                    print(url)
                    endTime = time.time() - startTime
                    print("Round: %d/%d" % (rounds, int(ittarations)))
                    print("Scp: %d/%d" % (loop, int(scps)))
                    print(round(endTime, 3), "seconds")

            endTime = time.time() - startTime
            print("", file=resultfile)
            print("Scps: %d/%d" % (loop, int(scps)), file=resultfile)
            print("Ittarations: %d/%d" % (rounds, int(ittarations)), file=resultfile)
            print("Time: %d seconds" % (int(endTime)), file=resultfile)
            print("---------------------------------------------------", file=resultfile)
            print("", file=resultfile)


        print("----------- end scan -------------------", file=text_file)
        print("", file=text_file)
        print("", file=text_file)

except:
    with open ("debug.txt", "a+") as text_file:
        print("", file=text_file)
        print("Unexpected error:", sys.exc_info()[0], file=text_file)
        print("", file=text_file)
        print("----------- Unexpected error -----------", file=text_file)
        print("----------- end scan -------------------", file=text_file)
        print("", file=text_file)
        print("", file=text_file)
        raise

clear()
print ("Keep output file? [y/n]")
RM = input()
clear()

if RM == "n":
    os.remove(File)
    print(File, " has been removed")
    print()
    print()
    end = input("press enter to exit")

elif RM == "y":
    print("The output file can be found in this programs directory")
    print()
    print()
    end = input("press enter to exit")
    
else:
    print("Error: Command not recognized, output file not removed")
    print()
    print()
    end = input("press enter to exit")
