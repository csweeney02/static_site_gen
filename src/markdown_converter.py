import re
import functools
from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            node_list.append(old_node)
        else:
            text_list = old_node.text.split(delimiter)
            #if len(text_list) % 2 == 0:
                #raise Exception("invalid markdown syntax")
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
    lines = markdown.split('\n')
    blocks = []
    block = ""
    for line in lines:
        if line == "":
            if block != "":
                blocks.append(block.strip())
                block = ""
        else:
            block = block+line+"\n"
    if block != '' and block != None:
        blocks.append(block.strip())
    return blocks

def block_to_block_type(block):
    if block[0] == "#":
        hashes = block.split(" ", 1)
        number = len(hashes[0])
        return "heading"+str(number)
    if block[:3] == "```" and block[-3:] == '```':
        return "code"
    lines = block.split("\n")
    condition = True
    for i in range(0, len(lines)):
        if lines[i][0] == ">":
            condition = True
        else:
            condition = False
            break
    if condition:
        return "quote"
    condition = True
    for i in range(0, len(lines)):
        if lines[i][:2] == "* " or lines[i][:2] == "- ":
            condition = True
        else:
            condition = False
            break
    if condition:
        return "unordered_list"
    condition = True
    for i in range(0, len(lines)):
        if lines[i][:3] == f"{i+1}. ":
            condition = True
        else:
            condition = False
            break
    if condition:
        return "ordered_list"
    else:
        return "paragraph"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in blocks:
        type = block_to_block_type(block)
        children = block_to_children(block)
        html_blocks.append(block_type_to_parent_node(type, children))
    return ParentNode("div", html_blocks)

def block_to_children(block):
    lines = block.split('\n')
    all_children = []
    i = 0
    for line in lines:
        i += 1
        if line.startswith(('#',"* ","-",f'{i}.')):
            line = line.split(' ', 1)
            line = line[-1]
        all_children.append(text_to_children(line))
    return all_children

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return ParentNode('p',list(map(text_node_to_html_node, text_nodes)))


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
    raise Exception("text type not supported")

def block_type_to_parent_node(block_type, children):
    if block_type == "paragraph":
        return ParentNode("p", children)
    if block_type == "quote":
        return ParentNode("blockquote", children)
    if block_type == "unordered_list":
        return ParentNode('ul', list(map(tag_list, children)))
    if block_type == "ordered_list":
        return ParentNode('ol', list(map(tag_list, children)))
    if block_type == "code":
        return ParentNode('pre', ParentNode('code', children))
    if block_type[:7] == "heading":
        number = int(block_type[-1])
        return ParentNode(f"h{number}", children)
    
def tag_list(html_node):
    return ParentNode('li', html_node)

