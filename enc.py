import random
import string
import pyperclip

MSG = input('Message: ')
KEY = input('Key: ')
inc = input('Encrypt (Y/n): ')
INC = inc == "" or inc == "y" or inc == "Y"

random.seed(KEY)

tempList = list(map(str, string.ascii_letters + string.digits + string.punctuation + " "))
NEW_KEYS = ""

for _ in range(len(tempList)):
    NEW_KEYS += tempList.pop(random.choice(range(len(tempList))))

def get_pos_nums(num):
    pos_nums = []
    for _ in range(num):
        pos_nums.append(random.randint(0, 9))
    return pos_nums


def encrypt(msg):
    l = len(msg)
    rand = get_pos_nums(l)
    encMsg = ""
    for i, char in enumerate(msg):
        currIndex = NEW_KEYS.index(char)
        newIndex = rand[i] + currIndex if rand[i] + currIndex < len(NEW_KEYS) else rand[i] + currIndex - len(NEW_KEYS)
        encMsg += NEW_KEYS[newIndex]
    pyperclip.copy(encMsg)
    return encMsg

def decrypt(msg):
    l = len(msg)
    rand = get_pos_nums(l)
    decMsg = ""
    for i, char in enumerate(msg):
        currIndex = NEW_KEYS.index(char)
        newIndex = currIndex - rand[i] if currIndex - rand[i] > 0 else currIndex - rand[i] + len(NEW_KEYS)
        decMsg += NEW_KEYS[newIndex]
    return decMsg

retVal = ""
if INC:
    retVal = encrypt(MSG)
else:
    retVal = decrypt(MSG)

print(f"Your response: {retVal}.")
pyperclip.copy(retVal)
print("It is copied to your clipboard, have a nice day.")
