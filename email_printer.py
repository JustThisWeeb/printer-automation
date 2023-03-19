import os
from time import sleep
import imaplib
import email
from email.header import decode_header

import pyautogui # py -m pip install pyautogui or alternatively pip install pyautogui

import shutil
import sys


#Instead of having a readme I am just going to say a few things here
#First of all this script is really simple. It doesn't really check for a lot of things which might be nice (I am kinda too lazy to add them) so you need to prepare a few things in advance.
#hmm I was planning on saying a few more things but that's it for those statements.
# anyways the variables below are the only ones you really need to change according to your system.

host = "imap.gmail.com" # you could change this one to whatever service uses imap. You could take a look at this site https://www.systoolsgroup.com/imap/ to see if your mail provider has it
username = "your email here" #you might want to make a new google account for this
password = "your password here" # Do note that for this script you need to enable apps access from https://myaccount.google.com/apppasswords (you also need to enable 2fa) and use the provided password
download_folder = "path" #note that this has only really been tested on windows. I might test it on a linux vm in the future though. It should theoretically work on both
#One thing to note about the download path - if you use windows you might use a path such as C:\Users\You\Some-Folder  but python doesn't like that so you need to add a second \ (and make it look like C:\\Users\\You\\Some-Folder)
printed_files_folder = "path" #This is where your printed files will be stored. If you don't want that you could delete lines 88 and 89
specfic_mailbox = "INBOX" # You can change that if you want to download all spam attachments for example... not sure why you would want that but you do you. Leave like this if you only want to scan inboxes.

#The way the printing is automated is kinda dumb but it works so... Yeah it just simulates a click on a certain part of the screen in order to click on the print button.
#I might also need to mention the fact that you need to set up your preferred printer as the default
pointer_x = 0
pointer_y = 0

while True:
    #This is the downloading part
    sleep(10) #I haven't done extensive tests on this so I am not sure if google would like a shorter delay. I would actually recommend something like 30 seconds just to be safe but 10 should also be fine. It's also not as strenuous to the network.
    print("searching for and downloading the file...")
    # credit to baali (https://gist.github.com/baali/2633554) for this one. I shortened the code a bit by removing a few parts and made it compatible with python 3.x but generally haven't changed most of it
    imap_session = imaplib.IMAP4_SSL('imap.gmail.com')
    typ, accountDetails = imap_session.login(username, password)
    if typ != 'OK':
        print('Not able to sign in!')

    imap_session.select(f'{specfic_mailbox}')
    typ, data = imap_session.search(None, 'ALL') #change this if you only want to download only unseen files for example
    if typ != 'OK':
        print('Error searching Inbox.')

    for msg_id in data[0].split():
        typ, message_parts = imap_session.fetch(msg_id, '(RFC822)')
        if typ != 'OK':
            print('Error fetching mail.')

        email_body = message_parts[0][1]
        mail = email.message_from_bytes(email_body)
        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            file_name = part.get_filename()

            if file_name:
                file_path = f"{download_folder}\\{file_name}" #one small note here - If the name of the file is not latin it could cause some troubles
                if not os.path.isfile(file_path):
                    fp = open(file_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
        imap_session.close()
        imap_session.logout()

        print('Done')

    #Here comes the printing part!
    sleep(1)
    #If you think this part looks odd and not in place with the rest of the code then you're right. I copy pasted this one from my other project which automated printing using a file server.
    #Initially it was supposed to look if there were new files in a print folder and if there were to print them. Unfortunately while the code worked other circumstances prevented me from using it but I found a way to recycle it
    print("Printing the files...")
    path = download_folder
    dir_list = os.listdir(path)
    if len(dir_list) > 0:
        print(f"received {len(dir_list)} files...")
        for file in dir_list:
            try:
                os.startfile(f"{path}\\{file}", "print") # again this was only used in windows for reasons I will not disclose so the \\ are there because of windows.
                print(
                    f"printing {file}...\nThe file will be automatically deleted after 60 seconds (and will be moved to the '\\all printed files' directory where you can find all printed files)")
                sleep(3) #this is accounting for the lag. You may want to change that depending on how slow your device is. 3 seems like a good default for most systems though.
                pyautogui.click(x=pointer_x, y=pointer_y)
                sleep(60)
                shutil.move(f"{path}\\{file}", f"{printed_files_folder}")
                os.remove(f"{path}\\{file}")
                print(f"removed {file}")
                continue
            except:
                print("Error when printing the file. Check if the file is of a supported printing format")
    else:
        print("no files found...")