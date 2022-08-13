class FlatIterator:
    def __init__(self, little_list):
        self.list = little_list

    def __iter__(self):
        self.start = 0
        self.deeper = -1
        return self

    def __next__(self):
        self.deeper += 1
        if self.deeper == len(self.list[self.start]):
            self.start += 1
            self.deeper = 0
        if self.start == len(self.list):
            raise StopIteration
        return self.list[self.start][self.deeper]


if __name__ == '__main__':
    nested_list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False, ['666']],
        [1, 2, None],
    ]
    for item in FlatIterator(nested_list):
        print(item)
    flat_list = [item for item in FlatIterator(nested_list)]
    print(flat_list)
