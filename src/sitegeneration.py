import os
import shutil

from blockmarkdown import *

def copy_files_recursive(dir,copied):
    os.mkdir(copied)
    for item in os.listdir(dir):
        path = os.path.join(dir,item)
        target_path = os.path.join(copied,item)
        if os.path.isfile(path):
            shutil.copy(path,target_path)
        else:
            copy_files_recursive(path,target_path)
    
def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.isdir(dest_dir_path) and not os.path.isfile(dest_dir_path):
        os.mkdir(dest_dir_path)

    for item in os.listdir(dir_path_content):
        sc_path = os.path.join(dir_path_content,item)
        if os.path.isfile(sc_path):
           print(sc_path)
           html_path =  os.path.join(dest_dir_path,"index.html")
           generate_page(sc_path, template_path, html_path)
        else:
            target_path = os.path.join(dest_dir_path,item)
            generate_pages_recursive(sc_path,  template_path, target_path)