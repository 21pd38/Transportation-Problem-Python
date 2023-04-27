# SCL PROJECT SEM 4
# 21PD38 and 20PD18

import copy

#----creates matrix------

def create_matrix():
    rows = int(input("Enter the number of rows: "))
    columns = int(input("Enter the number of columns: "))
    matrix = []
    for i in range(rows):
        temp = []
        for j in range(columns):
            tempe = int(input("Enter {0},{1} th element of the matrix: ".format(i+1,j+1)))
            temp.append(tempe)
        matrix.append(temp)
    matrix = balance_matrix(matrix)
    print()
    return matrix

#------prints matrix--------

def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(str(matrix[i][j])+"\t",end = " ")
        print()
    

#-------subtracts each and every row with its min. element-----------

def row_reduction(matrix):
    matrix2 = matrix
    for i in range(len(matrix2)):
        mini = min(matrix2[i])
        for j in range(len(matrix2[i])):
            matrix2[i][j] = matrix2[i][j] - mini
    return matrix2

#----------tranposes the matrix--------

def transpose(matrix):
    matrixt = []
    for i in range(len(matrix[0])):
        temp = []
        for j in range(len(matrix)):
            temp.append(matrix[j][i])
        matrixt.append(temp)
    return matrixt

#-----------subtracts each and every column with its min. element----------

def column_reduction(matrix):
    matrix3 = transpose(matrix)
    matrix3 = row_reduction(matrix3)
    matrix3 = transpose(matrix3)
    return matrix3

#---------- Balance the matrix ----------

def balance_matrix(matrix):
    if len(matrix) == len(matrix[0]):
        return matrix
    elif len(matrix)>len(matrix[0]):
        diff = len(matrix) - len(matrix[0])
        for i in range(len(matrix)):
            for j in range(diff):
                matrix[i].append(0)
    elif len(matrix)<len(matrix[0]):
        diff = len(matrix[0]) - len(matrix)
        for i in range(diff):
            temp = []
            for j in range(len(matrix[i])):
                temp.append(0)
            matrix.append(temp)
    return matrix
    
#------------Index's matrix, i.e numbers the rows and columns-------

def indexing_matrix(matrix):
    matrixt = []
    column = len(matrix[0])
    temp = []
    for i in range(column+1):
        temp.append(i)
    matrixt.append(temp)
    row = len(matrix)
    for j in range(row):
        temp = [0 for k in range(column+1)]
        matrixt.append(temp)
    for j in range(len(matrixt)):
        matrixt[j][0] = j
    for i in range(1,len(matrixt)):
        for j in range(1,len(matrixt)):
            matrixt[i][j] = matrix[i-1][j-1]
    return matrixt


#--------- Converts the cost matrix into assignment matrix ---------

def assignment_matrix(matrix):    
    matrix2 = balance_matrix(matrix)
    matrix2 = row_reduction(matrix2)
    matrix2 = column_reduction(matrix2)
    matrix2 = indexing_matrix(matrix2)
    return matrix2

#--------- Counts the number of zeros in a row ------------

def count_zeros(row):
    count = 0
    for i in range(len(row)):
        if row[i] == 0:
            count += 1
    return count

#--------- find the minimum element ------------

def min_element(matrixt):
    mini = matrixt[1][1]
    matrixtt = copy.deepcopy(matrixt)
    matrixtt.remove(matrixtt[0])
    matrixtt = transpose(matrixtt)
    matrixtt.remove(matrixtt[0])
    matrixtt = transpose(matrixtt)
    for i in matrixtt:
        if mini>min(i):
            mini = min(i)
    return mini
        

#---------checks whether the matrix contains zero or not------------

def no_zeros(matrixt):
    for i in range(1,len(matrixt)):
        if 0 in matrixt[i]:
            return False
    return True

#---------checks whether the given matrix satisfys the assignment matrix condition or not---------

