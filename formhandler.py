#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi
import cgitb
print "Content-type: text/html\n"
global inp
cgitb.enable()


def cgiToDict(fieldStorage):
    ans = {}
    for key in fieldStorage.keys():
        ans[key] = fieldStorage[key].value
    return ans


def toVar():
    form = cgiToDict(cgi.FieldStorage())
    return form


inp = toVar()  # dictonary with html form inputs


"""
┌┐ ┌─┐┌─┐┬┌─┌┐ ┌─┐┌┐┌┌─┐  ┌─┐┌─┐┌┬┐┌─┐
├┴┐├─┤│  ├┴┐├┴┐│ ││││├┤   │  │ │ ││├┤
└─┘┴ ┴└─┘┴ ┴└─┘└─┘┘└┘└─┘  └─┘└─┘─┴┘└─┘
"""


def rawData():   # builds out the filename based off inputs, returns rawData
    try:
        file = open(str(inp["time"] + "_" + inp["type"] + "-0" + ".txt"), "r").read()
    except IOError:
        file = open("error.html", "r").read()
    return file


# accounts for the zero index, plus terminal newline
flen = len(rawData().split("\n")) - 2


niceInpTime = {"1501": "January 2015", "1506": "June 2015", "1601": "January 2016", "1606": "June 2016", "1701": "January 2017"}


# mega versatile function!!
# treats the data as a xy plane, returns value at row and column
# makes iterating a breeze
def dataIso(line, column):
    data = rawData().split("\n")
    output = data[line].split("|")
    return output[column].strip()


# returns a list of all the data at the column, in the same order as the list
def columnGen(col):
    output = []
    for x in range(flen):
        output.append(dataIso(x, col))

    for idx, x in enumerate(output):
        output[idx] = x.strip()
    return output


# lots of weird formatting in the raw data, this helps
# might be deprecated? idk
def spaceRemove(x):
    return x.replace(" ", "")


"""
┌─┐┌─┐┌─┐┌─┐┬┌─┐┬┌─┐  ┌─┐┌─┐┬┌─┌─┐  ┌─┐┌─┐┌┐┌┌─┐┬─┐┌─┐┌┬┐┌─┐┬─┐
└─┐├─┘├┤ │  │├┤ ││    ├─┘│ │├┴┐├┤   │ ┬├┤ │││├┤ ├┬┘├─┤ │ │ │├┬┘
└─┘┴  └─┘└─┘┴└  ┴└─┘  ┴  └─┘┴ ┴└─┘  └─┘└─┘┘└┘└─┘┴└─┴ ┴ ┴ └─┘┴└─
"""


# given the name of a pokemon, return a list with all of its info
def locateRow(value, col):
    output = []
    pokeInfo = []
    value = value.lower()
    for x in range(flen):
        output.append(spaceRemove(dataIso(x, col)).lower())
    location = output.index(value)
    for x in range(1, 7):
        pokeInfo.append(dataIso(location, x))
    return pokeInfo


# using the pokeFact.html, format it with relevant data
# return the formatted html
def pokePretty(data):
    file = open("pokeFact.html").read()
    return file.format(pokemon=data[1].lower(), percentUsed=data[2], rank=data[0], time=niceInpTime[inp["time"]], type=inp["type"])


def specPoke():
    return pokePretty(locateRow(inp["selectedPoke"], 2))


def specRank():
    return pokePretty(locateRow(inp["selectedRank"], 1))


"""
┬─┐┌─┐┬ ┬  ┌┬┐┌─┐┌┬┐┌─┐  ┌─┐┌─┐┌┐┌
├┬┘├─┤│││   ││├─┤ │ ├─┤  │ ┬├┤ │││
┴└─┴ ┴└┴┘  ─┴┘┴ ┴ ┴ ┴ ┴  └─┘└─┘┘└┘
"""


def tableHandler():
    template = open("rawData.html", "r").read()
    table = ""

    for x in range(flen):
        table += "<tr>"

        table += "<td>"
        table += dataIso(x, 1)
        table += "</td>"

        table += "<td>"
        table += dataIso(x, 2)
        table += "</td>"

        table += "<td>"
        table += dataIso(x, 3)
        table += "</td>"

        table += "</tr>"

        table += "\n"

    return template.format(data=table, type=inp["type"], time=niceInpTime[inp["time"]])


"""
┌─┐┌─┐┌─┐┬ ┬┬  ┌─┐┬─┐┬┌┬┐┬ ┬  ┌─┐┌─┐┌┐┌
├─┘│ │├─┘│ ││  ├─┤├┬┘│ │ └┬┘  │ ┬├┤ │││
┴  └─┘┴  └─┘┴─┘┴ ┴┴└─┴ ┴  ┴   └─┘└─┘┘└┘
"""

"""
def calc():
    fname = []
    for x in ["1501", "1506", "1601", "1606", "1701"]:
        fname.append(str(x + "_" + inp["type"] + "-0" + ".txt"))
        print fname
"""

"""
┌─┐┬─┐┬─┐┌─┐┬─┐  ┬ ┬┌─┐┌┐┌┌┬┐┬  ┌─┐┬─┐
├┤ ├┬┘├┬┘│ │├┬┘  ├─┤├─┤│││ │││  ├┤ ├┬┘
└─┘┴└─┴└─└─┘┴└─  ┴ ┴┴ ┴┘└┘─┴┘┴─┘└─┘┴└─
"""
errorFile = open("error.html", "r").read()


def errorHandle(message):
    return errorFile.format(errorcode=message)



"""
╦   ╔═╗
║───║ ║
╩   ╚═╝
"""


# top level code to handle possible form io
def main():
    if inp["time"] == "1501" and inp["type"] == "battlefactory":
        print errorHandle("battlefactory didnt exist")
        return

    try:
        if inp["calcMethod"] == "specific":
            if inp["selectedPoke"] in columnGen(2):
                print specPoke()
            else:
                print errorHandle("pokemon not found")

        elif inp["calcMethod"] == "general":
            print tableHandler()

        elif inp["calcMethod"] == "ranking":
            if inp["selectedRank"] in columnGen(1):
                print specRank()
            else:
                print errorHandle("rank out of range/ type a number for the rank")
        elif inp["calcMethod"] == "popular":
            print calc()

    except KeyError:
        print errorHandle("you didnt fill it out!")


main()


"""
┌─┐┬ ┬┌┬┐┬ ┬┬─┐┌─┐  ┌─┐┬  ┌─┐┌┐┌┌─┐
├┤ │ │ │ │ │├┬┘├┤   ├─┘│  ├─┤│││└─┐
└  └─┘ ┴ └─┘┴└─└─┘  ┴  ┴─┘┴ ┴┘└┘└─┘

SEARCH BY RANK
"""
