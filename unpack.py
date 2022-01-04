# -*- coding: utf-8 -*-
"""
Created on Sat May 15 20:14:25 2021

@author: Ming
"""
import os
import zipfile
import shutil
import py7zr


def del_old_zip(file_path):
    os.remove(file_path)
    
def decompress(file_path, root):
    if file_path.endswith('.zip'):
        z = zipfile.ZipFile(f'{file_path}', 'r')
    elif file_path.endswith('.7z'):
        z = py7zr.SevenZipFile(f'{file_path}','r')
    z.extractall(path=f"{root}")
    z.close()
    
def start_dir_make(root, dirname):
    os.chdir(root)
    os.mkdir(dirname)
    return os.path.join(root, dirname)

filepath = './mesh'

num = 0 #initial file name
files = os.listdir(filepath)
for i in files:
    if(os.path.isdir(filepath+'/'+i)): # Determine whether the current is a folder
        num += 1
print(num)

for files in os.listdir(filepath):
    if files.endswith('.zip'):
        new_ws = start_dir_make(filepath, 'unprocessed_%d'%num)
        decompress(files, new_ws)
        del_old_zip(files)
        #deal with .obj file
        if os.path.isdir(new_ws+'/source'):
            #Unzip the files in source folder
            subpath=os.path.join(new_ws,'source/')
            for subfile in os.listdir(subpath):
                decompress(subpath+subfile,new_ws)
                del_old_zip(subpath+subfile)
            os.rmdir(subpath)
            #Delete textures folder
            shutil.rmtree(os.path.join(new_ws,'textures'))
            #rename
            for subfile in os.listdir(new_ws):
                if subfile.endswith('.mtl'):
                    os.rename(os.path.join(new_ws,subfile),os.path.join(new_ws,'%d.mtl'%num))
                elif subfile.endswith('.obj'):
                    os.rename(os.path.join(new_ws,subfile),os.path.join(new_ws,'%d.obj'%num))
            #Judge whether the documents are complete
            filelist = os.listdir(new_ws)
            for k in range(len(filelist)):
                # Extract the suffix of all files in the folder
                filelist[k]=os.path.splitext(filelist[k])[1]
            if not '.mtl' in filelist:
                shutil.rmtree(new_ws)
                num-=1
        #Processing .gltf format files
        else:
            filelist = os.listdir(new_ws)
            #if not 'textures' in filelist:
            #    shutil.rmtree(new_ws)
            #    num-=1
            for k in range(len(filelist)):
                filelist[k]=os.path.splitext(filelist[k])[1]
            if not '.bin' in filelist or not '' in filelist:
                shutil.rmtree(new_ws)
                num-=1
    num+=1