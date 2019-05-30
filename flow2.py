import sys
import time
import subprocess

sourceNode,transitNode,destNode=int(sys.argv[1]),int(sys.argv[2]), int(sys.argv[3])
path_num=2

def demand_volume(source, transit, dest):
    output=""
    result="Minimize\n    r\nSubject to\n"
    for i in source:
        for j in dest:
            result+="    "
            for k in transit:
                if k==len(transit):
                    result+="x{}{}{} = {}\n".format(i,k,j, 2*i+j)
                else:
                    result+="x{}{}{} + ".format(i,k,j)
    output+=result
    return output

def binary_variable(source, transit, dest):
    output=""
    result=""
    for i in source:
        for j in dest:
            result+="    "
            for k in transit:
                if k==len(transit):
                    result+="u{}{}{} = {}\n".format(i,k,j,path_num)
                else:
                    result+="u{}{}{} + ".format(i,k,j)
    output+=result
    return output

def source_transit_capacity(source, transit, dest):
    output=""
    result=""
    for i in source:
        for k in transit:
            result+="    "
            for j in dest:
                if j==len(dest):
                    result+="x{}{}{} - c{}{} <= 0\n".format(i,k,j,i,k)
                else:
                    result+="x{}{}{} + ".format(i,k,j)
    output+=result
    return output

def transit_dest_capacity(source, transit, dest):
    output=""
    result=""
    for k in transit:
        for j in dest:
            result+="    "
            for i in source:
                if i==len(source):
                    result+="x{}{}{} - d{}{} <= 0\n".format(i,k,j,k,j)
                else:
                    result+="x{}{}{} + ".format(i,k,j)
    output+=result
    return output

def path_flow(source, transit, dest):
    result=""
    for i in source:
        for k in transit:
            for j in dest:
                result+="    {} x{}{}{} - {} u{}{}{} = 0\n".format(path_num,i,k,j,2*i+j,i,k,j)
    return result

def load(source, transit, dest):
    output=""
    result=""
    for k in transit:
        result+="    "
        for i in source:
            for j in dest:
                if i==len(source) and j==len(dest):
                    result+="x{}{}{} - r <= 0\n".format(i,k,j)
                else:
                    result+="x{}{}{} + ".format(i,k,j)
    output+=result
    return output

def bounds(source, transit, dest):
    result="Bounds\n"
    for i in source:
        for k in transit:
            for j in dest:
                result+="    x{}{}{} >= 0\n".format(i,k,j)

    for i in source:
        for k in transit:
            result+="    c{}{} >= 0\n".format(i,k)

    for k in transit:
        for j in dest:
            result+="    d{}{} >= 0\n".format(k,j)
    return result

def binary_list(source, transit, dest):
    result="Binary\n"
    for i in source:
        for k in transit:
            for j in dest:
                result+="    u{}{}{}\n".format(i,k,j)
    result+="End"
    return result

def create_file(lp, X, Y, Z):
    file_name = "{}{}{}.lp".format(X,Y,Z)
    f = open(file_name,'w')
    f.write(lp)
    f.close()    
    
def run_cplex(file_name):
    command="/home/cosc/student/myu37/cplex/bin/x86-64_linux/cplex"
    args=[
        "-c",
        "read /home/cosc/student/myu37/Desktop/" + file_name,
        "optimize",
        'display solution variables -'
    ] 
    proc = subprocess.Popen([command] + args,stdout=subprocess.PIPE)
    out,err = proc.communicate()
    result = out.decode("utf-8").split()
    
    time = 0
    for i in range(len(result)):
        if result[i] == 'Solution' and result[i+1] == 'time' and result[i+2] == '=':
            time = result[i+3]
    
    
    index = result.index('r')
    result = result[index:]
    none_zero = 0
    capacity = {}
    links = {}
    
    for i in range(len(result)):
        if result[i][0] == 'c' or result[i][0] == 'd':
            if float(result[i+1]) != 0 :
                none_zero += 1
            capacity[result[i]] = float(result[i+1])
        
        if result[i][0] == 'x':
            links[result[i]] = float(result[i+1])
        
    highest = max(capacity.values())
    highest_links = [k for k, v in capacity.items() if v == highest]
    
    
    links = sorted([(int(k[2]), v) for k, v in links.items()])
    
    groupByKey = {}
    for k, v in links:
        if k not in groupByKey.keys():
            groupByKey[k] = v
        else:
            groupByKey[k] += v
    spread = max(groupByKey.values()) - min(groupByKey.values())
    print('Spread:', spread)    
    print('highest_links:', highest_links)
    print('running time:',time, 'seconds')    
    print('none_zero capacity:', none_zero) 
    

def main():

    source = [i for i in range(1,sourceNode + 1)]
    dest = [i for i in range(1,destNode + 1)]
    transit=[i for i in range(1,transitNode + 1)]

    first = demand_volume(source, transit, dest)
    second = binary_variable(source, transit, dest)
    third = source_transit_capacity(source, transit, dest)
    fourth = transit_dest_capacity(source, transit, dest)
    fifth = path_flow(source, transit, dest)
    sixth = load(source, transit, dest)
    seventh = bounds(source, transit, dest)
    eighth = binary_list(source, transit, dest)
    lp = first + second + third + fourth + fifth + sixth + seventh + eighth
    
    create_file(lp, len(source), len(transit), len(dest))
    file_name = "{}{}{}.lp".format(sourceNode,transitNode,destNode)
    run_cplex(file_name)

main()