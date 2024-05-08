
from cryptography.fernet import Fernet
import pyautogui
import mouse
from PIL import Image
import pyperclip


def binary_to_integer(binary):
    power = 0
    value = 0
    for i in range(len(binary)-1, -1, -1):
        value += int(binary[i]) * 2 ** power
        power += 1
    return value


def get_key():
    image_savable = Image.open("image.png")
    image = image_savable.load()

    key = ""

    for row in range(44):
        binary = ""
        for column in range(8):
            binary += "0" if image[column, row][0] % 2 == 0 else "1"
        key += chr(binary_to_integer(binary))

    return key


def decrypt_text(encrypted_text):
    cipher = Fernet(key)
    decrypted_text = cipher.decrypt(encrypted_text).decode()
    return decrypted_text


def get_login_credentials():
    file = open("credentials", "r")
    credentials = {}
    for row in file:
        row = row.rstrip().split(",")
        credentials[decrypt_text(row[0])] = decrypt_text(row[1]), decrypt_text(row[2])
    return credentials


def get_url():
    pyautogui.leftClick()
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.hotkey('ctrl', 'c')
    return str(pyperclip.paste())


key = get_key()
credentials = get_login_credentials()
url = get_url()

pyautogui.leftClick()

for credential in credentials:
    if credential in url:
        username, password = credentials[credential][0], credentials[credential][1]

        pyautogui.write(username)

        mouse.wait()
        pyautogui.leftClick()

        pyautogui.write(password)

        pyautogui.press("Enter")
