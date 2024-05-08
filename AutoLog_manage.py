
from cryptography.fernet import Fernet
from PIL import Image
import getpass


def binary_to_integer(binary):
    power = 0
    value = 0
    for i in range(len(binary)-1, -1, -1):
        value += int(binary[i]) * 2 ** power
        power += 1
    return value


def get_key():
    image_saveable = Image.open("image.png")
    image = image_saveable.load()

    key = ""

    for row in range(44):
        binary = ""
        for column in range(8):
            binary += "0" if image[column, row][0] % 2 == 0 else "1"
        key += chr(binary_to_integer(binary))

    return key


def decrypt_text(text):
    cipher = Fernet(key)
    return cipher.decrypt(text).decode()


def encrypt_text(text):
    cipher = Fernet(key)
    return cipher.encrypt(text.encode()).decode()


def add_credential():
    file = open("credentials", "a")
    file.write(encrypt_text(platform) + "," + encrypt_text(username) + "," + encrypt_text(password) + "\n")
    file.close()


def remove_credential():
    file = open("credentials", "r").readlines()
    new_file = ""
    removed = False
    for row in file:
        n = row.split(",")
        if decrypt_text(n[0]) != platform:
            new_file += row
        else:
            removed = True

    file = open("credentials", "w")
    file.write(new_file)
    file.close()

    return removed

key = get_key()

while 1:
    command = input("What do you want to do? (add_credential(ac)/remove_credential(rc)/quit(q)): ").lower()

    if command == "add_credential" or command == "ac":
        platform, username, password = input("Platform: "), input("Username: "), getpass.getpass("Password: ")
        add_credential()
        print(f"Credential to {platform} added!")

    elif command == "remove_credential" or command == "rc":
        platform = input("Platform: ")
        if remove_credential():
            print(f"Credential to {platform} removed!")
        else:
            print(f"No credential to {platform} found!")

    elif command == "quit" or command == "q":
        break

