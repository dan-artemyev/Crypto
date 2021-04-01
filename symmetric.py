from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto import Random
from Crypto.Hash import SHA256


key = 'Traveling through hyperspace ain’t like dusting crops, farm boy.'


def transform_password(password_str):
    """Transform the password string into 32 bit MD5 hash

    :param password_str: <str> password in plain text;
    :return: <str> Transformed password fixed length

    """
    h = MD5.new()
    h.update(password_str.encode())
    return h.digest()


def symmetric_encrypt(message, key, verbose=True):
    """Encrypts the message using symmetric AES algorithm.

    :param message: <str> Message for encryption;
    :param key: <object> symmetric key;
    :param verbose: ;
    :return: <object> Message encrypted with key

    """

    key_MD5 = transform_password(key)
    message_hash = SHA256.new(message.encode())
    message_with_hash = message.encode() + message_hash.hexdigest().encode()
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key_MD5, AES.MODE_CFB, iv)
    encrypted_message = iv + cipher.encrypt(message_with_hash)
    # if verbose:
    #     print(f'Message was encrypted into: {encrypted_message.hex()}')
    return encrypted_message


def symmetric_decrypt(encr_message, key):
    """Decrypts the message using private_key and check it's hash

    :param encr_message: <object> Encrypted message
    :param key: <object> symmetric key;
    :return: <object> Message decrypted with key

    """
    key_MD5 = transform_password(key)

    # Размеры боков нужны, для извлечения их из текста
    bsize = AES.block_size
    dsize = SHA256.digest_size * 2

    iv = Random.new().read(bsize)
    cipher = AES.new(key_MD5, AES.MODE_CFB, iv)
    decrypted_message_with_hash = cipher.decrypt(encr_message)[bsize:]
    decrypted_message = decrypted_message_with_hash[:-dsize]
    digest = SHA256.new(
        decrypted_message).hexdigest()

    if digest == decrypted_message_with_hash[-dsize:].decode():
        # print(
        #     f"Success!\nEncrypted hash is {decrypted_message_with_hash[-dsize:].decode()}\nDecrypted hash is {digest}")
        return decrypted_message.decode()
    else:
        print(
            f"Encryption was not correct: the hash of decripted message doesn't match with encrypted hash\nEncrypted "
            f"hash is {decrypted_message_with_hash[-dsize:]}\nDecrypted hash is {digest}")


if __name__ == '__main__':
    print('It is supporting module, run main')