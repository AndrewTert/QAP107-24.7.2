# QAP107-24.7.2

В директории /tests располагается файл с тестами

Для работы приложения нужно установить библиотеки: requests, pytest, requests-toolbelt, dotenv:

    pip install requests
    pip install requests-toolbelt
    pip install pytest
    pip install dotenv

Также необходимо создать в корневой папке проекта файл **.env** со следущим содержимым:

    valid_email = "abyrvalg@mumu.com"
    valid_pass = "123323"
    valid_email_second_account = "abyrvalg@mumu1.com"

В рамках домашней работы были разработаны методы:

    add_new_pet_simple
    set_pet_photo
    
а также 10 тестов:

    test_simple_add_new_pet_with_valid_data
    test_add_photo_with_valid_data
    test_simple_add_new_pet_with_wrong_data
    test_simple_add_new_pet_with_wrong_auth
    test_simple_add_new_pet_with_empty_auth
    test_add_new_pet_with_broken_photo
    test_get_api_key_for_nonexistent_user
    test_get_all_pets_with_wrong_filter
    test_delete_self_pet_wrong_auth
    test_delete_pet_in_another_account
