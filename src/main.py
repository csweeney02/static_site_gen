from textnode import *
from htmlnode import *
import shutil
import os

def main():
    source = '/home/yllsved/workspace/github.com/csweeney02/static_site_gen/static'
    destination = '/home/yllsved/workspace/github.com/csweeney02/static_site_gen/public'
    copy_contents(source, destination)

def copy_contents(source, destination):
    if destination == '/home/yllsved/workspace/github.com/csweeney02/static_site_gen/public' and os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    directories = os.listdir(source)
    for dir in directories:
        if os.path.isfile(source+'/'+dir):
            shutil.copy(source+'/'+dir, destination)
        else:
            copy_contents(source+'/'+dir, destination+'/'+dir)


main()