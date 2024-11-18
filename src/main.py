from textnode import *
from htmlnode import *
from markdown_converter import *
import shutil
import os

def main():
    root_path = '/home/yllsved/workspace/github.com/csweeney02/static_site_gen'
    source = root_path+'/static'
    destination = root_path+'/public'
    content_to_generate = root_path+'/content/index.md'
    template = root_path+'/template.html'
    content_destination = root_path+'/public/index.html'
    copy_contents(source, destination)
    generate_page(content_to_generate, template, content_destination)

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

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line[:2] == "# ":
            return line.strip('#').strip()
    raise Exception("no header in markdown text")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path, 'r').read()
    template = open(template_path, 'r').read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    open(dest_path, 'w').write(template)




main()