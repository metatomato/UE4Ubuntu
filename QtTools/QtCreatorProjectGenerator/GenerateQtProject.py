#!/usr/bin/python3
# -*-coding:utf-8 -*

import os, sys, re, shlex
from collections import defaultdict

def process_paths(line, to_dict, build_engine, project_path, isrelative):
    path_list = shlex.split(line)
    for path in path_list:                                         
        if(project_rel_path in path):                           
            source_path = path.replace(project_rel_path, project_path)
            if isrelative:
                if source_path.startswith('/'):
                    source_path = source_path[1:]                                        
            if(".cs" in path):
                to_dict["proj_cs"].append(source_path)
            elif(".h" in path):
                to_dict["proj_h"].append(source_path)
            elif(".cpp" in path):
                to_dict["proj_cpp"].append(source_path)
            else:
                to_dict["proj_misc"] = source_path                      
        elif('Engine' in path and build_engine):            
            source_path = os.path.join(engine_path,path)
            if(".cs" in path):
                to_dict["eng_cs"].append(source_path)
            elif(".h" in path):
                to_dict["eng_h"].append(source_path)
            elif(".cpp" in path):
                to_dict["eng_cpp"].append(source_path)
            else:
                to_dict["eng_misc"].append(source_path)

def extract_include(path):
    include_not_found = True;
    head = ''
    tail = ''
    keywords = ['Private', 'Public', 'Classes']
    include = path    

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

def generate_includes(sources):
    proj_includes = list()
    eng_includes = list()
    for key, value in sources.items():
        for path in value:
            include = os.path.split(path)[0]
            ext = os.path.splitext(path)[1]
            if ext == '.h':
                extracted = extract_include(include)
                if not extracted == '':
                    if (key == 'proj_cs' or key == 'proj_h' or key == 'proj_cpp' or key == 'proj_misc'):                 
                        if not extracted in proj_includes:                    
                            proj_includes.append(extracted)   
                    if (key == 'eng_cs' or key == 'eng_h' or key == 'eng_cpp' or key == 'eng_misc'):  
                        if not extracted in eng_includes:
                            eng_includes.append(extracted)                                               
    
    sources['proj_includes'] = proj_includes
    sources['eng_includes'] = eng_includes
                      

def process_pattern(pattern,word):
    out = pattern.replace('\s', " ")
    out = out.replace('%s', word)
    return out    
    

def write_source():
    output_project = open(os.path.join(project_path,project_name)+"_extracted_source",'w')
    if(build_engine):
        output_engine = open(os.path.join(project_path,"engine")+"_extracted_source",'w')
    for key,value in sources.items():                      
            if ('eng' in key) and build_engine:    
                output_engine.write(key+': \n')
                for path in value:
                    out_path = process_pattern(path_pattern,path)
                    output_engine.write(out_path+'\n')
            elif('eng' not in key):          
                output_project.write(key+': \n')
                for path in value:
                    print(path)
                    out_path = process_pattern(path_pattern,path)
                    output_project.write(out_path+'\n')
                    print(out_path)


def write_pri():
    output_pri = open(os.path.join(project_path,"includes.pri"),'w')
    for key,value in sources.items():
        if ('eng_includes' in key) and build_engine:                    
                for path in value:
                    output_pri.write('INCLUDEPATH += '+ path + '\n' )
    output_pri.close()

def write_pro():
    pro_pattern = "TEMPLATE = app\nCONFIG += console\nCONFIG -= app_bundle\nCONFIG -= qt"
    output_pro = open(os.path.join(project_path, project_name + ".pro"),'w')
    output_pro.write(pro_pattern)
    for key,value in sources.items():
        if('proj_h' in key):
            output_pro.write('\n')
            for path in value:                
                output_pro.write('HEADERS += '+path+'\n')
        if('proj_cpp' in key):
            output_pro.write('\n')
            for path in value:
                output_pro.write('SOURCES += '+path+'\n')

    if('proj_includes' in sources):
            output_pro.write('\n')                
            for path in sources['proj_includes']:
                output_pro.write('INCLUDEPATH += ' + path + '\n' )
    output_pro.write("\n\ninclude(includes.pri)\n")

def write_pro_user(project_name, project_path):
    template_path = os.path.join(script_path,'template.pro.user')
    print('opening template at ' + template_path)
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



filename = "CMakeLists.txt"
build_engine = False
output_path = os.getcwd()
path_pattern = '%s'
use_relative_path = False
relative_path = ''
script_path = ''

print('Patching %s...' % filename)

if len(sys.argv) >= 4:

    for i,arg in enumerate(sys.argv):
        if(str(arg) == '-e'):
            engine_path = str(sys.argv[i+1])      
        if(str(arg) == '-p'):
            project_file = str(sys.argv[i+1])
        if(str(arg) == '-b'):
            if('True' == str(sys.argv[i+1]) or 'true' == str(sys.argv[i+1]) or '1' == str(sys.argv[i+1])):
                build_engine = True
        if(str(arg) == '-a'):
            path_pattern = str(sys.argv[i+1])
        if(str(arg) == '-r'):
            if('True' == str(sys.argv[i+1]) or 'true' == str(sys.argv[i+1]) or '1' == str(sys.argv[i+1])):
                use_relative_path = True
                print(relative_path)     
        if(str(arg) == '-d'):
            script_path = str(sys.argv[i+1])       

    project_name = os.path.splitext(os.path.basename(project_file))[0]
    project_path = os.path.dirname(project_file)
    project_rel_path = os.path.relpath(project_path,engine_path)
    filename_path = os.path.join(project_path,filename)
    if not use_relative_path :
        relative_path = project_path

    if os.path.isfile(filename_path):
        file = open(filename_path,'r')
        source_begin=False
        sources = defaultdict(list)
        for idx,line in enumerate(file):                        
            if("set(SOURCE_FILES" in line and "add_custom_target" not in line):
                source_begin=True
                line_stripped = line.strip('set(SOURCE_FILES')                                                         
                process_paths(line_stripped, sources, build_engine, relative_path, use_relative_path)
            elif( source_begin and "add_custom_target" not in line):               
                process_paths(line, sources, build_engine, relative_path, use_relative_path)         

        generate_includes(sources)
                  
        #write_source()    
    
        write_pri()

        write_pro()

        write_pro_user(project_name, project_path)
                
        print('Patching Done.')         
    else:
        print("%s not found." % filename_path)


else:
    print("Missing arguments. Abording...")