def check_assignment_matrix(matrixt):
    for i in range(len(matrixt)):
        if 0 in matrixt[i]:
            continue
        else:
            return False
    matrixt = transpose(matrixt)
    for i in range(len(matrixt)):
        if 0 in matrixt[i]:
            continue
        else:
            return False
    return True

#----------removes specific column and row and gives the resulting sub matrix---------

def submatrix(matrixt,row,column):
    matrixtt = copy.deepcopy(matrixt)
    matrixtt.remove(matrixtt[row])
    matrixtt = transpose(matrixtt)
    matrixtt.remove(matrixtt[column])
    matrixtt = transpose(matrixtt)
    return matrixtt

#---------removes the given row of the matrix -----------

def remove_row(matrixt,index):
    matrixt.remove(matrixt[index])
    return matrixt

#---------returns the number of zeros and the index of the row containing max no. of zeros--------

def max_row_zeros(matrixt):
    maxi = 0
    index = 0
    for i in range(1,len(matrixt)):
        if count_zeros(matrixt[i])>maxi:
            maxi = count_zeros(matrixt[i])
            index = i
    return maxi,index

#--------if IBFS != optimal solution then the matrix is converted accordingly to obtain the optimal soln.--------

def convert_matrix(matrixt):
    columnindices = []
    rowindices = []
    while no_zeros(matrixt) != True:
        rowmaxi,rowindex = max_row_zeros(matrixt)
        matrixt = transpose(matrixt)
        columnmaxi,columnindex = max_row_zeros(matrixt)
        matrixt = transpose(matrixt)
        if columnmaxi > rowmaxi:
            columnindices.append(matrixt[0][columnindex])
            matrixt = transpose(matrixt)
            matrixt = remove_row(matrixt, columnindex)
            matrixt = transpose(matrixt)
        else:
            rowindices.append(matrixt[rowindex][0])
            matrixt = remove_row(matrixt, rowindex)
    return matrixt,rowindices,columnindices

#--------allocates from the top left most zero-------

def northwest_allocation_method(matrixt):
    for i in range(1,len(matrixt)):
        if count_zeros(matrixt[i]) != 0:
            for j in range(1,len(matrixt[i])):
                if matrixt[i][j] == 0:
                    index = (matrixt[i][0],matrixt[0][j])
                    matrixt = copy.deepcopy(submatrix(matrixt,i,j))
                    return matrixt,index
    
#--------checks whether matrix has a sub null matrix or not----------

def check_maxrix(matrixt):
    for i in range(1,len(matrixt)):
        if count_zeros(matrixt[i]) == 1:
            return True
    matrixt = transpose(matrixt)
    for i in range(1,len(matrixt)):
        if count_zeros(matrixt[i]) == 1:
            return True
    return False

#---------selects the most suitable element from the current matrix------------

def select_element(matrixt):
    if check_maxrix(matrixt) == True:
        flag = True
        for i in range(1,len(matrixt)):
            if count_zeros(matrixt[i]) == 1:
                for j in range(1,len(matrixt[i])):
                    if matrixt[i][j] == 0:
                        index = (matrixt[i][0],matrixt[0][j])
                        matrixt = copy.deepcopy(submatrix(matrixt, i, j))
                        flag = False
                        print_matrix(matrixt)
                        print()
                        return matrixt,index
        if flag == True:
            matrixt = transpose(matrixt)
            for i in range(1,len(matrixt)):
                if count_zeros(matrixt[i]) == 1:
                    for j in range(1,len(matrixt[i])):
                        if matrixt[i][j] == 0:
                            index = (matrixt[j][0],matrixt[0][i])
                            matrixt = copy.deepcopy(submatrix(matrixt, i, j))
                            print_matrix(transpose(matrixt))
                            print()
                            matrixt = transpose(matrixt)
                            return matrixt,index
    else:
        matrixt,index = northwest_allocation_method(matrixt)
        print_matrix(matrixt)
        print()
        return matrixt,index

