import numpy as np

def tableau(A,b,c):
    m,n = A.shape

    #STEP 1 - Verify if works #TODO Not tested
    index_list = [index for index in range(len(b)) if b[index]<0]
    for index in index_list:
        b[index] = -b[index]
        A[index,:] = -A[index,:]

    #STEP 2 - Verified
    table = np.zeros((m+1,n+m+1))
    table[1:m+1,n+1:n+m+1] = np.eye(m)
    table[1:m+1,1:n+1] = A
    table[1:m+1,0] = b
    top_row = -1*table[:,0:n+1].sum(axis=0)
    table[0,0:n+1] = top_row[0:n+1]
    basis_list = np.arange(n+1,n+m+1) #x1,x2,x3,x4

    #TODO - Verifying
    _,t2 = table.shape
    simplex_mod(table,t2-1,basis_list)

    #STEP 3 - Should be fine
    if(table[0,0]>0):
        return None, None, 1, None
        
    while(True):
        #STEP 4 - #TODO Verify
        if(table[0,0]==0 and np.all(basis_list<n+1)):
            x_opt = np.zeros(n)
            j = 1
            for i in basis_list:
                x_opt[i-1] = table[j,0] #basis_list indices x1,x2,x3,x4
                j += 1

            new_table = np.zeros((len(basis_list)+1,n+1))
            new_table[1:len(basis_list)+1,0:n+1] = table[1:len(basis_list)+1,0:n+1]
                
            top_left = 0
            for var in basis_list:
                top_left += c[var-1]*x_opt[var-1]
            new_table[0,0] = top_left

            c_b = np.zeros(len(basis_list))
            i = 0
            for var in basis_list:
                c_b[i] = c[var-1]
                i += 1

            for i in range(n):
                if(i+1 not in basis_list):
                    new_table[0,i+1] = c[i] - np.dot(c_b,table[1:len(basis_list)+1,i+1])
            return x_opt,new_table,0,basis_list
        
        #STEP 5 - TODO Verify
        i = 0
        for var in basis_list:
            if(var > n and np.all(table[i+1,1:n+1]==0)):
                table = np.delete(table,i+1,0)
                basis_list = np.delete(basis_list,i)
            else:
                i += 1


def simplex_mod(table,n,basis_list):
    a, b = table.shape
    while(True):
        x = table[0,1:b]
        if(x>=0).all():
            x_opt = np.zeros(n)

            l = 1
            for i in basis_list:
                x_opt[i-1] = table[l,0]
                l += 1
            return x_opt, 0
            
        j = 0
        for i in range(b-1):
            if(x[i]<0):
                j = i
                break       #Verify cycling
        j += 1 #In original table

        u = table[1:a,j]
        if (u<=0).all():
            flag = 1
            return None, 1
        l = 0 #l in original table
        min_ratio = float("inf")
        for i in range(1,a):
            if(u[i-1]<=0):
                continue
            ratio = table[i,0] / u[i-1]
            ratio = round(ratio,10)
            if(ratio<min_ratio):
                min_ratio = ratio
                l = i

        basis_list[l-1] = j
        table[l,:] = (table[l,:])/table[l,j]
        for i in range(a):
            if(i == l):
                continue
            table[i,:] = table[i,:] - table[i,j]*table[l,:]