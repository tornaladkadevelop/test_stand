import glob
import argparse
import pymysql
from time import sleep

parser = argparse.ArgumentParser(description='A tutorial of argparse!')
parser.add_argument('-bt', default='*', type=str, help='This is the "block_type" variable.')
parser.add_argument('-sn', default='*', type=str, help='This is the "serial_number" variable.')

args = parser.parse_args()
bt = str(args.bt)
sn = str(args.sn)

search = 'd:\Протоколы\**\\' + bt + ('*N') + sn + '*.*'

try:
    connection = pymysql.connect(host='localhost', user='simple_user', passwd='user', database='simple_database')
    sleep(0.5)
except pymysql.err.OperationalError:
    print('Error! Ошибка связи с базой данных MySQL.')


cursor = connection.cursor()
cursor.execute('TRUNCATE simple_database.file_search')
#print(search)
bt = str(bt)
sn = str(sn)

for name in sorted(glob.glob(search, recursive=True)):
    md = name[name.find('_D')+2:-4]
    md = md.replace('_','.')
    md = str(md)
    print(bt, sn, md, name)
    sql = 'INSERT INTO simple_database.file_search (block_type, serial_num, date_verif, fs_path) VALUE (%s, %s, %s, %s)'
    val = (bt, sn, md, name)
    cursor.execute(sql, val)

connection.commit()
connection.close()


a = input('Press key Enter to exit...')
b = input('Press key Enter to exit...')