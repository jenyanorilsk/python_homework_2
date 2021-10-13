import os
import tempfile


class File(object):

    def __init__(self, file_name):
        self.file_name = os.path.abspath(file_name)
        self.file_obj = open(file_name, 'w+')

    def __enter__(self):
        self.file_obj.seek(0)
        return self.file_obj

    def __exit__(self, type, value, traceback):
        self.file_obj.close()

    def __str__(self):
        return self.file_name

    def __add__(self, other):
        os_handle, file_name = tempfile.mkstemp(dir=tempfile.gettempdir(), text=True)
        result = File(file_name)
        result.write(self.read())
        result.write(other.read())
        return result

    def __iter__(self):
        self.file_obj.seek(0)
        return self.file_obj

    def __next__(self):
        if self.file_obj.readable():
            return self.file_obj.readline()
        raise StopIteration

    def read(self):
        self.file_obj.seek(0)
        return ''.join(self.file_obj.readlines())

    def write(self, content):
        self.file_obj.write(content)


if __name__ == '__main__':

    path = './text1.txt'
    print('rel path:', path)
    print('is file exists:', os.path.exists(path))
    txt_file_first = File('./text1.txt')
    print('is file exists:', os.path.exists(path))
    print('full path:', txt_file_first)

    print()
    print('=====================')
    print('file content:')
    print(txt_file_first.read())
    txt_file_first.write('this is a text for a first file\n')
    print('file content:')
    print(txt_file_first.read())

    txt_file_second = File('./text2.txt')
    txt_file_second.write('this is a text for second file\n')

    sum_text_file = txt_file_first + txt_file_second
    print()
    print('=====================')
    print('is File:', isinstance(sum_text_file, File))
    print('path:', sum_text_file)
    print('content:')
    print(sum_text_file.read())

    print()
    print('=====================')
    for tmp in sum_text_file:
        print(tmp, end='')
