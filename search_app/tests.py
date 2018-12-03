from django.test import TestCase

# Create your tests here.
def addSalt(password):
    l = '1234567890qweiosdfghjklzxcvbnm,\./!@#$%^&*()[]~=-+的刷卡积分和喀什地方就哈'
    salt = ''.join(random.sample(l, 6))
    hash_code = hashlib.md5()
    password = str(password) + salt
    hash_code.update(password.encode())
    secret_key =hash_code.hexdigest()
    print(salt, secret_key, '随机数与其哈希')
    return salt,secret_key
print(addSalt(123))