# THIS IS THE ORIGINAL CODE FROM main.exe AKA malehTerminal.exe IN PYTHON. CREATED BY MALEH
# FEEL FREE TO ADD SOME OWN CODE TO IT OR MAKE CHANGES TO EXISTING CODE

import time
import wget
import subprocess
import socket
import getpass
import platform
from tkinter import *
from termcolor import colored as col
import os

os.chdir(os.path.expanduser('~'))

try:
    with open(os.path.expanduser('~')+'\\malehTerminal\\settings.txt', 'r') as file:
        promptcolor, directorycolor = file.read().split('\n')
        print(promptcolor, directorycolor)
        PROMPT_COLOR = promptcolor.split(':')[1]
        DIRECTORY_COLOR = directorycolor.split(':')[1]
except:
    PROMPT_COLOR = 'green'
    DIRECTORY_COLOR = 'cyan'

CURRENT_DIRECTORY = os.getcwd()
PREFIX = col(f'{str(getpass.getuser())}@{str(platform.system())} ', PROMPT_COLOR) + col(CURRENT_DIRECTORY, DIRECTORY_COLOR) +  '$ '
PREFIX_STATUS = True

def error_message(value):
    return col(value, 'red')

installer_links = {'spotify':'https://download.scdn.co/SpotifySetup.exe',
                    'discord':'https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x86',
                    'python':'https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe',
                    'vscode':'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user',
                    'chrome':'https://www.google.com/intl/de_de/chrome/thank-you.html?statcb=1&installdataindex=empty&defaultbrowser=0#',
                    'tor':'https://www.torproject.org/dist/torbrowser/11.5/torbrowser-install-win64-11.5_en-US.exe'
                    }
installer_list = ['spotify','discord','python','vscode','tor']

class commands:
    def echo(text):
        if text.lower() == '$shell':
            return os.getcwd()
        else:
            return text
    def sudo(command):
        pass
    def touch(path):
        def create_file():
            with open(path, 'w') as f:
                f.close()
        if os.path.exists(path):
            if os.path.isdir(path):
                print(error_message('touch: You need to enter a file not a directory'))
            elif os.path.isfile(path):
                print(error_message('touch: File does already exists'))
        else:
            create_file()
    def cat(file_name):
        def print_message(path):
            with open(path, 'r') as file:
                print(file.read())
                file.close()
        if os.path.exists(file_name):
            if os.path.isdir(file_name):
                print(error_message(f'cat: {str(file_name)} is a directory'))
            elif os.path.isfile(file_name):
                print_message(file_name)
        elif os.path.exists(CURRENT_DIRECTORY+'/'+file_name):
            if os.path.isdir(file_name):
                print(error_message(f'cat: {str(file_name)} is a directory'))
            elif os.path.isfile(file_name):
                print_message(CURRENT_DIRECTORY+'/'+file_name)
        else:
            print(error_message(f'cat: No such file or directory'))
    def install(app, directory):
        apps = list(installer_links.keys())
        if app in apps:
            url = installer_links[app]
            try:
                wget.download(url, out=directory+'\\'+str(app)+'.exe')
                print(col(f'\nSuccessfully installed {str(app)} installer to {str(directory)}', 'green'))
                question = input(f'Do you want to install {str(app)} now?\n(Y/N))')
                if question.lower() == 'y':
                    subprocess.call(f'{str(directory)}\\{str(app)}.exe')
            except:
                print(error_message('There was an error while downloading the installer'))
            print('\n')
        else:
            print(error_message(f'A installer for "{str(app)}" does not exist'))

    def change_directory(directory):
        global CURRENT_DIRECTORY, PREFIX
        if directory.startswith('~'):
            directory = directory.replace('~', f'/home/{str(getpass.getuser())}')
        if directory == '..':
            before_path = os.path.dirname(CURRENT_DIRECTORY)
            os.chdir(before_path)
            CURRENT_DIRECTORY = before_path
            PREFIX = col(f'{str(getpass.getuser())}@{str(platform.system())} ', PROMPT_COLOR) + col(CURRENT_DIRECTORY,DIRECTORY_COLOR) + '$ '
        elif directory in os.listdir(CURRENT_DIRECTORY):
            os.chdir(directory)
            CURRENT_DIRECTORY = CURRENT_DIRECTORY+'\\'+directory
            PREFIX = col(f'{str(getpass.getuser())}@{str(platform.system())} ', PROMPT_COLOR) + col(CURRENT_DIRECTORY,DIRECTORY_COLOR) + '$ '
        elif os.path.exists(directory):
            os.chdir(directory)
            CURRENT_DIRECTORY = directory
            PREFIX = col(f'{str(getpass.getuser())}@{str(platform.system())} ', PROMPT_COLOR) + col(CURRENT_DIRECTORY,DIRECTORY_COLOR) + '$ '
        else:
            print(error_message('No such file or directory ' + str(directory)))

    def write(command):
        while True:
            try:
                address = command.split(' ')[1]
                _lenmessage = []
                _lenmessage.append(command.split(' ')[0])
                _lenmessage.append(command.split(' ')[1])
                _lenmessage = ' '.join(_lenmessage)
                message = command[len(_lenmessage)+1:]
                if len(message) == 0:
                    print(error_message('You have to enter a message'))
                    break
                try:
                    addr, port = address.split(':')
                except:
                    print(error_message('Address doesnt have a port given'))
                    break
                try:
                    sock = socket.socket()
                    sock.connect((addr, int(port)))
                    sock.sendall(bytes(message,'UTF-8'))
                    sock.close()
                    print(col(f'Successfully sent {str(message)} to {addr}:{str(port)}', 'green'))
                except ConnectionRefusedError:
                    print(error_message('The target refused the connection'))
                    break
                except NameError:
                    print(error_message('There was an unknown error\nMaybe the address is incorrect'))
                    break
                except socket.gaierror:
                    print(error_message('There was an unknown error\nMaybe the address is incorrect'))
                    break
                finally:
                    break
            except IndexError:
                print(error_message('Usage: write (address:port) (message)'))
                break

    def list_dir(directory):
        if os.path.exists(directory):
            all_files = os.listdir(directory)
            for file in all_files:
                if os.path.isdir(directory+'/'+file):
                    all_files.remove(file)
                    new_file = col(file, 'cyan')
                    all_files.append(new_file)
                elif os.path.isfile(directory+'/'+file):
                    all_files.remove(file)
                    new_file = col(file, 'green')
                    all_files.append(new_file)
            for i in all_files:
                print(i)
        else:
            print(error_message('ls: No such file or directory'))

