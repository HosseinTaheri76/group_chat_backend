import re
from rest_framework.serializers import ValidationError


def username_validator(value):
    pattern = re.compile(r'^[a-zA-Z]\w{5,14}$')
    if pattern.match(value):
        return value
    raise ValidationError('نام کاربری میبایست حداقل 6 کاراکتر باشد که کاراکتر اول آن الز'
                          'اما از الفبا باشد , کاراکتر های مجاز الفبا اعداد و _ می باشند')


def password_validator(value):
    pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    if pattern.match(value):
        return value
    raise ValidationError('رمز عبور میبایست لااقل 8 کاراکتر باشد و حداقل حاوی یک عدد و یک حرف باشد')
