from cryptography.fernet import Fernet
import sys
import os


def generate_key() -> str:
    """Сгенерировать ключ

    Returns:
        str: Ключ
    """
    return Fernet.generate_key().decode()


def encrypt(data: str, key: str) -> str:
    """Зашифровать данные

    Args:
        data (str): Полезная нагрузка
        key (str): Ключ

    Returns:
        str: Зашифрованная полезная нагрузка
    """
    fernet = Fernet(key.encode())
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()


def decrypt(encrypted_data: str, key: str) -> str:
    """Расшифровка по ключу

    Args:
        encrypted_data (str): Зашифрованная полезная нагрузка
        key (str): Ключ

    Returns:
        str: Расшифрованная полезная нагрузка
    """
    fernet = Fernet(key.encode())
    decrypted_data = fernet.decrypt(encrypted_data.encode())
    return decrypted_data.decode()


def read_file(filepath: str) -> str:
    """Чтение файла

    Args:
        filepath (str): Путь к файлу

    Returns:
        str: Текст файла
    """
    with open(filepath, "r") as file:
        text = file.read()
    return text


def write_file(filepath: str, payload: str) -> None:
    """Запись в файл

    Args:
        filepath (str): Путь к файлу
        payload (str): Текст файла
    """
    with open(filepath, "w") as file:
        file.write(payload)


def find_all_envs(start_dir: str = ".", crypted: bool = False) -> list[str]:
    """Поиск всех .env файлов

    Args:
        start_dir (str): Стартовая директория. Defaults to ".".
        crypted (bool): Зашифрованные или расшифрованные. Defaults to False.

    Returns:
        list[str]: Все .env в директории
    """
    env_files = []
    for root, _, files in os.walk(start_dir):
        for file in files:
            if crypted:
                if file.endswith(".crypt"):
                    env_files.append(os.path.join(root, file))
            else:
                if file.endswith(".env"):
                    env_files.append(os.path.join(root, file))
    return [file.replace(r"\\", "\\") for file in env_files]


def config_encrypt(secret_key: str) -> None:
    """Полная зашифровка всех .env файлов

    Args:
        secret_key (str): Секртеный ключ
    """
    env_files = find_all_envs()

    for env_file in env_files:
        data = read_file(env_file)
        encrypted_data = encrypt(data, secret_key)
        write_file(env_file + ".crypt", encrypted_data)


def config_decrypt(secret_key: str) -> None:
    """Полная расшифровка всех .env файлов

    Args:
        secret_key (str): Ключ
    """
    env_files = find_all_envs(crypted=True)

    for env_file in env_files:
        encrypted_data = read_file(env_file)
        try:
            original_data = decrypt(encrypted_data, secret_key)
            write_file(env_file.replace(".crypt", ""), original_data)
            print(f"Файл {env_file} успешно расшифрован.")
        except Exception as e:
            print(f"Ошибка расшифровки файла {env_file}: {e}")


def help() -> None:
    """Сообщение помощи"""
    print("""
Автошифроватор конфигов by Marsvest

python secure_config.py help
Показать это сообщение

python secure_config.py genkey
Сгенерировать поддерживаемый ключ

python secure_config.py encrypt <SECRET_KEY>
Зашифровать все .env файлы в репозитории
<SECRET_KEY> - Ключ для расшифровки

python secure_config.py decrypt <SECRET_KEY>
Расшифровать все .env файлы в репозитории
<SECRET_KEY> - Ключ для расшифровки
          """)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        operation = sys.argv[1]

        if operation == "genkey":
            print(generate_key())
        elif operation == "help":
            help()

        sys.exit(0)

    elif len(sys.argv) < 3:
        help()
        sys.exit(1)

    operation = sys.argv[1]
    secret_key = sys.argv[2]

    # Расшифровка
    if operation == "decrypt":
        config_decrypt(secret_key)
    # Зашифровка
    elif operation == "encrypt":
        config_encrypt(secret_key)
    else:
        help()
