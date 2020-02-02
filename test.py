#!/usr/bin/env python


###
# NOTICE: This software  source code and any of  its derivatives are the
# confidential  and  proprietary   information  of  Vecna  Technologies,
# Inc. (such source  and its derivatives are hereinafter  referred to as
# "Confidential Information"). The  Confidential Information is intended
# to be  used exclusively by  individuals or entities that  have entered
# into either  a non-disclosure agreement or license  agreement (or both
# of  these agreements,  if  applicable) with  Vecna Technologies,  Inc.
# ("Vecna")   regarding  the  use   of  the   Confidential  Information.
# Furthermore,  the  Confidential  Information  shall be  used  only  in
# accordance  with   the  terms   of  such  license   or  non-disclosure
# agreements.   All  parties using  the  Confidential Information  shall
# verify that their  intended use of the Confidential  Information is in
# compliance  with and  not in  violation of  any applicable  license or
# non-disclosure  agreements.  Unless expressly  authorized by  Vecna in
# writing, the Confidential Information  shall not be printed, retained,
# copied, or  otherwise disseminated,  in part or  whole.  Additionally,
# any party using the Confidential  Information shall be held liable for
# any and  all damages incurred  by Vecna due  to any disclosure  of the
# Confidential  Information (including  accidental disclosure).   In the
# event that  the applicable  non-disclosure or license  agreements with
# Vecna  have  expired, or  if  none  currently  exists, all  copies  of
# Confidential Information in your  possession, whether in electronic or
# printed  form, shall be  destroyed or  returned to  Vecna immediately.
# Vecna  mdeviceTestedes no  representations  or warranties  hereby regarding  the
# suitability  of  the   Confidential  Information,  either  express  or
# implied,  including  but not  limited  to  the  implied warranties  of
# merchantability,  fitness  for  a   particular  purpose,  or
# non-infringement. Vecna  shall not be liable for  any damages suffered
# by  licensee as  a result  of  using, modifying  or distributing  this
# Confidential Information.  Please email [info@vecnatech.com]  with any
# questions regarding the use of the Confidential Information.
#
# This module is responsible for the GUI of the Autokit Test
###

from Tkinter import *
import yaml
import yamlordereddictloader
import socket
import time
# The following import is the only reference to the Device you are testing --> Autokit, Vport, etc
from AutoKit import AutoKit
from sendEmail import *
import os
import sys

# GUI definitions
win = Tk()
win.title("Vecna Robotics Factory Test")
win.attributes("-fullscreen", True)
win.configure(background="grey")

# This allows users to specify in the 'GUIConfig.yaml' file, what board they are testing
currentDirectory = os.path.dirname(os.path.realpath(__file__))
configFile = currentDirectory + "/GUIConfig.yaml"
openedFile = open(configFile)

GUIConfiguration = yaml.load(openedFile, Loader=yamlordereddictloader.Loader)
# device type
deviceType = GUIConfiguration['deviceInfo']['type']
# a pre condition for the test to work properly
preCondition = GUIConfiguration['deviceInfo']['testPreCondition']
canvas = Canvas(win, width=320, height=300, bg="grey", highlightthickness=0)
img = PhotoImage(file=currentDirectory + "/VLOGO.png")
canvas.create_image(20, 0, anchor=NW, image=img)
canvas.place(relx=0, rely=0)
imgPass = PhotoImage(file=currentDirectory + "/Tpass.png")
imgFail = PhotoImage(file=currentDirectory + "/fail.png")
closed = False
deviceTested = None
setupSuccess = True

TEST_PASS = 1
TIME_TO_BOOT_SECONDS = 120
TIME_TO_DISPLAY_ERROR_MILLISECONDS = 10000


