class matrix:
    def __init__(self, data):
        self.data = data

    def sum(self,sec):
        result  = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(self.data[i][j] + sec.data[i][j])
                result.append(row)
            return result

A = matrix([[1, 2,3], [4,5,6], [7,8,9]])
B = matrix([[9,8,7], [6,5,4], [3,2,1]])

result = A.sum(B)
print(result)