import helpers
import time


def test_creation_time(org_name, amount):
    for n in range(amount):
        helpers.create_cert(org_name, f'Name {n}', f'{n}.{n}.{n}', f'{n}*10')


def create_organizations(amount):
    for n in range(1, amount + 1):
        helpers.add_new_organization(f'org{n}')
    # helpers.add_new_organization('org1')
    # helpers.add_new_organization('org2')
    # helpers.add_new_organization('org3')
    # helpers.add_new_organization('org4')
    # helpers.add_new_organization('org5')
    # helpers.add_new_organization('org6')
    # helpers.add_new_organization('org7')
    # helpers.add_new_organization('org8')
    # helpers.add_new_organization('org9')
    # helpers.add_new_organization('org10')


def create_certificates():

    helpers.create_cert('org1', 'Иванов Петр Геннадьевич', '10.02.1975', '4013803456')
    helpers.create_cert('org1', 'Тузов Николай Васильевич', '11.05.1990', '4023345672')
    helpers.create_cert('org1', 'Поздняков Сергей Федорович', '14.11.1987', '4012675490')
    helpers.create_cert('org1', 'Ремизов Евгений Васильевич', '02.03.1998', '4923449043')
    helpers.create_cert('org1', 'Крутов Иван Денисович', '31.01.1964', '4678924554')

    helpers.create_cert('org2', 'Федоров Петр Петрович', '24.08.1995', '6574893564')
    helpers.create_cert('org2', 'Тузов Иван Васильевич', '23.02.1981', '8735273744')
    helpers.create_cert('org2', 'Кучин Егор Семенович', '30.06.2000', '5672947653')
    helpers.create_cert('org2', 'Пташкин Алексей Евгеньевич', '18.09.1999', '1254326493')
    helpers.create_cert('org2', 'Вислоухов Геннадий Федорович', '03.09.1996', '8469687790')

    helpers.create_cert('org3', 'Собакевич Ефим Викторович', '08.10.1978', '9087846673')
    helpers.create_cert('org3', 'Леоненков Виктор Александрович', '09.09.2002', '8478896345')
    helpers.create_cert('org3', 'Семенов Михаил Александрович', '10.11.1988', '3098567489')
    helpers.create_cert('org3', 'Козлов Иван Даниилович', '13.12.1958', '6358497624')
    helpers.create_cert('org3', 'Кошкин Игорь Федорович', '19.05.1993', '9484857363')

    helpers.create_cert('org4', 'Смелый Николай Егорович', '03.07.1997', '9484848483')
    helpers.create_cert('org4', 'Хорев Анатолий Васильевич', '14.02.1966', '3647837857')
    helpers.create_cert('org4', 'Крюков Андрей Федорович', '11.01.1981', '4457847384')
    helpers.create_cert('org4', 'Лазарев Петр Георгиевич', '15.03.2000', '2332456768')
    helpers.create_cert('org4', 'Долматов Никита Сергеевич', '19.01.2001', '8578940484')

    helpers.create_cert('org5', 'Егоров Глеб Витальевич', '09.05.1983', '9404909087')
    helpers.create_cert('org5', 'Филиппов Николай Андреевич', '18.10.1949', '4909896543')
    helpers.create_cert('org5', 'Яковлев Семен Федорович', '17.11.1973', '465789098')
    helpers.create_cert('org5', 'Леонов Константин Борисович', '24.01.1979', '5653767898')
    helpers.create_cert('org5', 'Морев Андрей Витальевич', '04.03.1987', '4528394084')


if __name__ == '__main__':

    start_time = time.time()

    org_name = 'org1'

    create_organizations(5)
    # create_certificates()

    # helpers.read_cert('org1/Иванов Петр Геннадьевич.png')
    # helpers.update_symmetric_key(org_name)
    # helpers.key_transfer_create(org_name)
    # helpers.key_transfer_read(org_name)

    # test_creation_time(org_name, 10)
    # helpers.update_symmetric_key(org_name)

    # helpers.check('org1/Иванов Петр Геннадьевич.png')

    print("--- %s seconds ---" % (time.time() - start_time))