def initializeTest(serialNo):
    global setupSuccess

    """
            This method initializes the Autokit Test. If one forgets to enter a serial number, or a thumb drive into the
            raspberry pi, the test will not start.

            If the AutoKit has not yet finished booting, the test will not start. It waits until it can ping both the
            HLC and the SICK ethernet gateway.

            Once it is ready to begin the test it sets the correct initial states of GPIO pins for the relay tests, and
            will establish a connection to the SICK safety system by creating an AutoKit object if one does not exist
            already.

            Finally, it calls the run test method.

            Parameters:
            serialNo(String): serialNumber of AutoKit being tested

            Returns:
            None
    """

    global closed
    global deviceTested
    initLabel = Label(win, text="                                                                                  "
                                "                                                       ",
                      relief=FLAT, bg='grey', font=('Verdana', 18))
    initLabel.place(relx=.5, rely=.1, anchor=CENTER)
    startTime = time.time()
    usbStatus = detectUSB()
    win.update()
    if (len(serialNo.strip()) == 0):
        initLabel.config(text="Please Enter Board Serial Number to Begin.")
        win.update()
        return
    if (usbStatus == 0):
        initLabel.config(text="Please Enter A Thumb Drive to Record Test Results.")
        win.update()
        return

    # make a new device to test if we haven't made one
    if deviceTested is None:
        win.update()
        deviceTested = eval(deviceType)(GUI=win)
    win.update()
    deviceTested.setSerialNo(serialNo)

    while deviceTested.getBootStatus() == deviceTested.NOT_BOOTED:
        initLabel.config(text="Test will Start Once " + deviceType + " Boots. Please Wait up to 2 Minutes.")
        win.update()
        if time.time() - startTime > TIME_TO_BOOT_SECONDS:
            initLabel.config(text="Failed to connect to " + deviceType + ". Exiting.")
            win.update()
            initLabel.after(TIME_TO_DISPLAY_ERROR_MILLISECONDS, initLabel.config(text=""))
            return

    # if we have restarted the GUI, mdeviceTestede a new autokit. Don't mdeviceTestede a new AK every time
    time.sleep(2)
    initLabel.config(text="                        Initializing Test                        ")
    win.update()

    # relay and other initializations prior to 'Auto' switch
    setupSuccess = deviceTested.setup()
    if (deviceTested.verbose):
        print("Socket is open")
    runTest()


def restart():
    """
            This method closes and restarts the GUI

            Parameters:
            None

            Returns:
            None
    """
    python = sys.executable
    os.execl(python, python, *sys.argv)


def emailResults(report, email):
    """
            This method sends an email of the results to a specified email address.

            Parameters:
            report(List(String)): report of test
            email(String): email to which the test results are being sent

            Returns:
            None
    """
    if (len(email) > 5 and '.com' in email):
        sendResults(report.get(0, END), email)
        exitTest()
    else:
        if (deviceTested.verbose):
            print("Invalid Email")
        pass


def exitTest():
    """
            This method exits the test. It calls the device's exit method, clears the screen, clears
            the test results for the device, and returns the user to the home screen.

            Parameters:
            None

            Returns:
            None
    """
    if (deviceTested.verbose):
        print("Socket Closing")
    clearScreen()
    del deviceTested.testResults[:]
    del deviceTested.tests[:]
    # reset the  boolean for the next run
    deviceTested.setupSuccess = True
    deviceTested.exit()
    homeScreen()
    # restart()


def showReport():
    """
            This method displays the test report to the user. First it created all the necessary elements: \
            scroll window, buttons, labels, etc.

            Then, inside the scroll window, it places each test name followed by the test result, and repeats the
            process for the SICK module status'.

            Parameters:
            None

            Returns:
            None
    """
    clearScreen()
    reportScroll = Scrollbar(win, orient='vertical')
    reportScroll.place(relx=.9, rely=.49, anchor=CENTER)
    scrollLabel = Label(win, text="Scroll For Full Results", relief=FLAT, bg='orange', font='Verdana')
    scrollLabel.place(relx=.5, rely=.27, anchor=CENTER)
    report = Listbox(win, yscrollcommand=reportScroll.set, bg='grey', relief=FLAT, font="Verdana", width=55,
                     highlightthickness=1)
    report.insert(0, "Test Results For " + deviceTested.name + ": " + deviceTested.getSerialNo())
    report.itemconfig(0, bg='yellow green')
    report.insert(1, " ")

    for i in range(len(deviceTested.testResults)):
        results = deviceTested.tests[i].translateResult().split('\n')
        if (len(results) > 1):
            # add an empty line so that multi-line results look less crowded
            report.insert(END, " ")
            report.insert(END, deviceTested.tests[i].name + ": ")
            for eachResult in results:
                report.insert(END, eachResult)
                # if it's a pass or a new line character, leave it grey
                if ((deviceTested.tests[i].getResult() == 1) or len(eachResult) == 0):
                    report.itemconfig(END, bg='grey')
                else:
                    report.itemconfig(END, bg='red')
        else:
            report.insert(END, deviceTested.tests[i].name + ": " + results[0])
            if (deviceTested.tests[i].getResult() == 1):
                report.itemconfig(END, bg='grey')
            else:
                report.itemconfig(END, bg='red')

        if (deviceTested.verbose):
            print(deviceTested.tests[i].name + deviceTested.tests[i].translateResult())

    report.place(relx=.5, rely=.52, anchor=CENTER)
    reportScroll.config(command=report.yview, width=48)
    exit = Button(win, height=1, width=15, text="Finish & Leave Test", command=exitTest, font=("Verdana", 18),
                  bg='orange')
    exit.place(relx=.5, rely=0.94, anchor=CENTER)
    emailLabel = Label(win, text="Enter Your Email", relief=FLAT, bg='grey', font='Verdana')
    emailLabel.place(relx=.3, rely=.78, anchor=CENTER)
    emailBox = Entry(win)
    emailBox.place(relx=.5, rely=0.78, anchor=CENTER)
    send = Button(win, text="Email Results", command=lambda: emailResults(report, emailBox.get()), font="Verdana",
                  bg='yellow green')
    send.place(relx=.5, rely=0.85, anchor=CENTER)
    win.update()


