def encode_base62(id):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(characters)
    encoded = []
    while id > 0:
        id, rem = divmod(id, base)
        encoded.append(characters[rem])
    return ''.join(reversed(encoded)).rjust(7, '0')

