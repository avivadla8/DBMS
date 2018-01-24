import csv
import numpy
import sys
import os

        # Enter the database folder
database_folder = ''


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


# print attributes

        # parse queries

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

    # print req
    return req

def load_tables(tables,tinfo):
    data = {}
    for table in tables:
        if table in tinfo.keys():
            data[table]={}
            for val in tinfo[table]:
                data[table][val] = []
        else:
            print "Error:- This Table ", table," is not present"
            exit(0)
    for table in tables:
        filename = table + ".csv"
        try:
            f = open(filename,'r')
        except:
            print "Metadata file does not exist"
            exit(0)
        lines = f.readlines()

        for line in lines:
            line = line.split("\r\n")[0]
            # line = line[0]
            vals = line.split(',')
            count = 0
            for val in vals:
                data[table][tinfo[table][count]].append(int(val))
                count = count+1
    # print data
    return data

def rec(project,data,tables,c_table,tinfo,counter):
    if(len(tables)==c_table):
        for table in tables:
            for val in tinfo[table]:
                project[table+'.'+val].append(data[table][val][counter[table]])
        return project

    table = tables[c_table]

    for val in tinfo[table]:
        temp = len(data[table][val])

    for i in range(0,temp):
        counter[table] = i
        project = rec(project,data,tables,c_table+1,tinfo,counter)

    return project


def combine_tables(data,tables,tinfo):
    project = {}
    counter = {}

    for table in tables:
        for val in tinfo[table]:
            project[table+'.'+val] = []
        counter[table] = 0

    project = rec(project,data,tables,0,tinfo,counter)

    # print project
    return project

def show_output(req,joined_tables,tinfo,tables):
    cols = req["select"]
    list_out = []
    for col in cols:
        if col=='*':
            for table in tables:
                for val in tinfo[table]:
                    list_out.append(table+'.'+val)
        else:
            if len(col.split('.'))==1:
                temp = ""
                flag = 0
                for table in tables:
                    if col in tinfo[table]:
                        flag=flag+1
                        temp = table
                if(flag==0 or flag>1):
                    print "Error :- This column", col, "is present in Multiple tables,please specify properly"
                else:
                    list_out.append(temp+'.'+col)
            else:
                if col in joined_tables.keys():
                    list_out.append(col)
    # print list_out
    count = 0
    temp = ""
    for val in list_out:
        if count==0:
            temp = val
        else:
            temp = temp + ','+val
        count = count+1
    print temp

    name = tables[0]+'.'+tinfo[tables[0]][0]
    length = len(joined_tables[name])
    for i in range(0,length):
        temp = ""
        count = 0
        for val in list_out:
            if count == 0:
                temp = str(joined_tables[val][i])
            else:
                temp = temp + ',' + str(joined_tables[val][i])
            count = count+1
        print temp

    return



def process_query(req,tinfo):
    tables = req["from"]
    data = load_tables(tables,tinfo)
    joined_tables = combine_tables(data,tables,tinfo)
    show_output(req,joined_tables,tinfo,tables)

    return

queries = sys.argv[1].split(';')

if len(queries)==1:
    print "Error :- Semicolon should be present"
    exit(0)

        # Load Metadata file

tinfo = load_metadata(database_folder+'metadata.txt')

for query in queries:
    if query == "":
        continue
    output = parse_query(query)
    process_query(output,tinfo)
