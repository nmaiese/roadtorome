import bz2
import os
import glob
import re

def findFiles(folder, extension):
    ''' return a list of all files *extension in folder'''
    if os.path.exists(folder):
        folder_pattern = os.path.join(folder, extension)
        return glob.glob(folder_pattern)
    else:
        print 'Folder "%s" not found' % folder

def extractBZ2Articles(file):
    ''' Read a list of Bz2 file, separate all articles
    contained in tag <page> ... </page>
    and return it in a list '''
    reader  = bz2.BZ2File(file)
    articles = []
    while True:
        line = reader.readline()
        if line == '':
            break
        article = ''
        if '<page>' in line:
            while True:
                article += line
                line = reader.readline()
                if '</page>' in line:
                    article += line
                    articles.append(article)
                    break
    if len(articles)>0:
        return articles
    else:
        return None


def extractTarget(articles):
    '''Read a list of Wikipedia articles, extract title and
    links in page and store it in a list of dict'''
    objects_list = []
    for a in articles:
        key = re.findall(r'<title>(.*?)</title>', a)[0]
        target = re.findall(r"\[\[(.*?)\]\]", a)
        objects_list.append({'key': key, 'target': target})
    if len(objects_list)>0:
        return objects_list
    else:
        return None




