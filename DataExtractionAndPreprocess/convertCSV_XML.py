import csv
import lxml.etree
import lxml.builder

def convert(filenames):
    E = lxml.builder.ElementMaker()
    DOC = E.DOC
    DOCNO = E.DOCNO
    TEXT = E.TEXT

    f = open("./data/tweets.xml", 'w')
    for filename in filenames:
        with open(filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            flag = 0
            for row in spamreader:
                if flag == 0:
                    flag = 1
                    continue
                else:
                    the_doc = (DOC(DOCNO(row[1]), TEXT(row[2])))
                    print >> f, (lxml.etree.tostring(the_doc, pretty_print=True))