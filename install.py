import json
from operator import concat
import sys


class Config:
    def __init__(self, cloneTo, backupTo, envFiles, token):
        self.cloneTo = cloneTo
        self.backupTo = backupTo
        self.envFiles = envFiles
        self.token = token
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def printMembers(self):
        print('configuration:')
        print('')
        print('\t- Clones to: ' + self.cloneTo)
        print('')
        print('\t- Backups at: ' + self.backupTo)
        print('')
        print('\t- Env files at: ' + self.token)

        
        

def logErr(msg):
    print("\033[91m {}\033[00m" .format(msg))


def configure() -> Config:
    ok = False
    configuration = None
    while not ok:
        print('')
        print('Where should the project be cloned to? (absolute path)')
        clonePath = str(input())
        print('')
        print('Where are the projects .env files? (absolute path)')
        envFiles = str(input())
        print('')
        print('Where should the database backups go to? (absolute path)')
        backup = str(input())
        print('')
        print('Github developer token ')
        token = str(input())

        configuration = Config(clonePath, backup, envFiles, token)

        print('')

        configuration.printMembers()

        print('')
        print('Are these values ok? (y or n)')
        
        isOk = str(input())

        if isOk == 'y':
            ok = True

        

    with open('config.json', 'w') as outfile:
        json.dump(configuration.toJSON(), outfile)
        print('')
        print('Sucessfully configured')

    return configuration




def checkConfig() -> bool:
    isConfigured = True
    try:
        open("./config.json")
    except IOError:
        isConfigured =  False

    return isConfigured


def loadConfig() -> Config:
    fileContent = open('./config.json', 'r').read()
    dict =  json.loads(fileContent)
    print(Config(**dict))



def printHelp():
    print('')
    print('install')
    print('\t- saves database snapshot then clones the repo and runs docker compose (needs configuration first)')
    print('configure')
    print('\t- to configure deployments')
    print('')

def install(configuration: Config):
    print(configuration.backupTo)

    


def main():
    args = sys.argv
    try:
        arg = args[1]
        if arg.upper() == 'HELP':
            printHelp()
        elif arg.upper() == 'INSTALL':
            if checkConfig():
                install(loadConfig())
            else:
                logErr('Install not possible configure first')
        elif arg.upper() == 'CONFIGURE':
            if checkConfig():
                logErr('Deployments already configured. Delete config file to reconfigure.')
            else:
                configure()
        else:
            print('Argument: \'' + arg + '\' unknown type \'help\' for options')
    except Exception as e:
        if isinstance(e, IndexError):
            print('No argument. Type \'help\' for options')
        else:
            print(str(e))
    
    
    

if __name__ == "__main__":
    main()