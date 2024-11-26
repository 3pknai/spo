
# Проверка на наличие больших латинских букв
def big_lat(s):
    for x in range(ord("A"), ord("Z")+1):
        y = chr(x)
        if y in s:
            return True
    return False

# Проверка на наличие маленьких латинских букв
def small_lat(s):
    for x in range(ord("a"), ord("z")+1):
        y = chr(x)
        if y in s:
            return True
    return False

# Проверка на наличие спецсимволов
def spec(s):
    alph = "!@#$%^&*()_+=-.,;:{}[]`~"
    for x in alph:
        if x in s:
            return True
    return False

# Проверка на наличие цифр
def digit(s):
    alph = "0123456789"
    for x in alph:
        if x in s:
            return True
    return False

# Проверка на наличие русских букв
def rus(s):
    s = s.lower()
    alph = "йцукенгшщзхъёфывапролджэюбьтимсчя"
    for x in alph:
        if x in s:
            return True
    return False