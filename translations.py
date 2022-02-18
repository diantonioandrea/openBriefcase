import os, pickle, sys
import functions

# indexes -> en: 0, it: 1

languages = ["English", "Italian"]
langIndex = 0 # default value

if not os.path.exists(str(os.getcwd()) + "/Data/Language.l"): # language setting <- only in english
    print("Entering language definition UI")

    newLanguageFile = open(str(os.getcwd()) + "/Data/Language.l", "wb")

    while True:
        print("\nSelect one element from the list by the index\n")

        index = 0

        for fLanguages in languages:
            print(str(index) + " - " + str(fLanguages))

            index += 1

        try:
            indexChosen = int(input("\nChoose an element in [0, " + str(len(languages) - 1) + "]: "))
        
        except(ValueError, KeyboardInterrupt, EOFError):
            continue

        if indexChosen in range(len(languages)):
            break

    langIndex = indexChosen

    pickle.dump(langIndex, newLanguageFile)

    newLanguageFile.close()

    print("Exiting language definition UI")

else:
    languageFile = open(str(os.getcwd()) + "/Data/Language.l", "rb")
    langIndex = pickle.load(languageFile)
    languageFile.close()

# outputs

# openBriefcase.py

startupMessage = ["openBriefcase, open-source, CLI accounting utility\n" + 
"Developer: Andrea Di Antonio", 
"openBriefcase, strumento open-source di contabilità con interfaccia CLI\n" + 
"Sviluppatore: Andrea Di Antonio"]

exCmdMessage = ["\nExit with Ctrl+d [G/L] or Ctrl+z and Enter [Win]", "\nUscire con Ctrl+d [G/L] o Ctrl+z e Invio [Win]"]

exMessage = ["\nExiting", "\nUscita"]

welcomeMessage = ["\nWelcome back ", "\nBentornato "]
usernameRequest = ["\nUsername: ", "\nNome utente: "]
lastLogoutMessage = ["Last logout: ", "Ultima disconnessione: "]

enUserCreationUI = ["\nEntering user creation UI\n", "\nIngresso nell'interfaccia di creazione utente\n"]
createdUserMessage = ["\nCreated user: ", "\nUtente creato: "]
noCreatedUserMessage = ["New user not created\n", "Nuovo utente non creato\n"]
exUserCreationUI = ["\nExiting user creation UI", "\nUscita dall'interfaccia di creazione utente"]

createAccountMessage = ["\nCreate an account first", "\nDevi prima creare un conto"]

enAccountCreationUI = ["\nEntering account creation UI", "\nIngresso nell'interfaccia di creazione conto"]
accountNameRequest = ["\nNew account name: ", "\nNome del nuovo conto: "]
accountBalanceRequest = ["New account starting balance: ", "Bilancio iniziale del nuovo conto: "]
exAccountCreationUI = ["\nExiting account creation UI", "\nUscita dall'interfaccia di creazione conto"]

enAccountDeletionUI = ["\nEntering account deletion UI", "\nIngresso nell'interfaccia di eliminazione conto"]
exAccountDeletionUI = ["\nExiting account deletion UI", "\nUscita dall'interfaccia di eliminazione conto"]

enMainUI = ["\nEntering main UI\nType 'help' to get help", "\nIngresso nell'interfaccia principale\nInserire 'aiuto' per ottenere aiuto"]
exMainUI = ["\nSaving and exiting main UI\nSee you next time", 
"\nUscita dall'interfaccia di principale\nAlla prossima"]

accountClosed = ["\nAccount closed", "\nConto chiuso"]
accountAlreadyClosed = ["\nAccount is already closed", "\nConto già chiuso"]
accountOpened = ["\nAccount opened", "\nConto aperto"]
accountAlreadyOpened = ["\nAccount is already opened", "\nConto già aperto"]

enMovementCreationUI = ["\nEntering movement creation UI", "\nIngresso nell'interfaccia di creazione movimenti"]
movementeFormatMessage = ["\nFormat -> week: reason, amount", "\nFormato -> settimana: causale, somma"]
movementReasonRequest = ["\nNew movement reason: ", "\nCausale del nuovo movimento: "]
movementAmountRequest = ["New movement amount: ", "Somma del nuovo movimento: "]
exMovementCreationUI = ["\nExiting movement creation UI", "\nUscita dall'interfaccia di creazione movimenti"]

enMovementCancellationUI = ["\nEntering movement cancellation UI", "\nIngresso nell'interfaccia di annullamento movimenti"]
exMovementCancellationUI = ["\nExiting movement cancellation UI", "\nUscita dall'interfaccia di annullamento movimenti"]

enMovementEditUI = ["\nEntering movement editing UI", "\nIngresso nell'interfaccia di modifica movimenti"]
exMovementEditUI = ["\nExiting movement editing UI", "\nUscita dall'interfaccia di modifica movimenti"]

enInformationCreationUI = ["\nEntering information creation UI", "\nIngresso nell'interfaccia di creazione informazioni"]
infoFormatMessage = ["\nFormat -> field: value", "\nFormato -> campo: valore"]
informationFieldRequest = ["\nNew information field: ", "\nCampo della nuova informazione: "]
informationValueRequest = ["New information value: ", "Valore della nuova informazione: "]
exInformationCreationUI = ["\nExiting information creation UI", "\nUscita dall'interfaccia di creazione informazioni"]

