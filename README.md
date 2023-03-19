# printer-automation
it's pretty much what you would think it is. If you have a printer and want to automate printing files you could use this little script. It does use gmail but generally you could do it with any mail provider.

A few things to note here:
1. The script is really simple and I made it as such for a reason but simplicity comes at a cost. It doesn't do any actual checks so you might have to some more setup and be a little inconvienienced but that's ok with you right?
2. While I said most of the things I wanted to say here in the script file itself I will also say them here again

External libraries to download:
pyautogui 

you can download it in windows by opening cmd and typing py -m pip install pyautogui or just pip install pyautogui

Note that you also need to have pip installed 


This works with a lot of mail providers but you need to search if your specific provider allows it. The major ones do and this script specifically uses google's gmail.
You can check this here: https://www.systoolsgroup.com/imap/

Massive credit to baali and all of the people in the comments here - https://gist.github.com/baali/2633554 - if it weren't for them I'd have to spend hours debugging different things

In order to change username, password, host, directories and other details you should open the files in a code editor and change the first 8 variables. I have explained in comments in detial about what to cahnge them to and little details about them.


I might also make a repository (or just add it here) with the original printer automation script I made which is simpler than that one and does work but might not be as useful. 
