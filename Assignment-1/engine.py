import csv
import numpy
import sys
import os
import time

        # Enter the database folder
database_folder = ''
print_length=False
print_time = False

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
            print "Error:- ", table," is not present in the database"
            exit(0)
    for table in tables:
        filename = table + ".csv"
        try:
            f = open(filename,'r')
        except:
            print "Error:- ", table," is not present in the database"
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



def apply_constraints(req,joined_tables,tinfo,tables):
    return joined_tables

def apply_aggregate(joined_tables,oper,val,length):
    output = 0
    for i in range(0,length):
        if i == 0:
            output = joined_tables[val][i]
        else:
            if oper == 'min':
                output = min(output,joined_tables[val][i])
            elif oper == 'max':
                output = max(output,joined_tables[val][i])
            elif oper == 'sum':
                output = output + joined_tables[val][i]
            elif oper == 'average':
                output = output + joined_tables[val][i]
    if oper == 'average':
        output = (output*1.0)/length

    return output

def extract_col(req,joined_tables,tinfo,tables,list_out,col):
    if len(col.split('('))==2 and col.split('(')[0]=='':
        col = col.split('(')[1]
        col = col.split(')')[0]
    elif(len(col.split('('))==2):
        print "Error:- ",col," is not according to syntax"
        exit(0)

    if len(col.split('.'))==1:
        temp = ""
        flag = 0
        for table in tables:
            if col in tinfo[table]:
                flag=flag+1
                temp = table
        if(flag==0):
            print "Error :- '", col, "' is not present in the given list of tables"
            exit(0)
        elif(flag>1):
            print "Error :- '", col, "' is present in Multiple tables,please specify properly"
            exit(0)
        else:
            list_out.append(temp+'.'+col)
            col = temp+'.'+col
    else:
        if col in joined_tables.keys():
            list_out.append(col)
        else:
            print "Error :- '", col, "' is not present in the given list of tables"
            exit(0)

    return list_out,col

def show_output(req,joined_tables,tinfo,tables):
    cols = req["select"]
    list_out = []
    list_distinct = []
    list_aggre = {}
    list_aggre['max']=[]
    list_aggre['min']=[]
    list_aggre['sum']=[]
    list_aggre['average']=[]

    flag_main = -1
    for col in cols:
        if col=="":
            continue
        if col=='*':
            for table in tables:
                for val in tinfo[table]:
                    list_out.append(table+'.'+val)
        elif(len(col.split('max'))==2 or len(col.split('min'))==2 or len(col.split('sum'))==2 or len(col.split('average'))==2):
            if(flag_main==0):
                print "Error:- In Aggregated query, select list also contains non-aggregated columns"
                exit(0)

            if(len(col.split('max'))==2):
                col = col.split('max')[1]
                list_out,col = extract_col(req,joined_tables,tinfo,tables,list_out,col)
                list_aggre['max'].append(col)
            elif(len(col.split('min'))==2):
                col = col.split('min')[1]
                list_out,col = extract_col(req,joined_tables,tinfo,tables,list_out,col)
                list_aggre['min'].append(col)
            elif(len(col.split('sum'))==2):
                col = col.split('sum')[1]
                list_out,col = extract_col(req,joined_tables,tinfo,tables,list_out,col)
                list_aggre['sum'].append(col)
            elif(len(col.split('average'))==2):
                col = col.split('average')[1]
                list_out,col = extract_col(req,joined_tables,tinfo,tables,list_out,col)
                list_aggre['average'].append(col)
            else:
                print "Error:- Improper usage of Aggregate query"
                exit(0)
            flag_main=1
        elif(len(col.split('distinct'))==2):
            col = col.split('distinct')[1]
            if(flag_main==1):
                print "Error:- In Aggregated query, select list contains non-aggregated column -- ", col
                exit(0)
            elif(flag_main==2):
                print "Error:- Multiple distinct can't be used"
                exit(0)

            list_out,col = extract_col(req,joined_tables,tinfo,tables,list_out,col)
            list_distinct.append(col)
            flag_main = 2
        else:

            if flag_main==1:
                print "Error:- In Aggregated query, select list contains non-aggregated column -- ", col
                exit(0)
            if(flag_main==-1):
                flag_main=0
            list_out,col = extract_col(req,joined_tables,tinfo,tables,list_out,col)


    # print list_out
    if list_out==[]:
        print "Warning:- No select columns included"
        exit(0)

    joined_tables = apply_constraints(req,joined_tables,tinfo,tables)

    if flag_main==0 or flag_main==2:
        dist_attri=""
        dist_attri_list= []
        if flag_main==2:
            dist_attri = list_distinct[0]
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
            flag=0
            temp = ""
            count = 0
            for val in list_out:
                if flag_main==2 and dist_attri==val:
                    if joined_tables[val][i] not in dist_attri_list:
                        dist_attri_list.append(joined_tables[val][i])
                    else:
                        flag = 1 
                if count == 0:
                    temp = str(joined_tables[val][i])
                else:
                    temp = temp + ',' + str(joined_tables[val][i])
                count = count+1
            if flag==0:
                print temp

    elif(flag_main==1):
        count = 0
        temp = ""
        for val in list_out:
            for oper in list_aggre.keys():
                if val in list_aggre[oper]:
                    val = oper +'('+val + ')'
                    if count==0:
                        temp = val
                    else:
                        temp = temp + ','+val
                    count = count+1
        print temp

        name = tables[0]+'.'+tinfo[tables[0]][0]
        length = len(joined_tables[name])
        temp = ""
        count = 0
        for val in list_out:
            for oper in list_aggre.keys():
                if val in list_aggre[oper]:
                    output = apply_aggregate(joined_tables,oper,val,length)
                    if count==0:
                        temp = str(output)
                    else:
                        temp = temp + ',' + str(output)
                    count = count + 1
        print temp
    if(print_length):
        print "\n",length,"Rows in set"


    return



def process_query(req,tinfo):
    tables = req["from"]
    length = len(tables)
    flag=0
    for i in range(0,length):
        for j in range(i+1,length):
            if tables[i]==tables[j]:
                flag=1
                break
        if flag:
            break

    if(flag==1):
        print "Error:-table names should be unique"
        exit(0)

    data = load_tables(tables,tinfo)
    joined_tables = combine_tables(data,tables,tinfo)
    show_output(req,joined_tables,tinfo,tables)

    return

queries = sys.argv[1].split(';')

if len(queries)==1 or queries[len(queries)-1]!="":
    print "Error :- Semicolon should be present at the end"
    exit(0)

        # Load Metadata file

tinfo = load_metadata(database_folder+'metadata.txt')

for query in queries:
    if query == "":
        continue
    start = time.time()
    output = parse_query(query)
    process_query(output,tinfo)
    end = time.time()
    if(print_time):
        print "Time taken:- ",end-start,"\n"
