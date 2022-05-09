import argparse
import os


parser = argparse.ArgumentParser(description='Удаление файла')
<<<<<<< HEAD
parser.add_argument('-n', '--name', default='Ksenia', help='Имя пользователя')
parser.add_argument('-p', '--path', help='Путь файла')
parser.add_argument('-nQ', '--noQ', action='store_true', help='Давай без вопросов')
args = parser.parse_args()
print(f'Привет, {args.name}!')
print(args)
=======
parser.add_argument('-n', '--name', default='Anon', help='Имя пользователя')
parser.add_argument('-p', '--path', help='Путь файла')
parser.add_argument('-nQ', '--noQ', action='store_true', help='Давай без ')
parser.add_argument('-cF', '--crFile', action="store_true", help="Do u want to create file? ")
args = parser.parse_args()
print(f'Привет, {args.name}!')
print(args)

if os.path.exists(args.path):
    quest = input(f'\n{args.name}, Вы хотите создать этот файл? (Да/Нет) \n')
    if quest == 'Да' or quest == 'да':
        name = input('Напишите что-нибудь \n')
        with open(args.path, "w+") as f:
            f.write(name)
>>>>>>> origin/main
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


