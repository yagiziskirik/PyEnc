#!/opt/homebrew/bin/python3

import random
import string
import pyperclip
import argparse

class PyEnc:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="PyEnc", description="Encrypt and decrypt texts via passphrase")

        self.parser.add_argument("-c", "--clip", help="take the argument from the clipboard", action="store_true")
        self.parser.add_argument("-m", "--message", help="add your message", type=str)
        self.parser.add_argument("-k", "--key", help="include your key here", type=str)
        self.parser.add_argument("-d", "--decrypt", help="change action to decrypt", action="store_true")
        self.parser.add_argument("-e", "--encrypt", help="change action to encrypt", action="store_true")
        self.parser.add_argument("-r", "--recursive", help="recursively run the messages action", action="store_true")

        self.args = self.parser.parse_args()

        self.MSG = ""
        self.KEY = ""
        self.INC = ""
        self.retVal = ""
        self.RECURSIVE = False

        self._argParser()
        self.NEW_KEYS = self._key_generator()

        self.processMsg()
        keyChanges = False
        methodChanges = False

        if self.RECURSIVE:
            keyChangesInp = input("Does the key change? (y/N): ")
            keyChanges = keyChangesInp == "y" or keyChangesInp == "Y"
            methodChangesInp = input("Does the encrypt type change? (y/N): ")
            methodChanges = methodChangesInp == "y" or methodChangesInp == "Y"
        
        while self.RECURSIVE:
            self.MSG = input("Message: ")
            if keyChanges:
                self.KEY = input("Key: ")
            if methodChanges:
                inc = input("Encrypt (Y/n): ")
                self.INC = inc == "" or inc == "y" or inc == "Y"
            self.retVal = ""
            self.NEW_KEYS = self._key_generator()
            self.processMsg()

    def _argParser(self):
        if self.args.recursive:
            self.RECURSIVE = True
        if self.args.clip:
            self.MSG = pyperclip.paste()
        elif self.args.message:
            self.MSG = self.args.message
        else:
            self.MSG = input('Message: ')

        if self.args.key:
            self.KEY = self.args.key
        else:
            self.KEY = input('Key: ')

        if self.args.encrypt:
            self.INC = True
        elif self.args.decrypt:
            self.INC = False
        else:
            inc = input('Encrypt (Y/n): ')
            self.INC = inc == "" or inc == "y" or inc == "Y"

    def _key_generator(self):
        random.seed(self.KEY)
        tempList = list(map(str, string.ascii_letters + string.digits + string.punctuation + " "))
        temp_keys = ""
        for _ in range(len(tempList)):
            temp_keys += tempList.pop(random.choice(range(len(tempList))))
        return temp_keys

    def _get_pos_nums(self, num):
        pos_nums = []
        for _ in range(num):
            pos_nums.append(random.randint(0, 9))
        return pos_nums


    def encrypt(self, msg):
        l = len(msg)
        rand = self._get_pos_nums(l)
        encMsg = ""
        for i, char in enumerate(msg):
            currIndex = self.NEW_KEYS.index(char)
            newIndex = rand[i] + currIndex if rand[i] + currIndex < len(self.NEW_KEYS) else rand[i] + currIndex - len(self.NEW_KEYS)
            encMsg += self.NEW_KEYS[newIndex]
        pyperclip.copy(encMsg)
        return encMsg

    def decrypt(self, msg):
        l = len(msg)
        rand = self._get_pos_nums(l)
        decMsg = ""
        for i, char in enumerate(msg):
            currIndex = self.NEW_KEYS.index(char)
            newIndex = currIndex - rand[i] if currIndex - rand[i] > 0 else currIndex - rand[i] + len(self.NEW_KEYS)
            decMsg += self.NEW_KEYS[newIndex]
        return decMsg

    def processMsg(self):
        if self.INC:
            if "\n" in self.MSG:
                tempVal = self.MSG.split("\n")
                retTempVal = []
                for val in tempVal:
                    retTempVal.append(self.encrypt(val))
                    self.NEW_KEYS = self._key_generator()
                self.retVal = "\n".join(retTempVal)
            else:
                self.retVal = self.encrypt(self.MSG)
        else:
            if "\n" in self.MSG:
                tempVal = self.MSG.split("\n")
                retTempVal = []
                for val in tempVal:
                    retTempVal.append(self.decrypt(val))
                    self.NEW_KEYS = self._key_generator()
                self.retVal = "\n".join(retTempVal)
            else:
                self.retVal = self.decrypt(self.MSG)

        print(f"Your response: {self.retVal}.")
        if self.INC:
            pyperclip.copy(self.retVal)
            print("It is copied to your clipboard, have a nice day.")


if __name__ == "__main__":
    PyEnc()