#-----------corrects the assignment matrix for the optimal solution------------

def correction(matrixt,minel,rowindices,columnindices):
    for i in range(1,len(matrixt)):
        for j in range(1,len(matrixt[i])):
            if matrixt[i][0] not in rowindices:
                if matrixt[0][j] not in columnindices:
                    matrixt[i][j] -= minel
    for i in range(len(rowindices)):
        for j in range(len(columnindices)):
            matrixt[rowindices[i]][columnindices[j]] += minel
    return matrixt

#-----------gives matrix that is of optimal soln type------------

def optimal_soln(matrixt):
    print("Current submatrix is uncompatible.")
    print("Hence current assignment is not the optimal solution of the given system.")
    print()
    matrixt = copy.deepcopy(assigned_matrix)
    rowindices = []
    columnindices = []
    print("We now covert the matrix to sort the elements into basic and non basic")
    print()
    matrixt,rowindices,columnindices = convert_matrix(matrixt)
    mini = min_element(matrixt)
    matrixt = copy.deepcopy(assigned_matrix)
    matrixt = correction(matrixt, mini, rowindices, columnindices)
    return matrixt

#---------assigns all the optimum cells and return the indices as a list of tuple------ 

def assign(matrixt):
    indices = []
    print("Assignment of the cells optimally starts")
    print()
    while len(matrixt) != 1:
        matrixt,temp = select_element(matrixt)
        indices.append(temp)
        if check_assignment_matrix(matrixt) == False:
            indices.clear()
            matrixt = optimal_soln(matrixt)
            print("Current assignment matrix that has been modified for the optimal solution")
            print()
            print_matrix(matrixt)
            print()
            print("Assignment of the cells resumes......")
            print()
    return indices
    
#-------adds all the values of the assigned cells in the cost matrix and return the total cost--------

def total_cost(matrix,indices):
    total_cost = 0
    for i in indices:
        total_cost += matrix[i[0]-1][i[1]-1]
    return total_cost

#-------returns the largest element of the matrix------------

def max_element(matrixt):
    maxi = matrixt[0][0]
    for i in matrixt:
        if maxi < max(i):
            maxi = max(i)
    return maxi

#----------converts the maximisation problem into minimisation problem-------

def max_matrix(matrixt):
    ele = max_element(matrixt)
    for i in matrixt:
        for j in range(len(i)):
            i[j] -= ele
            i[j] *= -1
    return matrixt

#---------------menu driven-------------------------


print("1. minimisation problem")
print("2. maximisation problem")
choice = int(input("Enter your choice : "))

if choice == 1:
    matrix = create_matrix()
    cost_matrix = copy.deepcopy(matrix)
    matrix2 = assignment_matrix(matrix)
    assigned_matrix = copy.deepcopy(matrix2)
    indices = assign(matrix2)
    print("Cost Matrix :")
    print_matrix(cost_matrix)
    print()
    print("Assignment Matrix : ")
    print_matrix(assigned_matrix)
    print()
    print("Indices of the assigned cells in assigned order : ")
    print(indices)
    print()
    final_cost = total_cost(cost_matrix,indices)
    print('Min cost of the assignment is : ',final_cost)

elif choice == 2:
    matrix = create_matrix()
    cost_matrix = copy.deepcopy(matrix)
    matrix = copy.deepcopy(max_matrix(matrix))
    matrix2 = assignment_matrix(matrix)
    assigned_matrix = copy.deepcopy(matrix2)
    indices = assign(matrix2)
    print("Cost Matrix : ")
    print_matrix(cost_matrix)
    print()
    print("Assignment Matrix: ")
    print_matrix(assigned_matrix)
    print()
    print("Indices of the assigned cells in assigned order : ")
    print(indices)
    print()
    final_cost = total_cost(cost_matrix,indices)
    print('Min cost of the assignment is : ',final_cost)
