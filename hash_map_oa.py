# Name: Cassidy Unpingco
# OSU Email: unpingcc@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 03/11/2022
# Description: Portfolio Project Assignment 6 Hash_Map with Open Addressing


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash
        table capacity.
        """
        for item in range(self.capacity):
            if self.buckets.get_at_index(item) is not None:
                self.buckets.set_at_index(item, None)
                self.size -= 1



    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None
        """
        # quadratic probing required
        hash_it = self.hash_function(key)
        index = hash_it % self.capacity
        if self.size == 0: #hash map is empty
            return None
        if not self.contains_key(key): # key not found
            return None
        else:
            for item in range(self.size):
                hash_index = (index + item**2) % self.capacity
                if self.buckets.get_at_index(hash_index).key == key:
                    return self.buckets.get_at_index(hash_index).value

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key / value pair in the hash map. If the given key already exists in
        the hash map, its associated value must be replaced with the new value. If the given key is
        not in the hash map, a key / value pair must be added.

        """
        # remember, if the load factor is greater than or equal to 0.5,
        if self.table_load() >= 0.5:
            self.resize_table(self.capacity*2)
        # resize the table before putting the new key/value pair
        # quadratic probing required
        hash_it = self.hash_function(key)
        index = hash_it % self.capacity


        if self.contains_key(key):
            for item in range(self.capacity):
                hash_index = (index + item**2) % self.capacity
                if self.buckets.get_at_index(hash_index).key == key: # replace key assign value
                    self.buckets.set_at_index(hash_index, HashEntry(key, value))
                    return
        else:
            if self.buckets.get_at_index(index) is None:
                self.buckets.set_at_index(index, HashEntry(key, value))
                self.size += 1
            else:
                for item in range(self.capacity):
                    hash_index = (index + item **2) % self.capacity
                    if self.buckets.get_at_index(hash_index) is None or self.buckets.get_at_index(index).is_tombstone == True:
                        self.buckets.set_at_index(hash_index, HashEntry(key, value))
                        self.buckets.get_at_index(hash_index).is_tombstone = False
                        self.size += 1  # update size
                        break



    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing (no exception needs to be raised).

        """
        # quadratic probing required
        hash_it = self.hash_function(key)
        index = hash_it % self.capacity

        if not self.contains_key(key):
            return

        else:
            #key match check tombstone status change status and decrease count
            if self.buckets.get_at_index(index).key == key and self.buckets.get_at_index(index).is_tombstone is False:
                self.buckets.get_at_index(index).is_tombstone = True
                self.size -= 1
            else:
                for item in range(self.capacity):
                    hash_index = (index + item **2) % self.capacity
                    if self.buckets.get_at_index(hash_index) is None:
                        continue
                    if self.buckets.get_at_index(hash_index).key == key and self.buckets.get_at_index(hash_index).is_tombstone is False:
                        self.buckets.get_at_index(hash_index).is_tombstone = True
                        self.size -= 1


    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.
        """
        # quadratic probing required
        hash_it = self.hash_function(key)
        index = hash_it % self.capacity
        if self.size == 0: #empty occurence
            return False
        for item in range(self.capacity): #go through items in Hashmap
            hash_index = (index + item**2) % self.capacity
            if not self.buckets.get_at_index(hash_index):
                return False
            if self.buckets.get_at_index(hash_index).key == key: #Key match check tombstone status
                if self.buckets.get_at_index(hash_index).is_tombstone == True:
                    return False
                elif self.buckets.get_at_index(hash_index).is_tombstone == False:
                    return True
        return False #not in hashmap

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table
        """
        empty_bucket = 0
        for item in range(self.capacity):
            # figure out if bucket is empty and increment count
            if self.buckets.get_at_index(item) is None:
                empty_bucket += 1
        return empty_bucket

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor
        """
        return float(self.size / self.capacity)


    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All existing key / value pairs
        must remain in the new hash map, and all hash table links must be rehashed. If
        new_capacity is less than 1, the method does nothing.
        """

        if new_capacity < 1 or new_capacity <= self.size: # cannot resize less than element amount
            return
        #new hashmap generation
        new_hash_map = HashMap(new_capacity, self.hash_function)
        #iterate through each item in the hashmap
        for item in range(self.capacity):
            old_map = self.buckets.get_at_index(item)
            if old_map is None:
                continue
            if old_map.is_tombstone== True:
                old_map.is_tombstone = False
            else:
                new_hash_map.put(old_map.key, old_map.value)
        self.buckets = new_hash_map.buckets
        self.capacity = new_hash_map.capacity
        self.size = new_hash_map.size

    def get_keys(self) -> DynamicArray:
        """
        This method returns a DynamicArray that contains all the keys stored in the hash map. The
        order of the keys in the DA does not matter
        """
        keys = DynamicArray()
        for item in range(self.capacity):
            if self.buckets.get_at_index(item) is not None:
                if self.buckets.get_at_index(item).is_tombstone == False: #if true then add to DynamicArray
                    keys.append(self.buckets.get_at_index(item).key)
        return keys

if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
