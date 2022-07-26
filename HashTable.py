class HashTable:
    # constructor/initial state declaration of class
    def __init__(self, initial_capacity=10):
        # sets itself to a table with an empty list
        self.table = []
        # for every int in specified range, another list is put inside of initial list, creating buckets for hash
        # table values
        for i in range(initial_capacity):
            self.table.append([])

    # gets the bucket index for the specified key that's passed in
    # runtime complexity is O(1)
    def get_hash(self, key):
        bucket_index = int(key) % len(self.table)
        return bucket_index

    # inserts a new key and item pair into the hash table using the get_hash function to find the bucket index that
    # it should be placed in
    # runtime complexity is O(n)
    def insert(self, key, item):
        bucket_index = self.get_hash(key)
        key_value = [key, item]

        if self.table[bucket_index] is None:
            self.table[bucket_index] = list([key_value])
            return True
        else:
            for pairedValues in self.table[bucket_index]:
                if pairedValues[0] == key:
                    pairedValues[1] = key_value
                    return True
            self.table[bucket_index].append(key_value)
            return True

    # runtime complexity is O(n)
    def lookup(self, key):
        bucket_index = self.get_hash(key)
        if self.table[bucket_index] is not None:
            for pairedValues in self.table[bucket_index]:
                if pairedValues[0] == key:
                    return pairedValues[1]
        return None

    # runtime complexity is O(n)
    def remove(self, key):
        bucket_index = self.get_hash(key)
        length = len(self.table[bucket_index])

        if self.table[bucket_index] is None:
            return False
        for i in range(0, length):
            if self.table[bucket_index][i][0] == key:
                self.table[bucket_index].pop(i)
                return True
        return False

    # runtime complexity is O(n)
    def update(self, key, item):
        bucket_index = self.get_hash(key)
        if self.table[bucket_index] is not None:
            for pairedValues in self.table[bucket_index]:
                if pairedValues[0] == key:
                    pairedValues[1] = item
                    return True
        else:
            print("this item could not be updated")

    # runtime complexity is O(n)
    def table_length(self):
        count = 0
        for _ in range(10):
            items = self.table[_]
            for item in items:
                count += 1
        return count
