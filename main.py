# -*- coding: utf-8 -*-

import neo4jconnection
import readBz2
import chunkfile
from tqdm import tqdm

#Original DB file
filename = '/Users/N/Desktop/MEC/roadtorome/rawfile/itwiki-20161120-pages-articles.xml.bz2'
#Folder for splitted DB files
folder = 'chunks'


if __name__ == '__main__':

    # Split Big file in smaller files
    chunkfile.split_xml(filename, folder)

    # Get all files in folder
    files = readBz2.findFiles(folder, '*.bz2')
    graph_list = []

    # For every file, extract articles list and create object graph to upload
    for file in tqdm(files):
        articles = readBz2.extractBZ2Articles(file)
        graph_list += readBz2.extractTarget(articles)

    # Upload a graph object to db
    for g in graph_list:
        neo4jconnection.addObjectGraph(g)