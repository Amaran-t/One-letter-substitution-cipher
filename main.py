import requests

def download_dictionary():
    # Функция для загрузки словаря английских слов через HTTP-запрос
    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
    response = requests.get(url)
    words = response.text.splitlines()
    return set(words)

def encrypt(message, key):
    # Функция для шифрования сообщения методом однобуквенной замены
    encrypted_message = ''
    for char in message:
        if char.isalpha():
            shifted = ord(char) + key
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted_message += chr(shifted)
        else:
            encrypted_message += char
    return encrypted_message

def decrypt(encrypted_message, key):
    # Функция для дешифрования сообщения
    return encrypt(encrypted_message, -key)

def crack(encrypted_message):
    # Функция для взлома шифра методом частотного анализа
    decrypted_texts = []
    english_words = download_dictionary()

    # Попытка расшифровки для всех возможных значений ключа
    for key in range(1, 26):
        decrypted = decrypt(encrypted_message, key)
        decrypted_texts.append(decrypted)

    # Сравнение расшифрованных текстов с английскими словами из словаря
    possible_decryptions = []
    for text in decrypted_texts:
        words = text.split()
        valid_word_count = sum(1 for word in words if word.lower() in english_words)
        possible_decryptions.append((valid_word_count, text))

    # Выбор наиболее вероятной расшифровки по количеству правильных слов
    best_decryption = max(possible_decryptions, key=lambda x: x[0])
    return best_decryption[1]

def main():
    print("Выберите действие:")
    print("E: Зашифровать сообщение")
    print("D: Расшифровать сообщение")
    print("C: Взломать шифр")
    choice = input("Введите ваш выбор: ").upper()

    if choice == 'E':
        message = input("Введите сообщение для шифрования: ")
        shift = int(input("Введите ключ шифрования (число): "))
        encrypted = encrypt(message, shift)
        print("Зашифрованное сообщение:", encrypted)
    elif choice == 'D':
        encrypted_message = input("Введите зашифрованное сообщение: ")
        shift = int(input("Введите ключ, использованный для шифрования: "))
        decrypted = decrypt(encrypted_message, shift)
        print("Расшифрованное сообщение:", decrypted)
    elif choice == 'C':
        encrypted_message = input("Введите зашифрованное сообщение для взлома: ")
        cracked_message = crack(encrypted_message)
        print("Взломанное сообщение:", cracked_message)
    else:
        print("Неверный выбор. Пожалуйста, выберите 'E', 'D' или 'C'.")

if __name__ == "__main__":
    main()