def detectUSB():
    """
            This method detects the external thumb drive connected to the Raspberry Pi. It does this by looking in the
            /media/pi folder. If no USB Drive is connected, the folder is empty. Otherwise, we tdeviceTestede the name of the
            directory with /media/pi as our USB Drive identifier.

            Parameters:
            None

            Returns:
            String with the name of the USB drive
    """

    usbFolder = '/media/pi/'
    if not os.listdir(usbFolder):
        if ((deviceTested is not None) and (deviceTested.verbose == True)):
            print("No USB Found")
        return 0
    else:
        if ((deviceTested is not None) and (deviceTested.verbose == True)):
            print("USB Found")
        return os.listdir(usbFolder)


def writeToTextFile():
    """
            This method writes the test report to the USB drive, and appends to the name of the file a time stamp.
            The name of the file contains the AutoKit serialNumber as an identifier as to which file corresponds to
            which AutoKit.

            Parameters:
            None

            Returns:
            None
    """

    report = []
    body = ""
    report.append("Test Results For " + deviceTested.name + ": " + deviceTested.getSerialNo() + "\r\n")
    for i in range(len(deviceTested.testResults)):
        results = deviceTested.tests[i].translateResult().split('\n')
        if (len(results) > 1):
            report.append('\r\n')
            report.append(deviceTested.tests[i].name + ": ")
            for eachResult in results:
                report.append(eachResult)
        else:
            report.append(deviceTested.tests[i].name + ": " + results[0])

    f = open("/media/pi/" + str(detectUSB()[0]) + "/BOARD_" + deviceTested.getSerialNo() + "_" + time.strftime(
        "%Y%m%d-%H%M%S") + ".txt", "w+")
    if (deviceTested.verbose):
        print(report)
    for i in report:
        body = body + i + '\r\n'
    f.write(body)
    f.close()


def failScreen():
    """
            This method displays the test result as a "Fail" to the user. It then writes the test results to a file.

            Parameters:
            None

            Returns:
            None
    """

    clearScreen()
    canvasFail = Canvas(win, width=220, height=220, bg="grey", highlightthickness=0)
    canvasFail.create_image(10, 0, anchor=NW, image=imgFail)
    canvasFail.place(relx=.5, rely=.5, anchor=CENTER)
    failLabel = Label(win, text=deviceType + " Test Failed!", relief=FLAT, bg='grey',
                      font=("Verdana", 18))
    failLabel.place(relx=0.5, rely=0.73, anchor=CENTER)
    failureDetails = Button(win, text="Details", command=showReport, bg='orange', font=("Verdana", 18), height=1,
                            width=5)
    failureDetails.place(relx=0.5, rely=0.83, anchor=CENTER)
    exit = Button(win, height=1, width=15, text="Finish & Leave Test", command=exitTest, font=("Verdana", 18),
                  bg='orange')
    exit.place(relx=.5, rely=0.93, anchor=CENTER)
    writeToTextFile()