enInformationDeletionUI = ["\nEntering information Deletion UI", "\nIngresso nell'interfaccia di eliminazione informazioni"]
exInformationCreationUI = ["\nExiting information deletion UI", "\nUscita dall'interfaccia di eliminazione informazioni"]

homeHelp = ["\ndetails: show details\naccounts: move to accounts environment\n" + 
"new accounts: create new accounts\ndelete accounts: delete old accounts", 
"\ndettagli: mostra i dettagli del profilo\nconti: passa all'ambiente dei conti\n" + 
"nuovi conti: crea nuovi conti\nelimina conti: elimina vecchi conti"]

accountsHelp = ["\ndetails: show details\nclose: close account\nopen: open account\n" +
"new movements: create new movements\ncancel movements: calcel old movements\n" +
"new informations: create new informations\ndelete informations: delete old informations\n" +
"edit movements: edit reason and amount of old movements\n" + "cancel movements: cancel old movements", 
"\ndettagli: mostra i dettagli del conto\nchiudi: chiudi il conto\napri: apri il conto\n" +
"nuovi movimenti: crea nuovi movimenti\nannulla movimenti: annulla vecchi movimenti\n" +
"nuove informazioni: aggiungi nuove informazioni\elimina informazioni: elimina vecchie informazioni\n" + 
"modifica movimenti: modifica causale e somma di vecchi movimenti\n" +
"annulla movimenti: annulla vecchi movimenti"]

unexpectedError = ["\nUnexpected error", "\nErrore inaspettato"]

# functions.py

approveMessage = ["Approve: \"", "Approvare: \""]
ynMessage = ["\"? [y/n]: ", "\"? [s/n]: "]
indexSelection = ["\nSelect one element from the list by the index\n", "\nScegli un elemento dalla lista tramite l'indice\n"]
indexRequest = ["\nChoose an element in [0, ", "\nScegli un elemento in [0, "]

# classes.py

userCurrentSituation = ["\nCurrent situation for user: ", "\nSituazione atttuale per l'utente: "]
accountsMessage = ["\nAccounts:", "\nConti:"]

currentBalance = ["\nCurrent balance: ", "\nBilancio attuale: "]
currentBalanceTab = ["\n\tCurrent balance: ", "\n\tBilancio attuale: "]

accountCreated = ["Account succesfully created", "Conto creato con successo"]
accountNotCreated = ["Account creation denied", "Creazione del conto impedita"]

accountId = ["Account id: ", "Identificativo conto: "]
closedAccount = ["closed", "chiuso"]

currentlyClosedAccount = ["\nAccount is currently closed", "\nConto attualmente chiuso"]
currentlyClosedAccountNoReturn = ["Account is currently closed", "Conto attualmente chiuso"]
currentlyOpenAccount = ["\nAccount is currently open", "\nConto attualmente aperto"]
currentlyClosedAccountTab = ["\n\tAccount is currently closed", "\n\tConto attualmente chiuso"]
currentlyOpenAccountTab = ["\n\tAccount is currently open", "\n\tConto attualmente aperto"]

accountDeleted = ["\nSelected account deleted", "\nConto selezionato eliminato"]
noAccountsDeleted = ["\nNo accounts deleted", "\nNessun conto eliminato"]

accountInformations = ["\nInformations of account: ", "\nInformazioni del conto: "]
accountMovements = ["\nMovements of account: ", "\nMovimenti del conto: "]

movementCancelled = ["\nSelected movements cancelled", "\nMovimento selezionato annullato"]
noMovementsCancelled = ["\nNo movements cancelled", "\nNessun movimento annullato"]

movementEdited = ["\nSelected movements edited", "\nMovimento selezionato modificato"]
noMovementsEdited = ["\nNo movements edited", "\nNessun movimento modificato"]

movementAdded = ["\nMovement added", "\nMovimento aggiunto"]
movementNotAdded = ["\nMovement not added", "\nMovimento non aggiunto"]

informationAddded = ["\nInformation added", "\nInformazione aggiunta"]
informationNotAdded = ["\nInformation not added", "\nInformazione non aggiunta"]

informationDeleted = ["\nSelected information deleted", "\nInformazione selezionata eliminata"]
noInformationsDeleted = ["\nNo informations deleted", "\nNessuna informazione eliminata"]

nothingToSeeHere = ["\nNothing to see here", "\nNiente da mostrare qui"]
nothingToSeeHereTab = ["\tNothing to see here", "\tNiente da mostrare qui"]

# inputs

cmd_help = ["help", "aiuto"]
cmd_details = ["details", "dettagli"]
cmd_new = ["new", "nuovi", "nuove"] # multiple italian translations
cmd_accounts = ["accounts", "conti"]
cmd_close = ["close", "chiudi"]
cmd_open = ["open", "apri"]
cmd_edit = ["edit", "modifica"]
cmd_movements = ["movements", "movimenti"]
cmd_informations = ["informations", "informazioni"]
cmd_cancel = ["cancel", "annulla"]
cmd_delete = ["delete", "elimina"]

cmd_yes = ["y", "s"]
cmd_no = ["n", "n"]