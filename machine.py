import sys
import os
import platform
import time
import datetime

class OSTools():
    def __init__(self):
        pass
    
    def detectOS(self):
        value = platform.system()
        if(value == 'Windows'):
            return 1
        elif(value == 'Darwin'):
            return 2
        elif(value == 'Linux'):
            return 3
        else:
            return 4

    def clearConsole(self):
        operatingSystem = self.detectOS()
        if(operatingSystem == 1):
            os.system('cls')
        elif(operatingSystem == 2):
            os.system('clear')
        elif(operatingSystem == 3):
            os.system('clear')
        else:
            print('Unknown operating system')

class machine():
    def __init__(self):
        self.assetNumber = 'Not Set'
        self.serialNumber = 'default'
        self.UUIDno = 'default'
        self.computerName = 'default'
        self.macAddress = []
        self.model = 'default'
        self.problemDevice = False

class csvFile():
    def __init__(self):
        self.csvName = 'Details.csv'
        self.storeName = 'dat.gus'

class main():
    def __init__(self):
        self.cTools = OSTools()
        self.activeMachine = machine()
        self.firstBoot = True
        self.csv = csvFile()
        self.previousAsset = 'Not Set'

    def Header(self):
        message = '---------------Machine Details Tool---------------'
        if(self.firstBoot == True):
            for x in range(len(message)):
                print(message[x],end='',flush=True)
                time.sleep(.015)
            self.firstBoot = False
        else:
            print(message)
        print('\n')

    def genTemplate(self):
        csvPresent = os.path.isfile(self.csv.csvName)
        if(csvPresent == True):
            pass
        else:
            csvTemplate = open(self.csv.csvName,'w')
            csvTemplate.write('Asset Number')
            csvTemplate.write(',')
            csvTemplate.write('Computer Name')
            csvTemplate.write(',')
            csvTemplate.write('Serial Number')
            csvTemplate.write(',')
            csvTemplate.write('UUID')
            csvTemplate.write(',')
            csvTemplate.write('MAC')
            csvTemplate.write('\n')
            csvTemplate.close()

    def getStored(self):
        storeFilePresent = os.path.isfile(self.csv.storeName)
        if(storeFilePresent == True):
            pass
        else:
            writer = open(self.csv.storeName,'w')
            writer.write('none')
            writer.close()
        writer = open(self.csv.storeName,'r')
        value = writer.readline()
        writer.close()
        self.previousAsset = (str(value))
    
    def writeStored(self,asset):
        writer = open(self.csv.storeName,'w')
        writer.write(asset)
        writer.close()

    def getComputerName(self):
        cnameGet = os.popen("hostname").read()
        cnameList = cnameGet.split()
        self.activeMachine.computerName = cnameList[0]
    
    def getSerial(self):
        serialGet = os.popen('wmic bios get serialnumber').read()
        serialList = serialGet.split()
        self.activeMachine.serialNumber = serialList[1]

    def getUUID(self):
        uuidGet = os.popen('wmic csproduct get "UUID"').read()
        uuidList = uuidGet.split()
        if(self.activeMachine.problemDevice == True):
            pass
        else:
            self.activeMachine.UUIDno = uuidList[1]

    def identify_problem_device(self):
        problem_devices = ['HP ProBook 6360b','test','Surface Book']
        if(self.activeMachine.model in problem_devices):
            self.activeMachine.problemDevice = True

    def getModel(self):
        machineList = os.popen('wmic csproduct get name').read()
        machineModel = machineList.split()
        if(len(machineModel) > 1):
            for x in range(len(machineModel)-1):
                if(x == 0):
                    self.activeMachine.model = str(machineModel[x+1]) + ' '
                else:
                    self.activeMachine.model += str(machineModel[x+1]) + ' '
    
    def getMac(self):
        macGet = os.popen('wmic nic get MACaddress').read()
        macList = macGet.split()
        for x in range(len(macList)):
            if(macList[x] != '' and macList[x] != 'MACAddress'):
                self.activeMachine.macAddress.append(macList[x])

    def incrementAsset(self,assetValue):
        try:
            intAsset = int(assetValue)
            intAsset = intAsset + 1
            print('')
            print('Will increment to',intAsset)
            print('')
            print('Press enter to accept value...')
            input('')
            self.activeMachine.assetNumber = intAsset
            return False
        except ValueError:
            print('Previous asset contains letters therefore unable to increment...')
            print('')
            return True

    def getAsset(self):
        print('')
        loopval = True
        while(loopval == True):
            print('Stored asset for incrementation: ',self.previousAsset)
            print('')
            readAsset = input('Please input asset number or press enter to try automatic incrementation: ')
            if(readAsset == ''):
                loopval = self.incrementAsset(self.previousAsset)
            else:
                self.activeMachine.assetNumber = str(readAsset)
                loopval = False
        self.writeStored(str(self.activeMachine.assetNumber))
    
    def printDetails(self):
        print('            Time:',self.timeGet)
        print('    Asset Number:',self.activeMachine.assetNumber)
        print('   Computer Name:',self.activeMachine.computerName)
        print('   Serial Number:',self.activeMachine.serialNumber)
        print('            UUID:',self.activeMachine.UUIDno)
        print('           Model:',self.activeMachine.model)
        print('    Mac Adresses: ',end='')
        for x in range(len(self.activeMachine.macAddress)):
            if(x == 0):
                print(self.activeMachine.macAddress[x])
            else:
                print('                 ',self.activeMachine.macAddress[x])
    
    def writeCSV(self):
        print('')
        print('Press enter to write the stored values to disk...')
        input('')
        csvFile = open(self.csv.csvName,'a')
        csvFile.write(str(self.activeMachine.assetNumber))
        csvFile.write(',')
        csvFile.write(str(self.activeMachine.computerName))
        csvFile.write(',')
        csvFile.write(str(self.activeMachine.serialNumber))
        csvFile.write(',')
        csvFile.write(str(self.activeMachine.UUIDno))
        csvFile.write(',')
        for x in range(len(self.activeMachine.macAddress)):
            if(x == len(self.activeMachine.macAddress)-1):
                csvFile.write(str(self.activeMachine.macAddress[x]))
            else:
                csvFile.write(str(self.activeMachine.macAddress[x]))
                csvFile.write(',')
        csvFile.write('\n')
        csvFile.close()
        print('')
        print('Data has been written to disk...')
        print('')
        input('Press enter to exit...')

    def check_time(self):

        self.timeGet = datetime.datetime.now()

    def sequenceStart(self):
        self.cTools.clearConsole()
        self.check_time()
        self.Header()
        self.genTemplate()
        self.getStored()
        self.getComputerName()
        self.getModel()
        self.identify_problem_device()
        self.getMac()
        self.getSerial()
        self.getUUID()
        self.printDetails()
        self.getAsset()
        self.cTools.clearConsole()
        self.Header()
        self.printDetails()
        self.writeCSV()

root = main()
root.sequenceStart()