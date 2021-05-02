from mpi4py import MPI
import numpy as np

def main():
    vector_size = 1000000
    part_size = 1000
    comm = MPI.COMM_WORLD
    numProcesses = comm.Get_size()
    comm = comm.Create_cart([numProcesses])
    id = comm.Get_rank()

    if id == 0:
        vector = np.random.randint(vector_size, size=vector_size).tolist()
    else:
        vector = []

    for i in range(int(vector_size/part_size)):
        prev, next = comm.Shift(0, 1)

        part = comm.recv(source=prev)
        vector.extend(part or [])

        part = vector[(i*part_size):((i+1)*part_size)]
        comm.send(part, dest=next)
  
    print(f"id = {id}, len = {len(vector)}, first = {vector[0]}, last = {vector[vector_size - 1]}")


########## Run the main function
main()