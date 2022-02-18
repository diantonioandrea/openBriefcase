import functions

import translations
from translations import langIndex

class user:
    def __init__(self, username: str) -> None:
        self.username = username
        self.lastLogout = ""

        self.accounts = []

    def __str__(self) -> str:
        return self.username
    
    def details(self):
        print(translations.userCurrentSituation[langIndex] + str(self))
        print(translations.accountsMessage[langIndex])

        totalBalance = 0

        for fAccounts in self.accounts:
            print(fAccounts)

            if fAccounts.isOpen:
                totalBalance += fAccounts.balance

        if len(self.accounts) == 0:
            print(translations.nothingToSeeHere[langIndex])

        print(translations.currentBalance[langIndex] + str(round(totalBalance, 2)))
    
    def deleteAccount(self):
        tbdAccount = functions.elementFromList(self.accounts) # tbd: to be deleted

        if tbdAccount != None:
            self.accounts.remove(tbdAccount)
            print(translations.accountDeleted[langIndex])
            return True

        else:
            if len(self.accounts) > 0:
                print(translations.noAccountsDeleted[langIndex])
            return False


class account:
    def __init__(self, id: str, balance: float) -> None:
        self.id = id.lower()
        self.balance = 0

        self.movements = []
        self.informations = []

        self.isOpen = functions.approve(self.id + ", " + str(balance))

        if self.isOpen:
            print(translations.accountCreated[langIndex])
            self.movement("---", translations.accountCreated[langIndex], balance, noConfirmation=True)
        else:
            print(translations.accountNotCreated[langIndex])

    def __str__(self) -> str:
        if not self.isOpen:
            return translations.accountId[langIndex] + self.id + " - " + translations.closedAccount[langIndex]

        returnString = translations.accountId[langIndex] + self.id
        returnString += translations.currentBalanceTab[langIndex] + str(round(self.balance, 2))

        if self.balance < 0:
            returnString += " (!)"

        if self.isOpen:
            returnString += translations.currentlyOpenAccountTab[langIndex]
        else:
            returnString += translations.currentlyClosedAccountTab[langIndex]

        return returnString
    
    def details(self):
        print(translations.accountInformations[langIndex] + self.id)

        for fInformations in self.informations:
            print("\t" + fInformations)

        if len(self.informations) == 0:
            print(translations.nothingToSeeHereTab[langIndex])

        if self.isOpen:
            print(translations.currentlyOpenAccount[langIndex])
        else:
            print(translations.currentlyClosedAccount[langIndex])

        print(translations.accountMovements[langIndex] + self.id)

        for fMovements in self.movements:
            print("\t" + fMovements)

        if len(self.movements) == 0:
            print(translations.nothingToSeeHereTab[langIndex])
        
        print(translations.currentBalance[langIndex] + str(round(self.balance, 2)))

    def movement(self, week: str, reason: str, amount: float, noConfirmation=False) -> None:
        if amount > 0:
            movementString = (week + ": " + reason + ", +" + str(amount)).lower()
        else:
            movementString = (week + ": " + reason + ", " + str(amount)).lower()

        if not noConfirmation:
            if functions.approve(movementString) and self.isOpen:
                self.movements.append(movementString)
                self.balance += amount
                print(translations.movementAdded[langIndex])

                print(translations.currentBalance[langIndex] + str(round(self.balance, 2)))

            else:
                print(translations.movementNotAdded[langIndex])
                if not self.isOpen:
                    print(translations.currentlyClosedAccountNoReturn[langIndex])
                else:
                    print(translations.currentBalance[langIndex] + str(round(self.balance, 2)))
            
        else:
            self.movements.append(movementString)
            self.balance += amount
    
    def cancelMovement(self):
        tbcMovement = functions.elementFromList(self.movements) # tbc: to be cancelled

        if tbcMovement != None:
            tbcMovementAmount = float(tbcMovement.split(" ")[-1])
            self.movements.remove(tbcMovement)
            self.balance -= tbcMovementAmount

            print(translations.movementCancelled[langIndex])
            return True

        else:
            if len(self.movements) > 0:
                print(translations.noMovementsCancelled[langIndex])

            return False

    def editMovement(self):
        tbeMovement = functions.elementFromList(self.movements) # tbe: to be edited

        if tbeMovement != None:
            oldAmount = tbeMovement.split(" ")[-1]
            oldWeek = tbeMovement.split(": ")[0]

            newReason = functions.stringInput(translations.movementReasonRequest[langIndex])
            newAmount = round(functions.numericalInput(translations.movementAmountRequest[langIndex]), 2)

            self.balance -= float(oldAmount)
            self.balance += newAmount

            if newAmount > 0:
                newMovementString = oldWeek + ": " + newReason + ", +" + str(newAmount)

            else:
                newMovementString = oldWeek + ": " + newReason + ", " + str(newAmount)

            if functions.approve(newMovementString):
                self.movements[self.movements.index(tbeMovement)] = newMovementString

                print(translations.movementEdited[langIndex])
                return True
            
            else:
                print(translations.noMovementsEdited[langIndex])
                return False

        else:
            if len(self.movements) > 0:
                print(translations.noMovementsEdited[langIndex])
            return False

    def information(self, field: str, value: str) -> None:
        informationString = (field + ": " + value).lower()

        if functions.approve(informationString):
            print(translations.informationAddded[langIndex])
            self.informations.append(informationString)

        else:
            print(translations.informationNotAdded[langIndex])

    def deleteInformation(self):
        tbdInformation = functions.elementFromList(self.informations) # tbd: to be deleted

        if tbdInformation != None:
            self.informations.remove(tbdInformation)
            print(translations.informationDeleted[langIndex])
            return True

        else:
            if len(self.informations) > 0:
                print(translations.noInformationsDeleted[langIndex])
            return False

    def informationsReorder(self):
        rangeLen = len(self.informations)

        for x in range(rangeLen):
            for y in range(x, rangeLen):
                try:
                    if self.informations[y][0] > self.informations[y + 1][0]:
                        self.informations[y], self.informations[y + 1] = self.informations[y + 1], self.informations[y]
                except(IndexError):
                    continue