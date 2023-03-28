import random


class searchingAlgo:

    @staticmethod
    def binarySearch(arr, target):
        """
        ITA:
        L'algoritmo di ricerca binaria (o binary search in inglese) è un algoritmo di ricerca efficiente che
        viene utilizzato per trovare un elemento in un insieme ordinato di dati. Questo algoritmo è in grado di
        trovare l'elemento in un tempo logaritmico, ovvero O(log n), dove n è la dimensione dell'insieme di dati.

        Nella funzione binary_search si passa come parametri un array (l'insieme di dati in cui si vuole cercare) e
        un target (l'elemento che si vuole trovare). La funzione inizia inizializzando due variabili, low e high,
        rispettivamente all'inizio e alla fine dell'array. Viene quindi eseguito un ciclo while finché low è minore o
        uguale a high. Ad ogni iterazione, viene calcolato il valore di mid, che corrisponde all'indice centrale
        dell'array. Se il valore dell'elemento in mid è uguale al target, la funzione restituisce l'indice. Se
        l'elemento in mid è minore del target, allora la ricerca viene effettuata nella metà superiore dell'array.
        Altrimenti, la ricerca viene effettuata nella metà inferiore dell'array. Se l'elemento non viene trovato,
        la funzione restituisce -1.

        Ad esempio, supponiamo di avere un array ordinato [2, 5, 8, 12, 16, 23, 38, 56, 72, 91] e di voler cercare
        l'elemento 16. La chiamata alla funzione binary_search restituirebbe l'indice 4, poiché l'elemento 16 si
        trova all'indice 4 dell'array.

        ENG:
        The binary search algorithm (or binary search in English) is an efficient search algorithm that is used to
        find an element in a sorted set of data. This algorithm is able to find the element in a logarithmic time,
        that is O(log n), where n is the size of the set of data.

        In the binary_search function, an array (the set of data in which you want to search) and a target (the
        element you want to find) are passed as parameters. The function begins by initializing two variables,
        low and high, respectively at the beginning and at the end of the array. Then a while loop is executed
        until low is less than or equal to high. At each iteration, the value of mid is calculated, which corresponds
        to the central index of the array. If the value of the element in mid is equal to the target, the function
        returns the index. If the element in mid is less than the target, then the search is performed in the upper
        half of the array. Otherwise, the search is performed in the lower half of the array. If the element is not
        found, the function returns -1.
        :param arr:
        :param target:
        :return:
        """
        left = 0
        right = len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    def quickSort(self, array):
        """
        ITA:
        Il QuickSort è un algoritmo di ordinamento molto efficiente che utilizza il principio "divide et impera"
        per ordinare un array. L'algoritmo è basato sulla scelta di un elemento di partizione, che viene usato per
        dividere l'array in due parti, in modo che tutti gli elementi a sinistra del pivot siano minori o uguali al
        pivot, mentre tutti gli elementi a destra del pivot siano maggiori del pivot. Il processo viene quindi
        ripetuto ricorsivamente sui due sottogruppi generati fino a quando l'array è completamente ordinato.

        Nella funzione quick_sort si passa come parametro un array non ordinato. Se l'array ha una lunghezza
        inferiore o uguale a 1, viene restituito l'array stesso poiché è già ordinato. Altrimenti, viene scelto un
        pivot, che in questo caso è l'elemento al centro dell'array. Si creano poi tre sottoarray, left,
        middle e right, che contengono rispettivamente gli elementi minori, uguali e maggiori del pivot. Infine,
        si richiama ricorsivamente la funzione quick_sort sui sottogruppi left e right, e si restituisce l'array
        concatenando i sottogruppi ordinati e il sottogruppo middle.

        Ad esempio, supponiamo di avere un array non ordinato [7, 2, 5, 1, 8, 3, 9, 6, 4]. La chiamata alla funzione
        quick_sort restituirebbe l'array ordinato [1, 2, 3, 4, 5, 6, 7, 8, 9].

        ENG:
        The QuickSort is a very efficient sorting algorithm that uses the "divide et impera" principle to sort an
        array. The algorithm is based on the choice of a partition element, which is used to divide the array into
        two parts, so that all the elements on the left of the pivot are less than or equal to the pivot, while all
        the elements on the right of the pivot are greater than the pivot. The process is then repeated recursively
        on the two subgroups generated until the array is completely sorted.

        In the quick_sort function, an unsorted array is passed as a parameter. If the array has a length less than
        or equal to 1, the array itself is returned because it is already sorted. Otherwise, a pivot is chosen,
        which in this case is the element in the center of the array. Then three subarrays, left, middle and right,
        are created that contain respectively the elements less than, equal to and greater than the pivot. Finally,
        the quick_sort function is called recursively on the subgroups left and right, and the array is returned
        by concatenating the sorted subgroups and the middle subgroup.

        For example, suppose we have an unsorted array [7, 2, 5, 1, 8, 3, 9, 6, 4]. The call to the quick_sort
        function would return the sorted array [1, 2, 3, 4, 5, 6, 7, 8, 9].

        :param
        array:
        :return:
        """
        if len(array) <= 1:
            return array

        pivot = array[len(array) // 2]
        left = [x for x in array if x < pivot]
        middle = [x for x in array if x == pivot]
        right = [x for x in array if x > pivot]

        return self.quickSort(left) + middle + self.quickSort(right)

    def mergeSort(self, array):
        """
        ITA:
        Il MergeSort è un algoritmo di ordinamento basato sul principio "divide et impera", come il QuickSort.
        L'algoritmo utilizza una strategia di ricorsione per ordinare un array. In pratica, l'array viene diviso in
        due parti uguali e ciascuna parte viene ordinata ricorsivamente. Infine, le due parti ordinate vengono unite
        per creare l'array ordinato completo.

        Nella funzione merge_sort si passa come parametro un array non ordinato. Se l'array ha una lunghezza
        inferiore o uguale a 1, viene restituito l'array stesso poiché è già ordinato. Altrimenti, si calcola
        l'indice middle dell'array e si dividono l'array in due parti, left e right, in corrispondenza di
        quell'indice. Viene poi richiamata ricorsivamente la funzione merge_sort sui due sottogruppi left e right.
        Infine, si uniscono i due sottogruppi chiamando la funzione merge.

        La funzione merge prende come parametri i due sottogruppi left e right e restituisce un array ordinato
        contenente tutti gli elementi di left e right. La funzione utilizza un ciclo while per confrontare gli
        elementi degli array left e right e unirli in ordine crescente. Una volta che un sottogruppo è stato
        completamente aggiunto all'array risultante, gli elementi rimanenti nell'altro sottogruppo vengono aggiunti
        direttamente all'array risultante.

        Ad esempio, supponiamo di avere un array non ordinato [7, 2, 5, 1, 8, 3, 9, 6, 4]. La chiamata alla funzione
        merge_sort restituirebbe l'array ordinato [1, 2, 3, 4, 5, 6, 7, 8, 9]

        ENG:
        MergeSort is a sorting algorithm based on the "divide et impera" principle, like QuickSort.
        The algorithm uses a recursive strategy to sort an array. In practice, the array is divided into
        two equal parts and each part is sorted recursively. Finally, the two sorted parts are combined
        to create the complete sorted array.

        In the merge_sort function, an unsorted array is passed as a parameter. If the array has a length less than
        or equal to 1, the array itself is returned because it is already sorted. Otherwise, the middle index of the
        array is calculated and the array is divided into two parts, left and right, at that index. Then the
        merge_sort function is called recursively on the two subgroups left and right. Finally, the two subgroups
        are merged by calling the merge function.

        The merge function takes as parameters the two subgroups left and right and returns a sorted array
        containing all the elements of left and right. The function uses a while loop to compare the elements
        of the arrays left and right and merge them in ascending order. Once one subgroup has been completely
        added to the resulting array, the remaining elements of the other subgroup are added directly to the
        resulting array.

        For example, suppose we have an unsorted array [7, 2, 5, 1, 8, 3, 9, 6, 4]. The call to the merge_sort
        function would return the sorted array [1, 2, 3, 4, 5, 6, 7, 8, 9]

        For example,
        :param array:
        :return:
        """
        if len(array) <= 1:
            return array
        middle = len(array) // 2
        left = array[:middle]
        right = array[middle:]
        left = self.mergeSort(left)
        right = self.mergeSort(right)

        return self.merge(left, right)

    @staticmethod
    def merge(left, right):
        result = []

        while left and right:
            if left[0] <= right[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))

        if left:
            result += left
        if right:
            result += right

        return result

    @staticmethod
    def bubbleSort(array):
        """
        ITA:
            in generale il Bubble Sort è meno efficiente del QuickSort in termini di velocità di esecuzione. Il
            Bubble Sort ha una complessità temporale di O(n^2), il che significa che il tempo di esecuzione aumenta
            quadraticamente con la dimensione dell'array di input. Il QuickSort, d'altra parte, ha una complessità
            temporale media di O(n log n), il che lo rende molto più veloce per grandi insiemi di dati.

            Inoltre, il Bubble Sort richiede un numero maggiore di confronti e scambi di elementi rispetto al
            QuickSort, poiché effettua un confronto e uno scambio alla volta, mentre il QuickSort utilizza un
            algoritmo di partizionamento per dividere l'array in due sottogruppi e poi ordinarli in modo indipendente.

            Ciò detto, ci sono alcune eccezioni in cui il Bubble Sort potrebbe essere più veloce del QuickSort,
            ad esempio se l'array di input è già ordinato o quasi ordinato. Tuttavia, in generale, il QuickSort è
            considerato un algoritmo di ordinamento più efficiente del Bubble Sort.

        ENG:
            In general, Bubble Sort is less efficient than QuickSort in terms of execution speed. The Bubble Sort
            has a time complexity of O(n^2), which means that the execution time increases quadratically with the
            size of the input array. QuickSort, on the other hand, has a mean time complexity of O(n log n), which
            makes it much faster for large data sets.

            In addition, Bubble Sort requires a greater number of comparisons and element swaps than QuickSort,
            as it performs one comparison and one swap at a time, while QuickSort uses a partitioning algorithm
            to divide the array into two subgroups and then sort them independently.

            That said, there are some exceptions where Bubble Sort may be faster than QuickSort, for example if
            the input array is already sorted or almost sorted. However, in general, QuickSort is considered a
            more efficient sorting algorithm than Bubble Sort.

        :param array:
        :return:
        """
        n = len(array)
        for i in range(n):
            for j in range(0, n - i - 1):
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
        return array

    @staticmethod
    def createRandomArray(length, min_value, max_value):
        """
        ITA:
            Crea un array di lunghezza specificata, riempito con numeri casuali nell'intervallo specificato.
        ENG:
            Creates an array of the specified length, filled with random numbers in the specified range.

        Example:

                createRandomArray(10, 1, 100)

        :param length: array length
        :param min_value: minimum value (included) for random numbers
        :param max_value: maximum value (included) for random numbers
        :return: array of random numbers
        """
        return [random.randint(min_value, max_value) for _ in range(length)]

    @staticmethod
    def loadArrayFromFile(filename):
        """
        ITA:
            Carica un array da un file di testo.
        ENG:
            Loads an array from a text file.

        Example:

                loadArrayFromFile("array.txt")

        :param filename: file name
        :return: array
        """
        with open(filename, "r") as f:
            return [int(x) for x in f.read().split(",")]

    @staticmethod
    def saveArrayToFile(filename, array):
        """
        ITA:
            Salva un array su un file di testo.
        ENG:
            Saves an array to a text file.

        Example:

                saveArrayToFile("array.txt", [1, 2, 3, 4, 5])

        :param filename: file name
        :param array: array
        """
        with open(filename, "w") as f:
            f.write(",".join([str(x) for x in array]))