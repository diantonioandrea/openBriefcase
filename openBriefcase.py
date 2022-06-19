# compilation: pyinstaller.exe .\openBriefcase.py -F -c
# openBriefcase, a simple CLI accounting program written in Python

import pickle
import sys
import os

from datetime import datetime, date
from copy import copy

if not os.path.exists(str(os.getcwd()) + "/Data"): # checks "Data" folder
    os.makedirs(str(os.getcwd()) + "/Data")

import classes
import functions
import translations
from translations import langIndex

# startup message
print("v1.0.0") # release tag
print(translations.startupMessage[langIndex] + translations.exCmdMessage[langIndex])

while True: # login
    try:
        username = functions.stringInput(translations.usernameRequest[langIndex]).lower()

        if " " in username:
            continue

        userFile = open("Data/" + username + ".p", "rb")
        userData = pickle.load(userFile) # user
        userFile.close()

        wUser = userData

        print(translations.welcomeMessage[langIndex] + str(wUser))
        print(translations.lastLogoutMessage[langIndex] + wUser.lastLogout)

        break
        
    except(FileNotFoundError):
        print(translations.enUserCreationUI[langIndex])

        if functions.approve(username):
            wUser = classes.user(username)

            print(translations.createdUserMessage[langIndex] + wUser.username + translations.exUserCreationUI[langIndex])

            break
        
        print(translations.exUserCreationUI[langIndex])
        print(translations.noCreatedUserMessage[langIndex])

    except(KeyboardInterrupt):
        print(translations.exCmdMessage[langIndex])

    except(EOFError):
        print(translations.exMessage[langIndex])
        sys.exit(0)

    except:
        print(translations.unexpectedError[langIndex])

print(translations.enMainUI[langIndex])

# variables initialization
env = "home"
wAccount = None
wWeek = str(date.today().isocalendar()[0]) + "." + str(date.today().isocalendar()[1])

while True: # main user interface (CLI)
    try:
        command = " ".join(input("\n" + str(wUser) + "@openBriefcase/" + env + ": ").split()).lower()
        instructions = command.split(" ") # for multiple words commands

        if env == "home":
            if len(instructions) == 1:
                if instructions[0] in translations.cmd_help:
                    print(translations.homeHelp[langIndex])
                    continue

                elif instructions[0] in translations.cmd_accounts:
                    if len(wUser.accounts) == 0:
                        print(translations.createAccountMessage[langIndex])
                        continue

                    wAccount = functions.elementFromList(wUser.accounts)

                    if wAccount == None:
                        continue

                    env = "accounts/" + wAccount.id
                    continue

                elif instructions[0] in translations.cmd_details:
                    wUser.details()

            if len(instructions) == 2:
                if instructions[0] in translations.cmd_new:
                    if instructions[1] in translations.cmd_accounts:
                        print(translations.enAccountCreationUI[langIndex] + translations.exCmdMessage[langIndex])

                        while True:
                            try:
                                newAccountName = functions.stringInput(translations.accountNameRequest[langIndex]).lower()
                                newAccountBalance = functions.numericalInput(translations.accountBalanceRequest[langIndex])

                                newAccount = classes.account(newAccountName, newAccountBalance)

                                if newAccount.isOpen:
                                    wUser.accounts.append(newAccount)
                            
                            except(EOFError):
                                print(translations.exAccountCreationUI[langIndex])
                                break
                            
                        continue
                
                elif instructions[0] in translations.cmd_delete:
                    if instructions[1] in translations.cmd_accounts:
                        print(translations.enAccountDeletionUI[langIndex] + translations.exCmdMessage[langIndex])

                        while True:
                            try:
                                if not wUser.deleteAccount():
                                    break

                            except(EOFError):
                                print(translations.exAccountDeletionUI[langIndex])
                                break

        elif "accounts/" in env:
            if len(instructions) == 1:
                if instructions[0] in translations.cmd_help:
                    print(translations.accountsHelp[langIndex])
                    continue

                if instructions[0] in translations.cmd_details: # show account movements
                    wAccount.details()

                if instructions[0] in translations.cmd_close:
                    if wAccount.isOpen:
                        wAccount.isOpen = False
                        print(translations.accountClosed[langIndex])
                    else:
                        print(translations.accountAlreadyClosed[langIndex])
                
                if instructions[0] in translations.cmd_open:
                    if not wAccount.isOpen:
                        wAccount.isOpen = True
                        print(translations.accountOpened[langIndex])
                    else:
                        print(translations.accountAlreadyOpened[langIndex])

            if len(instructions) == 2:
                if instructions[0] in translations.cmd_new:
                    if instructions[1] in translations.cmd_movements: # multiple movements
                        print(translations.enMovementCreationUI[langIndex]  + translations.movementeFormatMessage[langIndex] + translations.exCmdMessage[langIndex])

                        while True:
                            try:
                                newMovementReason = functions.stringInput(translations.movementReasonRequest[langIndex])
                                newMovementAmount = functions.numericalInput(translations.movementAmountRequest[langIndex])

                                wAccount.movement(wWeek, newMovementReason, newMovementAmount)

                            except(EOFError):
                                print(translations.exMovementCreationUI[langIndex])
                                break
                    
                    elif instructions[1] in translations.cmd_informations:
                        print(translations.enInformationCreationUI[langIndex] + translations.infoFormatMessage[langIndex] + translations.exCmdMessage[langIndex])

                        while True:
                            try:
                                newInfoField = functions.stringInput(translations.informationFieldRequest[langIndex])
                                newInfoValue = functions.stringInput(translations.informationValueRequest[langIndex])

                                wAccount.information(newInfoField, newInfoValue)

                            except(EOFError):
                                print(translations.exInformationCreationUI[langIndex])
                                break
                
                elif instructions[0] in translations.cmd_cancel:
                    if instructions[1] in translations.cmd_movements:
                        print(translations.enMovementCancellationUI[langIndex] + translations.exCmdMessage[langIndex])

                        while True:
                            try:
                                if not wAccount.cancelMovement():
                                    break

                            except(EOFError):
                                print(translations.exMovementCancellationUI[langIndex])
                                break
                
                elif instructions[0] in translations.cmd_edit:
                    if instructions[1] in translations.cmd_movements:
                        print(translations.enMovementEditUI[langIndex] + translations.exCmdMessage[langIndex])

                        while True:
                            try:
                                if not wAccount.editMovement():
                                    break

                            except(EOFError):
                                print(translations.exMovementEditUI[langIndex])
                                break
                
                elif instructions[0] in translations.cmd_delete:
                    if instructions[1] in translations.cmd_informations:
                        print(translations.enInformationDeletionUI[langIndex] + translations.exCmdMessage[langIndex])

                        while True:
                            try:
                                if not wAccount.deleteInformation():
                                    break

                            except(EOFError):
                                print(translations.exInformationCreationUI[langIndex])
                                break

    except(EOFError):
        if env != "home":
            env = "home"
            continue

        print(translations.exMainUI[langIndex])

        wUser.lastLogout = str(datetime.now())

        userFile = open("Data/" + wUser.username + ".p", "wb")
        pickle.dump(wUser, userFile)
        userFile.close()

        sys.exit(0)
    
    except(KeyboardInterrupt):
        print(translations.exCmdMessage[langIndex])

    except:
        print(translations.unexpectedError[langIndex])