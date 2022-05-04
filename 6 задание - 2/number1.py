import argparse
import os


parser = argparse.ArgumentParser(description='Удаление файла')
parser.add_argument('-n', '--name', default='Ksenia', help='Имя пользователя')
parser.add_argument('-p', '--path', help='Путь файла')
parser.add_argument('-nQ', '--noQ', action='store_true', help='Давай без вопросов')
args = parser.parse_args()
print(f'Привет, {args.name}!')
print(args)
if os.path.exists(args.path):
    if args.noQ:
        os.remove(args.path)
        exit(0)
    else:
        question = input('Вы хотите удалить этот файл? (Да/Нет) \n')
        if question == 'Да' or question == 'да':
            os.remove(args.path)
            print('Файл удален!')
        else:
            print('Файл не был удален')
else:
    print('Такой файл не существует')


