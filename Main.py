import keyboard
import numpy as np 
import cv2 
import pyautogui 
from selenium.webdriver import Firefox
from selenium.webdriver import Chrome
from selenium.webdriver.firefox.options import Options
import datetime
import time
import os
import tkinter as tk
from tkinter import ttk
import mouse
from PIL import Image

# CONFIG

DEVMODE = False

###################

BLUE = (100,130,255)
BLACK = (0,0,0)
GREY = (50,50,50)
WHITE = (255,255,255)

root = tk.Tk()
root.title("Sparx Helper")

SCREEN_WITH = 250
SCREEN_HEIGHT = 100

#set window attrabutes.
root.attributes('-topmost', 1)
root.geometry(str(SCREEN_WITH)+"x"+str(SCREEN_HEIGHT))
root.iconbitmap('./assets/app.ico')


def openBrowser():
    
    global BrowserOpen
    global opts
    global browser
    if (not BrowserOpen and selected_browser.get() == "firefox"):
        if DEVMODE:
            print("opening")
        opts = Options()
        #opts.add_argument("--headless")
        browser = Firefox(options=opts)
        browser.get('https://www.sparxmaths.uk/')
        BrowserOpen = True
        if DEVMODE:
            print("The browser has been opened")
    elif (not BrowserOpen and selected_browser.get() == "chrome"):
        if DEVMODE:
            print("opening")
        browser = Chrome()
        browser.get('https://www.sparxmaths.uk/')
        BrowserOpen = True
        if DEVMODE:
            print("The browser has been opened")


def screenshot():
    if (BrowserOpen):
        try:
            if (selected_browser.get() == "firefox"):
                QNumXPATH = '/html/body/div[1]/div[2]/div[2]/div/div/div/div[1]/div[1]/div[1]/div'
            elif (selected_browser.get() == "chrome"):
                QNumXPATH = '//*[@id="root"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div[1]/div'
        
            QNum = browser.find_element('xpath',QNumXPATH).get_attribute("textContent")
            print(str(QNum))
            #screenshot
            if DEVMODE:
                print("screenshot" + str(QNum)[15:17])
            image = pyautogui.screenshot() 
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) 
            cv2.imwrite(folder+str(QNum)[15:17]+".png", image)
        except:
            if DEVMODE:
                print("Can't screenshot.")
            pass


            
def search():
    global textbox
    if (textbox.get() == ''):
        pass
    else:
        searchfile = textbox.get()+".png"
        for i in os.listdir(folder):
            if (i == searchfile):
                #img = Image.open(folder+i)
                #img.show()
                img = cv2.imread(folder+i, cv2.IMREAD_ANYCOLOR)
                cv2.imshow("question", img)

def QuestionCheck():
    #print("checking...")
    global BrowserOpen
    try:
        browser.current_url
        BrowserOpen = True
    except:
        BrowserOpen = False
    #The script for question detection
    #==========================================================================================
    if keyboard.is_pressed("f10"):
        screenshot()
        while keyboard.is_pressed("f10"):
            pass
    else:
        try:
            if (selected_browser.get() == "firefox"):
                correctXPATH = '/html/body/div/div[2]/div[2]/div/div/div/div/div[3]/div/div[2]/div[1]/div/span[1]'
            elif (selected_browser.get() == "chrome"):
                correctXPATH = '//*[@id="RESULT_POPOVER"]/div/div[2]/div[1]/div/span[1]'
            correct = browser.find_element('xpath',correctXPATH).get_attribute("textContent")
            
            print(correct)
            screenshot()
            time.sleep(0.5)
            keyboard.press("enter")
        except:
            pass
    #print("done checking!")
    ttk.Label().after(1000, QuestionCheck)
    #==========================================================================================


text = tk.StringVar()

#see if the browser is open
global BrowserOpen
BrowserOpen = False
#set the date
date = datetime.datetime.now()

#set the path for the screenshots
path = './sparks_week.'+date.strftime("%W")
folder = 'sparks_week.'+date.strftime("%W")+'/'

#say the date
if DEVMODE:
    print("The Week Is: "+date.strftime("%W"))

#make the folder for the screenshots
if not os.path.exists(path): 
    os.mkdir(path)



selected_browser = tk.StringVar()
browser_cb = ttk.Combobox(root, textvariable=selected_browser)

browser_cb['values'] = ["chrome","firefox"]
browser_cb['state'] = 'readonly'
browser_cb.pack()

ttk.Button(root, text = "Open The Browser", command = openBrowser).pack(fill=tk.X)

textbox = ttk.Entry(root, textvariable=text)
textbox.pack(fill= tk.X,side=tk.LEFT,padx=1)
ttk.Button(root, text = "Find", command = search).pack(side=tk.RIGHT,padx=1)

QuestionCheck()
root.mainloop()

