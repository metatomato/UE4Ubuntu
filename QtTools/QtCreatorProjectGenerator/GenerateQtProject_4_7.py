#!/usr/bin/python3
# -*-coding:utf-8 -*

import os, sys, re, shlex
from collections import defaultdict

def write_pri():
    output_pri = open(os.path.join(project_path,"includes.pri"),'w')
    for key,value in sources.items():
        if ('eng_includes' in key) and build_engine:                    
                for path in value:
                    output_pri.write('INCLUDEPATH += '+ path + '\n' )
    output_pri.close()


def process_path(path,in_mode):
    source_paths = shlex.split(line)
    file_type=''
    new_path=''
    for path in source_paths:
        if("${UE4_ROOT_PATH}" in line):        
            new_path = path.replace('${UE4_ROOT_PATH}',engine_path)
            file_type='UE'
        elif("${GAME_ROOT_PATH}" in line):        
            new_path = path.replace('${GAME_ROOT_PATH}',project_path)
            file_type='PROJECT'
    if('SOURCE' in mode or 'HEADER' in mode):
        extracted = extract_include(new_path)
        if(extracted):
            new_path = extracted
            append_path(new_path,in_mode,file_type)
    else:
        append_path(new_path,in_mode,file_type)
              

def append_path(path,in_mode,file_type):
    if('SOURCE' in in_mode and path not in sources[file_type]):
        sources[file_type].append(path)
    elif('HEADER' in in_mode and path not in headers[file_type]):
        headers[file_type].append(path)
    elif('CONFIG' in in_mode and path not in configs[file_type]):
        configs[file_type].append(path)
    #print('add ' + path + ' in ' + mode + ' for ' + file_type)


def set_mode(line):
    current_mode = mode
    if("set(SOURCE_FILES" in line):
        current_mode = "SOURCE"
    elif("set(HEADER_FILES" in line):
        current_mode = "HEADER"
    elif("set(CONFIG_FILES" in line):
        current_mode = "CONFIG"
    elif("add_custom_target" in line):
        current_mode = "TARGET"
    return current_mode


def extract_include(in_path):
    include_not_found = True;
    head = ''
    tail = ''
    keywords = ['Private', 'Public', 'Classes']
    include = in_path    

    if(include):
        while(include_not_found):
            head = os.path.split(include)[0]
            tail = os.path.split(include)[1]
            #print(head + '  <------>  ' + tail)
            if(head == '/'):
                break
            if tail in keywords: 
                include_not_found = False
                #print('include found! ' + include)
                return include
            include = head

    return ''


def write_pri():
    print('Writing includes.pri...')
    output_pri = open(os.path.join(project_path,"includes.pri"),'w')
    for key,value in headers.items():
        if ('UE' in key):                    
            for path in value:
                output_pri.write('INCLUDEPATH += '+ path + '\n' )
    output_pri.close()


def write_pro_user(project_name, project_path):
    template_path = os.path.join(script_path,'template.pro.user')
    #print('opening template at ' + template_path)
    if os.path.isfile( template_path ):                    
        with open(template_path,'r') as pro_user_content:
            data = pro_user_content.read()
            data = data.replace('%{project_name}',project_name)
            data = data.replace('%{project_path}',project_path)
            output = open(os.path.join(project_path,project_name + '.pro.user'),'w')
            output.write(data)
            print("Creating Qt pro.user config file.")
    else:
        print("Couldn't process template! Abording...")



cmakefilename = "CMakeLists.txt"
script_path = "/usr/local/QtTools/QtCreatorProjectGenerator/"

for i,arg in enumerate(sys.argv):
    if(str(arg) == '-e'):
        engine_path = str(sys.argv[i+1]) 
    if(str(arg) == '-p'):
        project_file = str(sys.argv[i+1])
    if(str(arg) == '-d'):
        script_path = str(sys.argv[i+1])

project_name = os.path.splitext(os.path.basename(project_file))[0]
project_path = os.path.dirname(project_file)
filename_path = os.path.join(project_path,cmakefilename)

if os.path.isfile(filename_path):
        sources = defaultdict(list)
        headers = defaultdict(list)
        configs = defaultdict(list)
        file = open(filename_path,'r')
        mode = ""            
        for idx,line in enumerate(file):
            if(line):
                mode = set_mode(line)
                if(mode and not "TARGET" in mode):
                    #print(mode)                                
                    process_path(line,mode)
        write_pri()
        write_pro_user(project_name, project_path)
            
               






















                
            
