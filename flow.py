import sys
import time

X,Y,Z=int(sys.argv[1]),int(sys.argv[2]), int(sys.argv[3])

source=range(1,X+1)
transit=range(1,Y+1)
dest=range(1,Z+1)
path_num=2


def demand_volume():
    output=""
    result="Minimize\n    r\nSubject to\n"
    for i in source:
        for j in dest:
            result+="    "
            for k in transit:
                if k==Y:
                    result+="x{}{}{} = {}\n".format(i,k,j, 2*i+j)                  
                else:
                    result+="x{}{}{} + ".format(i,k,j)
    output+=result
    return output         
                                      
def binary_variable():
    output=""
    result=""    
    for i in source:
        for j in dest:
            result+="    "
            for k in transit:
                if k==Y:
                    result+="u{}{}{} = {}\n".format(i,k,j,path_num)
                else:
                    result+="u{}{}{} + ".format(i,k,j)
    output+=result
    return output
                    
def source_transit_capacity():
    output=""
    result=""     
    for i in source:
        for k in transit:
            result+="    "
            for j in dest:
                if j==Z:
                    result+="x{}{}{} - c{}{} <= 0\n".format(i,k,j,i,k)
                else:
                    result+="x{}{}{} + ".format(i,k,j)
    output+=result
    return output
                
def transit_dest_capacity():
    output=""
    result=""     
    for k in transit:
        for j in dest:
            result+="    "
            for i in source:  
                if i==X:
                    result+="x{}{}{} - d{}{} <= 0\n".format(i,k,j,k,j)
                else:
                    result+="x{}{}{} + ".format(i,k,j)                   
    output+=result
    return output 
                  
def path_flow():
    result=""
    for i in source:
        for k in transit:
            for j in dest:
                result+="    {} x{}{}{} - {} u{}{}{} = 0\n".format(path_num,i,k,j,2*i+j,i,k,j)
    return result
                    
def load():
    output=""
    result=""     
    for k in transit:
        result+="    "
        for i in source:
            for j in dest:               
                if i==X and j==Z:
                    result+="x{}{}{} - r <= 0\n".format(i,k,j)
                else:
                    result+="x{}{}{} + ".format(i,k,j)
    output+=result
    return output
                    
def bounds():
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
            
def binary_list():
    result="Binary\n"
    for i in source:
        for k in transit:
            for j in dest:
                result+="    u{}{}{}\n".format(i,k,j)
    result+="End"
    return result

def create_file(lp):
    file_name = "{}{}{}.lp".format(X,Y,Z)
    f = open(file_name,'w') 
    f.write(lp)
    f.close()
    
def main():
    first = demand_volume()
    second = binary_variable()
    third = source_transit_capacity() 
    fourth = transit_dest_capacity()
    fifth = path_flow()
    sixth = load()
    seventh = bounds()
    eighth = binary_list()
    lp = first + second + third + fourth + fifth + sixth + seventh + eighth
    
    start_time=time.time()
    create_file(lp)   
    
    end_time=time.time()
    print("Run time: {}".format(end_time - start_time))
    
main()