import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            node_list.append(old_node)
        else:
            text_list = old_node.text.split(delimiter)
            if len(text_list) % 2 == 0:
                raise Exception("invalid markdown syntax")
            new_nodes = []
            for text in text_list:
                if len(new_nodes) == 0 or len(new_nodes) % 2 == 0:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text, text_type))
            node_list.extend(new_nodes)
    return node_list

def extract_markdown_images(text):
    tuple_list = []
    alt_texts = re.findall(r"!\[(.*?)\]", text)
    urls = re.findall(r"\((.*?)\)", text)
    for i in range(0, len(alt_texts)):
        tuple_list.append((alt_texts[i], urls[i]))
    return tuple_list

def extract_markdown_links(text):
    tuple_list = []
    anchor_texts = re.findall(r"\[(.*?)\]", text)
    urls = re.findall(r"\((.*?)\)", text)
    for i in range(0, len(anchor_texts)):
        tuple_list.append((anchor_texts[i], urls[i]))
    return tuple_list

def split_nodes_image(old_nodes):
    node_list = []
    for old_node in old_nodes:
        if old_node.text.find("[") == -1 or old_node.text.rfind(')') == -1:
            node_list.append(old_node)
        else:
            images = extract_markdown_images(old_node.text)
            text = old_node.text
            for i in range(0, len(images)):
                text_list = text.split(f'![{images[i][0]}]({images[i][1]})', 1)
                if text_list[0] != '':
                    node_list.append(TextNode(text_list[0], TextType.TEXT))
                node_list.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
                del text_list[0]
                text = ''.join(text_list)
            if text != "":
                node_list.append(TextNode(text, TextType.TEXT))
    return node_list

def split_nodes_link(old_nodes):
    node_list = []
    for old_node in old_nodes:
        if old_node.text.find("[") == -1 or old_node.text.rfind(')') == -1:
            node_list.append(old_node)
        else:
            links = extract_markdown_links(old_node.text)
            text = old_node.text
            for i in range(0, len(links)):
                text_list = text.split(f"[{links[i][0]}]({links[i][1]})", 1)
                if text_list[0] != '':
                    node_list.append(TextNode(text_list[0], TextType.TEXT))
                node_list.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                del text_list[0]
                text = ''.join(text_list)
            if text != '':
                node_list.append(TextNode(text, TextType.TEXT))
    return node_list

def text_to_textnodes(text):
    old_node = TextNode(text, TextType.TEXT)
    return split_nodes_link(split_nodes_image(
        split_nodes_delimiter(split_nodes_delimiter(
            split_nodes_delimiter([old_node], "`", TextType.CODE), "**", TextType.BOLD), "*", TextType.ITALIC)
    ))

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n")
    