from mpi4py import MPI
import sys
import math

def checkInput(n, id):
    numArguments = len(sys.argv)
    if numArguments - 1 != n or not math.log2(n).is_integer():
        if id == 0:
            print("Liczba procesów i argumentów musi być równa i być potęgą 2.")
        sys.exit()

def nwd(a, b):
    while b != 0:
        a, b = b, a%b
    return a

def main():
    comm = MPI.COMM_WORLD
    id = comm.Get_rank()            #number of the process running the code
    numProcesses = comm.Get_size()  #total number of processes running
    myHostName = MPI.Get_processor_name()  #machine name running the code

    checkInput(numProcesses, id)

    a = int(sys.argv[id + 1])
    for i in range(int(math.log2(numProcesses))):
        offset = pow(2, i)
        # print(f"id = {id}, to = {(id + offset) % numProcesses}, from={(id - offset) % numProcesses}")
        b = comm.sendrecv(
            a, (id + offset) % numProcesses, 0,
            None, (id - offset) % numProcesses, 0
        )
        a = nwd(a, b)
    
    print(a)


########## Run the main function
main()