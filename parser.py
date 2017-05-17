import pdb
import re
import json

class Parser():

    PAGE_START = re.compile('^.*<page>')
    PAGE_END = re.compile('^.*</page>')
    TITLE_PATTERN = re.compile('^.*<title>(.*)</title>', re.M)
    LINK_PATTERN = re.compile('^.*\[\[([a-zA-Z0-9-\|\(\)\s]+)?\]\]', re.M)


    def __init__(self):
        self.page_status = False
        self.page = []
        self.output = []
        self.result = []

    def process_line(self, line):
        if self.PAGE_START.match(line) is not None:
            self.page_status = True
            self.page.append(line)
        if self.page_status:
            if self.PAGE_END.match(line) is not None:
                self.page.append(line)
                self.output.append(' '.join(self.page))
                self.page = []
                self.page_status = False
            else:
                self.page.append(line)

    def process_output(self):
        for doc in self.output:
            title = self.TITLE_PATTERN.findall(doc)[0]
            links = self.LINK_PATTERN.findall(doc)
            self.result.append({
                'title': title,
                'links': sorted(('|').join(links).split('|'), key=lambda s: s.lower())
            })

if __name__ == '__main__':

    filepath = 'data/chunk-1.xml'
    parser = Parser()
    with open(filepath, 'r') as f:
        for line in f:
            parser.process_line(line)
    parser.process_output()
    with open('chunk-1.json', 'w+') as out:
        json.dump(parser.result, out, sort_keys=True, indent=4, separators=(',', ': '))

