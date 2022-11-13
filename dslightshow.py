from argparse import FileType
from ast import Import
from cgitb import enable
from distutils.log import warn
import PySimpleGUI as sg
from pydualsense import *
import time
import threading
import math
import colorsys
import os
import json

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b

def tocel(num: float):
    if num == "":
        return(0)
    else:
        try:
            value = float(num)
            return(math.floor(clamp(value, 0, 255)))
        except:
            return(0)

sg.theme("SystemDefaultForReal")
ds = pydualsense()
ds.init()

leftColumn = [
    [sg.Text("Mode")], 
    [sg.Text("Speed")],
    [sg.Text("ColorA")],
    [sg.Text("ColorB")],
]

rightColumn = [
    [sg.Combo(["Solid", "Pulse", "Rainbow"], default_value="Solid", size=(15, 20), readonly=True, key="type", enable_events=True)],
    [sg.Input("7", key="speed", size=(5,0), text_color="red")],
    [sg.Input("0", key="ar", size=(5,0)), sg.Input("0", key="ag", size=(5,0)), sg.Input("255", key="ab", size=(5,0))],
    [sg.Input("0", key="br", size=(5,0), text_color="red"), sg.Input("0", key="bg", size=(5,0), text_color="red"), sg.Input("25", key="bb", size=(5,0), text_color="red")],
]

ftypes = (("DSL", ".dsl"), ("TXT", ".txt"), ("ALL FILES", ".*"))

layout = [
    [sg.Column(leftColumn), sg.Column(rightColumn)],
    [sg.Button("Apply Changes")],
    [sg.FileBrowse("Import", file_types=ftypes, target="Import", enable_events=True), sg.SaveAs("Export", file_types=ftypes, target="Export", enable_events=True)],
    [sg.Text("", key="file")],
]

window = sg.Window("DS Lights", layout, margins=(20, 20))

event = None
values = None

type = "Solid"
delta = 0.01
speed = 7
colora = (0, 0, 255)
colorb = (0, 0, 25)

def windowLoop():
    global event, values, type, speed, colora, colorb

    while True:
        event, values = window.read()
        print(event,values)
        if event in (None, "Exit"):
            break
        elif event == "type":
            type = values["type"]
            if values["type"] =="Solid":
                window["speed"].update(text_color="red")
                window["ar"].update(text_color="black")
                window["ag"].update(text_color="black")
                window["ab"].update(text_color="black")
                window["br"].update(text_color="red")
                window["bg"].update(text_color="red")
                window["bb"].update(text_color="red")
            elif values["type"] == "Pulse":
                window["speed"].update(text_color="black")
                window["ar"].update(text_color="black")
                window["ag"].update(text_color="black")
                window["ab"].update(text_color="black")
                window["br"].update(text_color="black")
                window["bg"].update(text_color="black")
                window["bb"].update(text_color="black")
            elif values["type"] == "Rainbow":
                window["speed"].update(text_color="black")
                window["ar"].update(text_color="red")
                window["ag"].update(text_color="red")
                window["ab"].update(text_color="red")
                window["br"].update(text_color="red")
                window["bg"].update(text_color="red")
                window["bb"].update(text_color="red")
        elif event == "Apply Changes":
            speed = float(values["speed"])
            colora = (tocel(values["ar"]), tocel(values["ag"]), tocel(values["ab"]))
            colorb = (tocel(values["br"]), tocel(values["bg"]), tocel(values["bb"]))
        elif event == "Import":
            print("Importing settings from "+values["Import"])
            try:
                file = open(values["Import"], "r")
                dict = json.load(file)
                try:
                    if dict.get("type", type):
                        type = dict["type"]
                        window["type"].update(type)
                    if dict.get("colora", colora):
                        colora = dict["colora"]
                        window["ar"].update(colora[0])
                        window["ag"].update(colora[1])
                        window["ab"].update(colora[2])
                    if dict.get("colorb", colorb):
                        colorb = dict["colorb"]
                        window["br"].update(colorb[0])
                        window["bg"].update(colorb[1])
                        window["bb"].update(colorb[2])
                    if dict.get("speed", speed):
                        speed = float(dict["speed"])
                        window["speed"].update(speed)
                except:
                    warn("Error: File is missing value")
            except:
                warn("Error: Invalid file")
        elif event == "Export":
            print("Exporting settings to "+values["Export"])
            dict = {
                "type": values["type"],
                "colora": (tocel(values["ar"]), tocel(values["ag"]), tocel(values["ab"])),
                "colorb": (tocel(values["br"]), tocel(values["bg"]), tocel(values["bb"])),
                "speed": values["speed"]
            }
            # contents = json.dumps(dict)
            with open(values["Export"], "w") as outfile:
                json.dump(dict, outfile)

    window.close()
    os._exit(1)
    


def lightLoop():
    global event, values, ds, type, colora, colorb
    t = 0

    while True:
        if values != None: # \/ TYPE CHECK \/ #
            if type == "Solid":
                r, g, b = colora[0], colora[1], colora[2]

                ds.light.setColorI(r, g, b)
            elif type == "Pulse":
                c = clamp(math.sin(t*speed)/2+0.5, 0, 1)
                # print(c)
                r, g, b = lerp(colora[0], colorb[0], c), lerp(colora[1], colorb[1], c), lerp(colora[2], colorb[2], c)

                r = math.floor(r)
                g = math.floor(g)
                b = math.floor(b)

                ds.light.setColorI(r, g, b)
            elif type == "Rainbow":
                r, g, b = colorsys.hsv_to_rgb(t*(speed/7)%1, 1, 0.5)

                r = math.floor(r*255)
                g = math.floor(g*255)
                b = math.floor(b*255)

                ds.light.setColorI(r, g, b)
        
        t += delta
        time.sleep(delta*2)

p1 = threading.Thread(target=windowLoop)
p2 = threading.Thread(target=lightLoop)

p1.start()
p2.start()
