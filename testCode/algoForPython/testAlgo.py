from time import time

from searchingAlgo import searchingAlgo

al = searchingAlgo()
# array = al.createRandomArray(10000, 0, 9999)
# al.saveArrayToFile("array.txt", array)
array = al.loadArrayFromFile("array.txt")
print(array)

start_time = time()
result = al.quickSort(array)
print(result)
end_time = time()
elapsed_time = end_time - start_time
print(f"QuickSort Elapsed time: {elapsed_time:.4f} seconds\n")

start_time = time()
result = al.binarySearch(result, 217)
print(result)
end_time = time()
elapsed_time = end_time - start_time
print(f"binary Search Elapsed time: {elapsed_time:.4f} seconds\n")

array = al.loadArrayFromFile("array.txt")
print(array)
start_time = time()
result = al.mergeSort(array)
print(result)
end_time = time()
elapsed_time = end_time - start_time
print(f"Merge Sort Elapsed time: {elapsed_time:.4f} seconds\n")

array = al.loadArrayFromFile("array.txt")
print(array)
start_time = time()
result = al.bubbleSort(array)
print(result)
end_time = time()
elapsed_time = end_time - start_time
print(f"bubble Sort Elapsed time: {elapsed_time:.4f} seconds\n")