def passScreen():
    """
            This method displays the test result as a "Pass" to the user. It then writes the test results to a file.

            Parameters:
            None

            Returns:
            None
    """

    clearScreen()
    canvasPass = Canvas(win, width=220, height=220, bg="grey", highlightthickness=0)
    canvasPass.create_image(10, 0, anchor=NW, image=imgPass)
    canvasPass.place(relx=0.5, rely=0.5, anchor=CENTER)
    passLabel = Label(win, text=deviceType + " Test Passed!", relief=FLAT, bg='grey',
                      font=("Verdana", 18))
    passLabel.place(relx=0.5, rely=0.73, anchor=CENTER)
    passDetails = Button(win, text="Details", command=showReport, bg='orange', font=("Verdana", 18), height=1,
                         width=5)
    passDetails.place(relx=0.5, rely=0.83, anchor=CENTER)
    exit = Button(win, height=1, width=15, text="Finish & Leave Test", command=exitTest, font=("Verdana", 18),
                  bg='orange')
    exit.place(relx=.5, rely=0.93, anchor=CENTER)
    writeToTextFile()


def clearScreen():
    """
            This method clears the screen for the next screen to display. Every element is deleted except for the
            Vecna logo which remains on every screen.

            An empty label is put in the center of the screen each time this method is called. This is done because
            otherwise the label that is used as the test is deleted. This does not affect the appearance of the GUI as
            it essentially has no text.

            Parameters:
            None

            Returns:
            None
    """
    for widget in win.winfo_children():
        if widget.winfo_class() != Canvas and widget.winfo_height() != 300:
            widget.destroy()
    currentAction = Label(win, text=" ", relief=FLAT, bg='grey', font=("Verdana", 18))
    currentAction.place(relx=0.5, rely=0.5, anchor=CENTER)


def homeScreen():
    """
            This method is the home screen of the GUI. When the green central button is pressed, the test begins
            initializing.

            Parameters:
            None

            Returns:
            None
    """

    serialLabel = Label(win, text="Enter Board Serial Number:", relief=FLAT, bg='grey', font='Verdana')
    serialLabel.place(relx=.5, rely=.9, anchor=CENTER)
    serialBox = Entry(win)
    serialBox.place(relx=.5, rely=0.95, anchor=CENTER)
    startInManual = Label(win, text=preCondition, relief=FLAT, bg='red', font=("Verdana", 18))
    startInManual.place(relx=0.5, rely=0.32, anchor=CENTER)
    startTest = Button(win, text="Start Autokit Test", command=lambda: initializeTest(serialBox.get()),
                       bg='yellow green', font=("Verdana", 18), height=8, width=30)
    startTest.place(relx=0.5, rely=0.6, anchor=CENTER)
    startTest.config(relief=RAISED)


def runTest():
    """
            This method runs the AutoKit test.

            If the connection is open, each test configured upon construction of the Autokit object is run. After all
            the tests have run, the test will show the result of the test.

            Parameters:
            None

            Returns:
            None
    """

    clearScreen()
    global closed
    if closed == True:
        if (deviceTested.verbose):
            print("Socket Opening")
        deviceTested.sickSys.connect()
        closed = False

    progressLabel = Label(win, text="Progress: ", relief=FLAT, bg='grey', font=("Verdana", 18)).place(relx=0.1,
                                                                                                      rely=0.9,
                                                                                                      anchor=CENTER)
    currentAction = Label(win, relief=FLAT, bg='grey', font=("Verdana", 18))
    currentAction.place(relx=0.5, rely=0.5, anchor=CENTER)
    loadingBar = Canvas(win, width=500, height=25)
    loadingBar.place(relx=.53, rely=.905, anchor=CENTER)
    progress = loadingBar.create_rectangle(0, 0, 5, 25, fill="yellow green")
    exit = Button(win, text="Quit Test", command=exitTest, font=("Verdana", 18), bg='orange', height=2, width=10)
    exit.place(relx=.75, rely=0.12)
    win.update()
    if (deviceTested.verbose):
        print("Please Turn Auto/Manual Swith to 'Auto' To Begin Test")
    if (closed == False):
        runStatus = deviceTested.run(progress=progress, currentAction=currentAction, loadingBar=loadingBar)
        if (runStatus):
            if (deviceTested.verbose):
                print(deviceTested.testResults)
            if (all(result == TEST_PASS for result in deviceTested.testResults)):
                passScreen()
            else:
                failScreen()
        else:
            return


homeScreen()
win.mainloop()
