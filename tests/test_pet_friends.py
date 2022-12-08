from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Эмили', animal_type='папильон', age='4', pet_photo='images/dog1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Боня", "щенок", "1", "images/dog2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Сара', animal_type='собака', age=0):
    """Проверяем возможность обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:

        raise Exception("There is no my pets")


def test_add_new_pet_simple_with_valid_data(name='Эмили', animal_type='собака', age='4' ):
    """Проверяем что можно добавить питомца с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    print(result)
    assert status == 200
    assert result['name'] == name


def test_add_pet_photo_with_valid_data(pet_photo ='images/52ef623f10eb7c17761a38ca594a0b99.jpeg'):
    """Проверяем что можно добавить фото питомца """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_pet_winch_photo(auth_key, pet_id, pet_photo )

    print(result)
    assert status == 200
    assert result["pet_photo"] is not None

def test_get_api_key_for_valid_user_negative():
    """ Проверяем что запрос api ключа возвращает статус 403 при неправильном вводе email"""
    email = "invalid_email"
    password = valid_password

    status, result = pf.get_api_key(email, password)
    print(result)
    assert status == 403


def test_get_api_key_for_valid_user_negative():
    """ Проверяем что запрос api ключа возвращает статус 403 при неправильном вводе password"""
    email = "valid_email"
    password = "invalid_password"

    status, result = pf.get_api_key(email, password)
    print(result)
    assert status == 403


def test_add_new_pet_with_valid_data_negative(name='Эмили', animal_type='', age='2', pet_photo='images/dog1.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными
    (обязательное поле заполнения animal_type заполнили пустым) Баг. """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    print(result)
    assert status == 200
    assert result['animal_type'] == animal_type

def test_add_new_pet_with_valid_data_negative(name='', animal_type='собака', age='2', pet_photo='images/dog1.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными
    (обязательное поле заполнения name заполнили пустым) Баг. """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    print(result)
    assert status == 200
    assert result['name'] ==  name

def test_successful_update_self_pet_info_negative(name="12345", animal_type='собака', age=0):
    """Проверяем возможность обновления информации о питомце. Ввод группы цифр в текстовое значение name """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:

        raise Exception("There is no my pets")
    print(my_pets)

def test_add_pet_photo_with_valid_data_negative(pet_photo ='images/on-the-run-maltipu-little-dog-is-posing_155003-22631.webp'):
    """Проверяем что можно добавить фото питомца в формате webp.
     Формат не соответствует с требованиями документации (JPG, JPEG и PNG) Баг"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']                                                                     

    status, result = pf.add_pet_winch_photo(auth_key, pet_id, pet_photo )

    print(result)
    assert status == 200
    assert result["pet_photo"] is not None

def test_successful_delete_self_pet_2():
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Боня", "щенок", "1", "images/dog2.jpg")
        pf.add_new_pet(auth_key, "Sara", "dog", "1", "images/dog1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][-1]['id']
    status, result = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    print(result)
    assert status == 200
    assert pet_id not in my_pets.values()


def test_add_new_pet_simple_with_valid_data_negative(name='Эмили', animal_type="@#$%^&*", age='4' ):
    """Проверяем что можно добавить питомца с некорректными данными.
    атрибут animal_typ принимает значение из спецсимволов. Баг"""
                                                                                                  
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    print(result)
    assert status == 200
    assert result['animal_type'] == animal_type
