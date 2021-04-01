import random
import string
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L
import datetime
import symmetric
import asymmetric
import csv
from Crypto.PublicKey import RSA
from pyzbar.pyzbar import decode
from PIL import Image
import os
from fnmatch import fnmatch


def add_new_organization(org_name):

    os.mkdir(org_name)
    create_asymmetric_key(org_name)
    create_symmetric_key(org_name)
    print(f'Organization {org_name} was successfully added!\n')
    key_transfer_create(org_name)


def create_asymmetric_key(name):
    with open('passphrases.csv', 'a', newline='') as csvfile:

        fieldnames = ['organization', 'passphrase']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()

        passphrase = password_generator()
        passphrase_coded = symmetric.symmetric_encrypt(passphrase, symmetric.key).hex()

        writer.writerow({'organization':    name,
                         'passphrase':      passphrase_coded})

    with open('keys.csv', 'a', newline='') as csvfile:

        private_key, public_key = asymmetric.generate_keys(bits=2048)

        fieldnames = ['organization', 'public_key', 'private_key']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()

        writer.writerow({'organization':    name,
                         'public_key':      public_key.exportKey(format='PEM').decode(),
                         'private_key':     private_key.exportKey(format='PEM', passphrase=passphrase).decode()})


def create_symmetric_key(name):
    with open('symmetric_keys.csv', 'a', newline='') as csvfile:

        fieldnames = ['organization', 'key']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()

        key = name + password_generator(30)
        writer.writerow({'organization':    name,
                         'key':             key})


def change_symmetric_key(name):

    with open('symmetric_keys.csv') as infile, open('symmetric_keys_temp.csv', 'w') as outfile:

        fieldnames = ['organization', 'key']

        reader = csv.DictReader(infile, fieldnames=fieldnames)
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        for row in reader:
            if row['organization'] == name:
                key = name + password_generator(30)
                writer.writerow({'organization':    name,
                                 'key':             key})
                break
            else:
                writer.writerow(row)
        writer.writerows(reader)

    os.remove('symmetric_keys.csv')
    os.rename('symmetric_keys_temp.csv', 'symmetric_keys.csv')
    print(f'Symmetric key for {name} successfully updated!')


def update_symmetric_key(org_name):
    old_key = get_symmetric_key(org_name)
    change_symmetric_key(org_name)
    counter = 0
    for file in os.listdir(org_name):
        if fnmatch(file, '?*.png'):
            path = org_name + '/' + file
            message = eval(read_cert(path, old_key, output=False))
            create_cert(org_name, message['name'], message['birth_date'], message['id'])
            counter += 1
    print(f'Updated {counter} certificates issued by {org_name}!')
    key_transfer_create(org_name)


def check(certificate, passphrase='roza'):

    print(f'Производится проверка сертификата в папке: {certificate}\n')
    person = {'name': input('Введите ФИО:\n'), 'birth_date': input('Введите дату рождения:\n'),
              'id': input('Введите номер документа удостоверяющего личность:\n')}

    data = eval(read_cert(certificate, output=False))

    if data['name'] == person['name'] and data['birth_date'] == person['birth_date'] and \
            data['id'] == person['id']:
        return print('Сертификат является подлинным!')
    else:
        return print('Сертификат не принадлежит данному человеку!')


def get_symmetric_key(org_name):
    with open('symmetric_keys.csv', newline='') as csvfile:
        fieldnames = ['organization', 'key']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)

        for row in reader:
            if row['organization'] == org_name:
                key = row['key']
                return key

        return print('Invalid organization')


def get_passphrase(name):

    with open('passphrases.csv', newline='') as csvfile:
        fieldnames = ['organization', 'passphrase']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)

        for row in reader:
            if row['organization'] == name:
                passphrase = symmetric.symmetric_decrypt(bytearray.fromhex(row['passphrase']), symmetric.key)
                # print(hex(int(row['passphrase'], 16)))
                return passphrase

        return print('Invalid organization')


def get_private_key(name, passphrase='roza'):

    with open('keys.csv', newline='') as csvfile:
        fieldnames = ['organization', 'public_key', 'private_key', 'passphrase']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)

        for row in reader:
            if row['organization'] == name:
                private_key = RSA.import_key(row['private_key'], passphrase=passphrase)
                return private_key

        return print('Invalid organization')


def get_public_key(name):

    with open('keys.csv', newline='') as csvfile:
        fieldnames = ['organization', 'public_key', 'private_key', 'passphrase']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)

        for row in reader:
            if row['organization'] == name:
                public_key = RSA.import_key(row['public_key'])
                return public_key

        return print('Invalid organization')


def password_generator(length=20):

    letters = string.ascii_letters
    numbers = string.digits
    punctuation = string.punctuation

    printable = f'{letters}{numbers}{punctuation}'

    printable = list(printable)
    random.shuffle(printable)

    random_password = random.choices(printable, k=length)
    random_password = ''.join(random_password)
    return random_password


def create_cert(org_name, name, birth_date, person_id):

    message = str({'organization': org_name,
                   'name':         name,
                   'birth_date':   birth_date,
                   'id':           person_id,
                   'date':         str(datetime.datetime.today())})

    # public_key = get_public_key(org_name)
    # certificate = asymmetric.encrypt_message(message, public_key).hex()

    certificate = org_name + '///' + symmetric.symmetric_encrypt(message, get_symmetric_key(org_name)).hex()

    qr = QRCode(version=None,
                error_correction=ERROR_CORRECT_L,
                box_size=10,
                border=5)
    qr.add_data(certificate)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(f'{org_name}/{name}.png')

    return print(f'QR code for {name} successfully created!')


def read_cert(im_name, key='', output=True):

    try:
        img = Image.open(im_name)
    except FileNotFoundError:
        return print('Такого сертификата не существует!')
    data = str(decode(img)[0].data)[2:-1]
    data = data.split('///', 1)

    if key == '':
        key = get_symmetric_key(data[0])
    data = symmetric.symmetric_decrypt(bytearray.fromhex(data[1]), key)

    if output:
        data = eval(data)
        return print(f'Наименование организации:   {data["organization"]};\n'
                     f'ФИО:                        {data["name"]};\n'
                     f'Дата рождения:              {data["birth_date"]};\n'
                     f'Паспорт:                    {data["id"]};\n'
                     f'Дата вакцинации:            {data["date"]}')
    else:
        return data


def key_transfer_create(org_name):
    key_coded = asymmetric.encrypt_message(get_symmetric_key(org_name), get_public_key(org_name)).hex()
    print(f'Key was transferred to {org_name}: {key_coded}.')

    with open(f'{org_name}.txt', 'w',  newline='') as file:
        file.write(key_coded)


def key_transfer_read(org_name):
    with open(f'{org_name}.txt', 'r', newline='') as file:
        key_coded = file.read()

    key_decoded = asymmetric.decrypt_message(bytearray.fromhex(key_coded),
                                             get_private_key(org_name, get_passphrase(org_name)))
    print(f'Key was received by {org_name} and decoded: {key_decoded}')


if __name__ == '__main__':
    print('It is supporting module, run main')
