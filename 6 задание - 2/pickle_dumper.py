import os
import argparse
import pickle
import class_file


parser = argparse.ArgumentParser(description='Сериализуем объекты в файл пикл')
parser.add_argument('-p', '--path', help='Путь файла')
args = parser.parse_args()

obj1 = class_file.MyClass(1, 2)
obj2 = class_file.MyClass(3, 4)
obj_list = [obj1, obj2]
with open(args.path, 'wb') as f:
    pickle.dump(obj_list, f)
if os.path.exists('settings/obj.pickle'):
    print('Pickled successfully!')
