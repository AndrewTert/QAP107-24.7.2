import pytest

from api import PetFriends
from settings import valid_email, valid_password, valid_email_second_account
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Котофей', animal_type='Кот',
                                     age='4', pet_photo='white_cat.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), 'images', pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Суперкот", "Кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Котлетка', animal_type='Кот', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Далее 10 проверок по заданию

def test_simple_add_new_pet_with_valid_data(name='Котяра', animal_type='Кот', age='2'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_photo_with_valid_data(pet_photo='white_cat.jpg'):
    """Проверяем возможность установки фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), 'images', pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


@pytest.mark.parametrize("name", ["gggggggggggggggggggggggggggggggfffffffffffffffffffffffffffffffffffffffffffffff"
                                  "fffffffffffffffffffffffffffffffffffffffffffffffhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
                                  "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhrrrrrrrrrrrrrrrrrrrrrrrrrr"
                                  "rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr", ""])
@pytest.mark.parametrize("animal_type", ["", '"-_=+/!@#$%^&*('])
@pytest.mark.parametrize("age", ["-1", "1000000000000000000000000000000", ""])
def test_simple_add_new_pet_with_wrong_data(name, animal_type, age):
    """Проверяем добавление питомца с не корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_simple_add_new_pet_with_wrong_auth(name="TestName", animal_type="TestType", age="1"):
    """Проверяем добавление питомца с не корректным ключом auth_key"""

    auth_key = {"key": "ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729"}
    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


def test_simple_add_new_pet_with_empty_auth(name="TestName", animal_type="TestType", age="1"):
    """Проверяем добавление питомца с пустым ключом auth_key"""

    auth_key = {"key": ""}
    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


def test_add_new_pet_with_broken_photo(name='broken', animal_type='broken',
                                       age='broken_photo', pet_photo='broken.jpg'):
    """Проверяем что можно добавить питомца с поломанной фотографией"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), 'images', pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


@pytest.mark.parametrize("email", ["", '"-_=+/!@#$%^&*(', "111dsas@goglu.com"])
@pytest.mark.parametrize("password", ["", "'/-_=+/!@#$%^&*("])
def test_get_api_key_for_nonexistent_user(email, password):
    """ Проверяем что запрос api ключа для некорректных пар е-мэйл/пароль возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


def test_get_all_pets_with_wrong_filter(my_filter='pet'):
    """ Проверяем что запрос всех питомцев с некорректным фильтром выдает ошибку 500"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, my_filter)

    assert status == 500


def test_delete_self_pet_wrong_auth():
    """Проверяем возможность удаления питомца с некорректным ключом auth_key"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Фломастер", "красный", "5")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    auth_key = {"key": ""}
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Проверяем что статус ответа равен 403
    assert status == 403


def test_delete_pet_in_another_account():
    """Проверяем возможность удаления питомца из чужого аккаунта"""

    # Получаем свой ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, other_auth_key = pf.get_api_key(valid_email_second_account, valid_password)
    _, other_pets = pf.get_list_of_pets(other_auth_key, "my_pets")

    # Проверяем - если список питомцев на втором аккаунте пустой,
    # то добавляем нового и опять запрашиваем список питомцев
    if len(other_pets['pets']) == 0:
        pf.add_new_pet_simple(other_auth_key, "Фломастер", "красный", "5")
        _, other_pets = pf.get_list_of_pets(other_auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = other_pets['pets'][0]['id']

    # Используем id питомца со второго аккаунта и отправляем запрос на удаление с первого аккаунта
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, other_pets = pf.get_list_of_pets(other_auth_key, "my_pets")

    if len(other_pets['pets']) == 0 or pet_id not in other_pets.values():
        raise Exception("Удален питомец из чужого аккаунта")
    assert status != 200
