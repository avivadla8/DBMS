import csv
import numpy
import sys
import os

        # Enter the database folder
database_folder = ''

queries = sys.argv[1].split(';')

def load_metadata(filename):
    attri = list()
    tinfo = {}

    try:
        f = open(filename,'r')
    except:
        print "Metadata file does not exist"
        exit(0)

    # lines = []
    # with open(filename,'r') as f:
    #     for line in f:
    #         lines.append(line)

    lines = f.readlines()
    flag = 0
    count = 0
    tname="a"

    for line in lines:
        line = line.split("\r\n");
        line = line[0]
        if line == "<begin_table>":
            flag = 1
            count = 0
        elif line == "<end_table>":
            count = 0
            flag = 0
        else:
            if flag==1:
                count = count+1
                if count==1:
                    tname=line
                    tinfo[tname] = []
                else:
                    temp = tname + "." + line
                    tinfo[tname].append(line)
                    attri = attri + [temp]
    return tinfo



        # Load Metadata file

attributes = load_metadata(database_folder+'metadata.txt')
# print attributes

        # Solve queries

def parse_query(query):
    grp = ""
    req = {}

    que = query.split("select")
    if len(que)==2:
        if que[0] is not "":
            print "Error:- Refer manual for syntax"
            exit(0)
        que = que[1].split("from")
        if len(que)==2:
            req["select"]=[]
            req["select"]= req["select"] + (que[0].split(' '))
            req["select"] = ''.join(req["select"])
            que = que[1].split("where")
            if len(que)==1:
                req["from"] = []
                req["from"] = req["from"] + (que[0].split(' '))
                req["from"] = ''.join(req["from"])
            elif len(que)==2:
                req["from"] = []
                req["from"] = req["from"] + (que[0].split(' '))
                req["from"] = ''.join(req["from"])
                req["where"] = []
                req["where"] = req["where"] + (que[1].split(' '))
                req["where"] = ''.join(req["where"])
            else:
                print "Error:- Refer manual for syntax"
                exit(0)
        else:
            print "Error:- Refer manual for syntax"
            exit(0)
    else:
        print "Error:- Refer manual for syntax"
        exit(0)


    req["select"] = req["select"].split(',')
    req["from"] = req["from"].split(',')
    # if "where" in req.keys():
    #     req["where"] = req["where"].split('and')
    #     req["where"] = req["where"].split('or')

    print req
    return

def parse_query2(query):
    term= ""
    req = {}
    que = query.split(" ")
    for q in que:
        if q== "select" or q=="from" or q=="where":
            if q in req.keys():
                print "Error:- Improper syntax" , q , "already given"
                exit(0)
            req[q]=[]
            term = q
        else:
            if term=="":
                print "No select term present"
                exit(0)
            else:
                req[term].append(q)

    if "from" not in req.keys():
        print "Error:- From not used, ie. no tables included"
        exit(0)
    if "select" not in req.keys():
        print "Error:- select not used, ie. no tables included"
        exit(0)
    # print req

    return req

for query in queries:
    output = parse_query(query)
    # process_query(output)
    # parse_query2(query)