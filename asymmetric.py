from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP


def generate_keys(bits=2048):
    """Generates the pair of private and public keys.

    :param bits: <int> Key length, or size (in bits)
    of the RSA modulus (default 2048)
    :return: <object> private_key, <object> public_key

    """
    private_key = RSA.generate(bits)
    public_key = private_key.publickey()
    return private_key, public_key


def encrypt_message(message, public_key, verbose=True):
    """Encrypts the message using public_key.

    :param message: <str> Message for encryption
    :param public_key: <object> public_key
    :param verbose: <bool> Print description;
    :return: <object> Message encrypted with public_key

    """
    message_hash = SHA256.new(message.encode())
    cipher = PKCS1_OAEP.new(public_key)
    message_with_hash = message.encode() + message_hash.hexdigest().encode()
    encrypted_message = cipher.encrypt(message_with_hash)
    # if verbose:
    #     print(f'Message: {message} was encrypted to\n{encrypted_message.hex()}')
    return encrypted_message


def decrypt_message(encrypted_message, private_key):
    """Decrypts the message using private_key and check it's hash

    :param encrypted_message: <object> Encrypted message
    :param private_key: <object> private_key
    :return: <object> Message decrypted with private_key

    """
    dsize = SHA256.digest_size * 2
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message_with_hash = cipher.decrypt(encrypted_message)
    decrypted_message = decrypted_message_with_hash[:-dsize]
    digest = SHA256.new(decrypted_message).hexdigest()
    if digest == decrypted_message_with_hash[-dsize:].decode():
        # print(
        #     f"Success!\nEncrypted hash is {decrypted_message_with_hash[-dsize:].decode()}\n
        #     Decrypted hash is {digest}")
        return decrypted_message.decode()
    else:
        print(
            f"Encryption was not correct: the hash of decrypted message doesn't match with encrypted hash\nEncrypted "
            f"hash is {decrypted_message_with_hash[-dsize:]}\nDecrypted hash is {digest}")


if __name__ == '__main__':
    print('It is supporting module, run main')
