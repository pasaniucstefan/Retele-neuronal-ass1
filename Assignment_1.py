import re
import math


###   FUNCTII AJUTATOARE   ###

def parse_system(filename):
  matrice_A = []
  vector_B = []

  def termen_la_float(termen):
    parte_numar = termen[:-1]  # Scoatem litera de la final (x, y sau z)
    if parte_numar == '' or parte_numar == '+':
      return 1.0
    elif parte_numar == '-':
      return -1.0
    else:
      return float(parte_numar)

  with open(filename, 'r') as file:
    for line in file:
      line = line.strip()
      if not line:
        continue

      left, right = line.split('=')
      vector_B.append(float(right))
      if not left.startswith('+') and not left.startswith('-'):
        left = '+' + left

      parts = left.split()
      if len(parts) >= 3:
        first, second, third = parts[0], parts[1], parts[2]
      else:
        continue

      val_first = termen_la_float(first)
      val_second = termen_la_float(second)
      val_third = termen_la_float(third)

      row = [val_first, val_second, val_third]
      matrice_A.append(row)

  return matrice_A, vector_B

def determinant(matrix):
  a11 = matrix[0][0]
  a12 = matrix[0][1]
  a13 = matrix[0][2]

  a21 = matrix[1][0]
  a22 = matrix[1][1]
  a23 = matrix[1][2]

  a31 = matrix[2][0]
  a32 = matrix[2][1]
  a33 = matrix[2][2]

  det = a11 * (a22 * a33 - a23 * a32) - a12 * (a21 * a33 - a23 * a31) + a13 * (a21 * a32 - a22 * a31)

  return det
def trace(matrix):
    a11 = matrix[0][0]
    a22 = matrix[1][1]
    a33 = matrix[2][2]
    t = a11+a22+a33
    return t   

def vector_norm(vector):
    norm = math.sqrt(sum(x*x for x in vector))
    return norm

def transpose(matrix):
    transposed = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[0])):
            row.append(matrix[j][i])
        transposed.append(row)
    return transposed

def matrix_multiply(matrix, vector):
    result = []
    for i in range(len(matrix)):
        sum = 0
        for j in range(len(matrix[0])):
            sum = sum + matrix[i][j] * vector[j] 

        result.append(sum) 

    return result

def replace_matrix(matrix,vector,index):

    new_matrix = [row[:] for row in matrix]
    for i in range(len(matrix)):
        new_matrix[i][index] = vector[i]

    return new_matrix

def Cramer_solver (matrix,vector):
    det_A = determinant(matrix)
    if det_A == 0:
        return "Nu are solutie unica"

    mat_x = replace_matrix(matrix ,vector,0)
    mat_y = replace_matrix(matrix ,vector,1)
    mat_z = replace_matrix(matrix ,vector,2)

    det_x = determinant(mat_x)
    det_y = determinant(mat_y)
    det_z = determinant(mat_z)

    x = det_x / det_A
    y = det_y / det_A  
    z = det_z / det_A

    return [x,y,z]

def det2x2(a, b, c, d):
  return a * d - b * c


def adj_matrix(matrix):
  # 1. Extragem elementele matricei ca să le vedem clar pe rânduri
  a00, a01, a02 = matrix[0]
  a10, a11, a12 = matrix[1]
  a20, a21, a22 = matrix[2]

  C00 = det2x2(a11, a12, a21, a22)
  C01 = -det2x2(a10, a12, a20, a22)
  C02 = det2x2(a10, a11, a20, a21)

  C10 = -det2x2(a01, a02, a21, a22)
  C11 = det2x2(a00, a02, a20, a22)
  C12 = -det2x2(a00, a01, a20, a21)

  C20 = det2x2(a01, a02, a11, a12)
  C21 = -det2x2(a00, a02, a10, a12)
  C22 = det2x2(a00, a01, a10, a11)


  adj = [[C00, C10, C20], [C01, C11, C21], [C02, C12, C22]]

  return adj

def Inverse_matrix(matrix):
    new_matrix = adj_matrix(matrix)
    det_A = determinant(matrix)
    if det_A == 0:
        return "Nu este inversabila"
    coef = 1/det_A
    for i in range(len(new_matrix)):
        for j in range(len(new_matrix[0])):
            new_matrix[i][j] *= coef
    return new_matrix

def Inversion_solver(matrix,vector):
    new_vector = vector
    new_matrix = Inverse_matrix(matrix)
    if new_matrix == "Nu este inversabila":
        return "Nu are solutie unica"
    result = matrix_multiply(new_matrix,new_vector)
    return result

###  MAIN  ###

A,B = parse_system("Input_Assignment1.txt")

print("Matricea A:" , A)
print("Vectorul B:" , B)
print()

solutie_cramer = Cramer_solver(A, B)
print("Solutia folosind Regula lui Cramer [x, y, z]:")
print(solutie_cramer)
print()

solutie_inversa = Inversion_solver(A, B)
print("Solutia folosind Inversa Matricei [x, y, z]:")
print(solutie_inversa)