def settings_menu():
    def handler(text):
        global PROMPT_COLOR, PREFIX, PREFIX_STATUS
        PROMPT_COLOR = text.lower()
        if PREFIX_STATUS:
            PREFIX = col(f'{str(getpass.getuser())}@{str(platform.system())} ', PROMPT_COLOR) + col(CURRENT_DIRECTORY,DIRECTORY_COLOR) + '$ '
        var.set(text)

    def handler2(text):
        global DIRECTORY_COLOR, PREFIX, PREFIX_STATUS
        DIRECTORY_COLOR = text.lower()
        if PREFIX_STATUS:
            PREFIX = col(f'{str(getpass.getuser())}@{str(platform.system())} ', PROMPT_COLOR) + col(CURRENT_DIRECTORY,DIRECTORY_COLOR) + '$ '
        var2.set(text)

    settings_window = Tk()
    settings_window.geometry('340x400')
    settings_window.resizable(False, False)
    settings_window.title('Settings')
    color_list = ['Cyan','Red','Blue','Yellow','Green', 'Grey', 'Magenta', 'White']
    var = StringVar()
    var.set(PROMPT_COLOR)
    var2 = StringVar()
    var2.set(DIRECTORY_COLOR)
    Label(settings_window, text='   Settings', font=('Consolas',25)).grid(row=0, column=0, columnspan=2)
    Label(settings_window, text='Prefix Color: ', font=('Consolas',25)).grid(row=1, column=0)
    op = OptionMenu(settings_window, var, *color_list, command=handler)
    op.grid(row=1,column=1)
    Label(settings_window, text='Directory Color: ', font=('Consolas', 25)).grid(row=2, column=0)
    op1 = OptionMenu(settings_window, var2, *color_list, command=handler2)
    op1.grid(row=2, column=1)
    Button(settings_window,text='Save', font=('Consolas',15), command=lambda: settings_window.destroy()).grid(row=3,column=0, columnspan=2)
    settings_window.mainloop()

os.system('cls' if os.name=='nt' else 'clear')
while True:
    command = input(PREFIX)
    if command.lower().startswith('install'):
        try:
            app = command.split(' ')[1]
            directory = command.split(' ')[2]
            commands.install(app, directory)
        except IndexError:
            print('Error')
        finally:
            continue
    elif command.lower().startswith('ls'):
        try:
            directory = command.split(' ')[1]
            commands.list_dir(directory)
        except:
            commands.list_dir(CURRENT_DIRECTORY)
        finally:
            continue
    elif command.lower().startswith('clear'):
        os.system('cls' if os.name=='nt' else 'clear')
    elif command.lower().startswith('write'):
        commands.write(command)
    elif command.lower().startswith('settings'):
        settings_menu()
    elif command.lower().startswith('prefix'):
        try:
            bool = command.split(' ')[1]
            if bool.lower() == 'on':
                PREFIX_STATUS = True
                PREFIX = col(f'{str(getpass.getuser())}@{str(platform.system())}', PROMPT_COLOR) + '$ '
            elif bool.lower() == 'off':
                PREFIX_STATUS = False
                PREFIX = ''
        except IndexError:
            print(error_message(f'Usage: prefix (on/off) / Currently prefix status is ' + 'on' if PREFIX_STATUS is True else f'Usage: prefix (on/off) / Currently prefix status is ' + 'off'))
    elif command.lower().startswith('exit'):
        exit()
    elif command.lower().startswith('cd'):
        try:
            directory = command.split(' ')[1]
            commands.change_directory(directory)
        except:
            print(error_message('Usage: cd (directory)'))
    elif command.lower().startswith('cat'):
        try:
            file_name = command.split(' ')[1]
            commands.cat(file_name)
        except IndexError:
            print(error_message('cat: You need to enter a file'))
    elif command.lower().startswith('touch'):
        try:
            path = command.split(' ')[1]
            commands.touch(path)
        except IndexError:
            print(error_message('touch: You need to enter a file'))
    elif command.lower().startswith('sudo'):
        try:
            cmd = command.split(' ')[1]
        except IndexError:
            print(error_message('sudo: Not enough arguments'))
    elif command.lower().startswith('whoami'):
        print(getpass.getuser())
    elif command.lower().startswith('echo'):
        text = command[5:]
        print(commands.echo(text))
    else:
        disabled_commands = ['help','cls']
        try:
            if command.lower() in disabled_commands:
                print(error_message(f'{str(getpass.getuser())}: command not found'))
                continue
            subprocess.call(command)
        except:
            print(error_message(f'{str(getpass.getuser())}: command not found'))
