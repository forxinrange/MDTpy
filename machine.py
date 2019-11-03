import sys
import os
import platform
import time
import datetime
import textwrap

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
        self.bomFixMachines = 'bugged_devices.txt'

class main():
    def __init__(self):
        self.cTools = OSTools()
        self.activeMachine = machine()
        self.firstBoot = True
        self.csv = csvFile() 
        self.previousAsset = 'Not Set'

    def Header(self):
        message = '---------------Machine Details Tool - UCLAN---------------'
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

        # Madcap logic for troublesome legacy HP devices...
        if(self.activeMachine.problemDevice == True):

            uuidStrip = uuidList[1].replace("-", '')
            uuid_breakout = textwrap.wrap(uuidStrip, 2)
            section_c = uuid_breakout[len(uuid_breakout)//2:]
            section_a = uuid_breakout[:len(uuid_breakout)//4]
            section_a = list(reversed(section_a))
            section_b = uuid_breakout[len(uuid_breakout)//4:len(uuid_breakout)//2]

            for x in range(len(section_b)):
                mem_store = ''
                if(x%2 == 0):
                    mem_store = section_b[x]
                    section_b[x] = section_b[x+1]
                    section_b[x+1] = mem_store
                else:
                    pass

            self.activeMachine.UUIDno = ''
            for x in range(len(section_a)):
                self.activeMachine.UUIDno += section_a[x]
            
            for x in range(len(section_b)):
                self.activeMachine.UUIDno += section_b[x]

            for x in range(len(section_c)):
                self.activeMachine.UUIDno += section_c[x]

        else:
            uuidStrip = uuidList[1].replace("-", '')
            self.activeMachine.UUIDno = uuidStrip

    def import_problem_devices(self):
        bom_bug_file_present = os.path.isfile(self.csv.bomFixMachines)
        if(bom_bug_file_present == False):
            writer = open(self.csv.bomFixMachines,'w')
            writer.close()
        
        with open(self.csv.bomFixMachines) as f:
            self.problem_devices = f.readlines()


    def identify_problem_device(self):
        if(str(self.activeMachine.model) in self.problem_devices):
            self.activeMachine.problemDevice = True

    def getModel(self):
        machineList = os.popen('wmic csproduct get name').read()
        machineModel = machineList.split()
        if(len(machineModel) > 1):

            for x in range(len(machineModel)-1):

                if(x == 0):
                    self.activeMachine.model = str(machineModel[x+1]) + ' '
                elif(x == len(machineModel)-2):
                    self.activeMachine.model += str(machineModel[x+1])
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
            print('Stored asset to increment: ',self.previousAsset)
            print('')
            readAsset = input('Please input asset number or press enter to try and auto increment: ')
            if(readAsset == ''):
                loopval = self.incrementAsset(self.previousAsset)
            else:
                self.activeMachine.assetNumber = str(readAsset)
                loopval = False
        self.writeStored(str(self.activeMachine.assetNumber))
    
    def printDetails(self):
        #print('            Time:',self.timeGet
        print('    Asset Number:',self.activeMachine.assetNumber)
        print('   Computer Name:',self.activeMachine.computerName)
        print('   Serial Number:',self.activeMachine.serialNumber)
        print('            UUID:',self.activeMachine.UUIDno)
        print('    UUID BOM Fix:',self.activeMachine.problemDevice)
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
        csvFile.write(str('U'))
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
        self.import_problem_devices()
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