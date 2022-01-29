import translations
from translations import langIndex

def approve(string: str) -> bool:
    while True:
        approval = str(input(translations.approveMessage[langIndex] + string + translations.ynMessage[langIndex])).lower()

        if approval == translations.cmd_yes[langIndex]:
            return True
        elif approval == translations.cmd_no[langIndex]:
            return False

def elementFromList(lst: list) -> str:
    if len(lst) == 0:
        return None

    while True:
        print(translations.indexSelection[langIndex])

        index = 0

        for fLst in lst:
            print(str(index) + " - " + str(fLst))

            index += 1

        try:
            indexChosen = int(input(translations.indexRequest[langIndex] + str(len(lst) - 1) + "]: "))

        except(EOFError):
            return None
        
        except(ValueError):
            continue

        if indexChosen in range(len(lst)):
            return lst[indexChosen]

def stringInput(request: str) -> str:
    while True:
        answer = str(input(request))

        if answer != "":
            return answer

def numericalInput(request: str) -> float:
    while True:
        try:
            answer = float(input(request))
            return answer

        except(ValueError):
            continue