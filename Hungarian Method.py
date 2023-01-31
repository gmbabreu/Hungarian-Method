import numpy as np

def main():
    """
    Tests out the method for different matrices
    """

    # Generate a random matrix
    matrix = np.array([[2, 3, 0,],
                       [2, 4, 7,],
                       [4, 0, 10]])

    # Solve the matrix with hungarian method
    solved = hungarian_method(matrix)
    
    print("Original Matrix")
    print(matrix)
    print("\nSolved matrix")
    print(solved)


def hungarian_method(X, minimize = True):
    """
    Solves the assignment problem for a given matrix
    Parameters: the matrix X, and whether to minimize or maximize
    """
    # Create an array of the max values of each column
    W = np.copy(X)

    # Delete the minimum or maximum from every column
    if minimize == True:
        for i in range(len(W[0])):
            W[:,i] -= np.min(X[:,i])
    else:
        for i in range(len(W[0])):
            W[:,i] = np.max(X[:,i])-W[:,i] 

    # Set the minimum entry in every row in which W has no zero
    for i in range(len(W)):
        if (0 not in W[i]):
            W[i] = W[i] - np.min(W[i]) 
    
    # Construct minimal cover of 0s with r rows and s columns
    r, s = konig_step(W)

    # If r + s = n we are done
    while len(r)+len(s) < len(W):
        # let e me the minimum of entries in the uncovered values
        uncovered = []
        for i in range(len(W)):
            if i not in r:
                for j in range(len(W[0])):
                    if j not in s:
                        uncovered.append(W[i, j])
        e = min(uncovered)

        # Add minimum to covered columns
        for j in range(len(W[0])):
            if j in s:
                W[:,j]+= e
        
        # Substract minimum from uncovered rows
        for i in range(len(W)):
            if i not in r:
                W[i]-= e
        
        r, s = konig_step(W)
    return W

def line_covering_both(X):
    """
    Finds each row or column with most 0s and covers it
    If both a row and column have the same amount of 0s, cover both
    """
    copy = np.copy(X)
    r = []      # covered rows
    s = []      # covered columns

    # While there are 0s in X, cover them
    while 0 in copy:
        # Find columns and rows with most 0s
        rmax, rindex = most_zeroes_row(copy)
        smax, sindex = most_zeroes_column(copy)

        delete_both = (rmax==smax and rmax>1)       # Variable for deleting both

        # Delete the column or row with the highest amount of 0s or both
        if rmax >= smax or delete_both:
            # Delete the indexed row from the matrix
            copy = np.delete(copy, rindex, 0)

            # Check if the current index is above the deleted indices
            r.sort()
            for i in r:
                if rindex >= i:
                    rindex+=1

            #Add this index to the list
            r.append(rindex)
        if smax > rmax or delete_both:
            # Delete the indexed column from the matrix
            copy = np.delete(copy, sindex, 1)

            # Check if the current index is above the deleted indices
            s.sort()
            for i in  s:
                if sindex >= i:
                   sindex+=1

            #Add this index to the list
            s.append(sindex)
    return r, s

def line_covering_one(X):
    """
    Finds each row or column with most 0s and covers it
    If both a row and column have the same amount of 0s, cover the row.
    """
    copy = np.copy(X)
    r = []      # covered rows
    s = []      # covered columns

    # While there are 0s in X, cover them
    while 0 in copy:
        # Find columns and rows with most 0s
        rmax, rindex = most_zeroes_row(copy)
        smax, sindex = most_zeroes_column(copy)

        # Delete the column or row with the highest amount of 0s or both
        if rmax >= smax:
            # Delete the indexed row from the matrix
            copy = np.delete(copy, rindex, 0)

            # Check if the current index is above the deleted indices
            r.sort()
            for i in r:
                if rindex >= i:
                    rindex+=1

            #Add this index to the list
            r.append(rindex)
        if smax > rmax:
            # Delete the indexed column from the matrix
            copy = np.delete(copy, sindex, 1)

            # Check if the current index is above the deleted indices
            s.sort()
            for i in  s:
                if sindex >= i:
                   sindex+=1

            #Add this index to the list
            s.append(sindex)
    return r, s

def konig_step(X):
    """
    Construct minimal cover of 0s for the matrix with r rows and s columns
    Finds the smallest amount of lines that cover the 0s in the matrix
    Uses two different line covering methods, returns the one with less lines
    """
    r1, s1 = line_covering_one(X)
    r2, s2 = line_covering_both(X)

    # Check which method yielded less lines
    if len(r1)+len(s1) <= len(r2) + len(s2):
        return r1, s1
    else: 
        return r2, s2
    


def most_zeroes_row(X):
    """
    Finds the row with the most zeroes
    """
    min = np.count_nonzero(X[0])
    index = 0
    for i in range(1, len(X)):
        tmp = np.count_nonzero(X[i])
        if min > tmp:
            min = tmp
            index = i
    return len(X[0])-min, index


def most_zeroes_column(X):
    """
    Finds the column with the most zeroes
    """
    min = np.count_nonzero(X[:,0])
    index = 0
    for i in range(1, len(X[0])):
        tmp = np.count_nonzero(X[:,i])
        if min > tmp:
            min = tmp
            index = i
    return len(X)-min, index


if __name__ == "__main__":
    main()