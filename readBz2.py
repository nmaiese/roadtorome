import bz2
import os
import glob
import re
from tqdm import tqdm

# return a list of all files *extension in folder
def findFiles(folder, extension):
    if os.path.exists(folder):
        folder_pattern = os.path.join(folder, extension)
        return glob.glob(folder_pattern)
    else:
        print 'Folder "%s" not found' % folder


# Read a list of Bz2 file, separate all articles
# contained in tag <page> ... </page>
# and return it in a list
def extractBZ2Articles(file):
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
        print 'N° of articles extracted in file %s : %s' % (file ,str(len(articles)))
        return articles
    else:
        return None


# Read a list of Wikipedia articles, extract title and
# links in page and store it in a list of dict

def extractTarget(articles):
    objects_list = []
    for a in articles:
        key = re.findall(r'<title>(.*?)</title>', a)[0]
        target = re.findall(r"\[\[(.*?)\]\]", a)
        objects_list.append({'key': key, 'target': target})
        print '% s == >> Targets:  %s' % (key, len(target))
    if len(objects_list)>0:
        print '\nN° of Articles with Target extracted: %s' % (len(objects_list))
        return objects_list
    else:
        return None


if __name__ == '__main__':

    #set bz2 files folder
    folder = 'chunks'
    files = findFiles(folder, '*.bz2')

    graph_list = []

    for file in files:
        articles = extractBZ2Articles(file)
        graph_list += extractTarget(articles)


