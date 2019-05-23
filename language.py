# -*- coding: UTF-8 -*-

import os.path
import shutil

def addLanguage(desFile, desStr):
    exists = os.path.isfile(desFile)
    if not exists:return
    with open(desFile, "r", encoding='utf-8') as f1:
        lines = f1.readlines()
    with open(desFile, "w", encoding='utf-8') as f2:
        for line in lines:
            if line.strip("\n") != "</resources>":
                f2.write(line)
    with open(desFile, "a", encoding='utf-8') as f3:
        f3.write(desStr)
        f3.flush()
        f3.close()

rootdir = 'C:\\videoDownloader\\trunk\\VideoDownloaderBase1.1.7\\commonLib\\src\\main\\res'

stringsDir = ''

if rootdir == '':
    rootdir = os.path.dirname(os.path.realpath(__file__))

for dirpath,dirnames,filenames in os.walk(rootdir):
    for dirname in dirnames:
        if dirname.startswith('stringsdownload_'):
            stringsDir = dirname
            break

for dirpath,dirnames,filenames in os.walk(os.path.join(rootdir, stringsDir)):
    for filename in filenames:
        f = open(os.path.join(dirpath, filename), 'r', encoding='utf-8')
        languageStr = f.read()
        f.close()
        resourcesStartIndex = languageStr.find('<resources>') + len('<resources>')
        desStr = languageStr[resourcesStartIndex:].replace('<string name=', '    <string name=')

        desFile = None
        language = filename.split('_')
        if len(language) == 2 and language[0] != 'en':
            desFile = os.path.join(rootdir, 'values-' + language[0], "strings.xml")
            if language[0] == 'es-mx':
                desFile = os.path.join(rootdir, 'values-es-rMX', "strings.xml")
        elif filename == 'in_ID_strings.xml':
            desFile = os.path.join(rootdir, 'values-in', "strings.xml")
        elif filename == 'pt_br_strings.xml':
            desFile = os.path.join(rootdir, 'values-pt', "strings.xml")
            addLanguage(desFile, desStr)
            desFile = os.path.join(rootdir, 'values-pt-rBR', "strings.xml")
        elif filename == 'zh_CN_strings.xml':
            desFile = os.path.join(rootdir, 'values-zh-rCN', "strings.xml")
        elif filename == 'zh_TW_strings.xml':
            desFile = os.path.join(rootdir, 'values-zh-rTW', "strings.xml")
        if desFile is not None:
            addLanguage(desFile, desStr)
            print(filename[:-len('_strings.xml')] + ' process finish...')

shutil.rmtree(os.path.join(rootdir, stringsDir))
