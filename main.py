# -*- coding: utf-8 -*-

import neo4jconnection
import readBz2
import chunkfile
import json
from tqdm import tqdm

#Original DB file
filename = '/Users/N/Desktop/MEC/roadtorome/rawfile/itwiki-20161120-pages-articles.xml.bz2'
#Folder for splitted DB files
folder = 'chunks'


if __name__ == '__main__':

    # Split Big file in smaller files

    print ' ########### Chunk file #############'
    chunkfile.split_xml(filename, folder)

    print ' ########### Read all file #############'
    # Get all files in folder
    files = readBz2.findFiles(folder, '*.bz2')
    graph_list = []

    print ' ########### Generate Graph Object #############'
    # For every file, extract articles list and create object graph to upload
    for file in tqdm(files):
        articles = readBz2.extractBZ2Articles(file)
        graph_list += readBz2.extractTarget(articles)

    with open('graph.json', 'w') as f:
        json.dump(graph_list, f)

    failed = []

    print ' ########### Upload to DB #############'
    # Upload a graph object to db
    for g in tqdm(graph_list):
        try:
            neo4jconnection.addObjectGraph(g)
        except:
            print '\n FAILED --> ', g
            failed.append(g)


    with open('failed.json', 'w') as f:
        json.dump(failed, f)



