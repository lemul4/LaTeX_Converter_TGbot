"""Модуль с функцией для конвертации с упрощенного языка записи математических выражений в латекс"""


def converter(string):
    string = string.replace('*', '\cdot')

    string = string.replace('∙', '\cdot')

    string = string.replace('∞', '\infty')

    string = string.replace('pi', '\pi')

    string = string.replace(' ', '')

    string = string.replace('sqrt', '\sqrt')

    while string.count('/'):
        sym = string.find('/')
        left_string = string[:sym]
        right_string = string[sym+1:]
        string = left_string[:left_string.rfind('(')] + r'\frac{' + left_string[left_string.rfind(
            '(')+1:-1] + "}{" + right_string[1:right_string.find(')')] + '}' + right_string[right_string.find(')')+1:]

    for i in range(len(string)):
        count = 0
        if string[i:i+4] == 'sqrt':
            right_string = string[i+4:]
            left_string = string[:i+4]
            for j in range(len(right_string)):
                sym = right_string[j]
                if sym == '(':
                    if count == 0:
                        right_string = right_string[:j]+'{'+right_string[j+1:]
                    count += 1
                if sym == ')':
                    if count == 1:
                        right_string = right_string[:j]+'}'+right_string[j+1:]
                        break
                    else:
                        count -= 1
            string = left_string+right_string

    for i in range(len(string)):
        count = 0
        if string[i] == '^':
            right_string = string[i:]
            left_string = string[:i]
            for j in range(len(right_string)):
                sym = right_string[j]
                if sym == '(':
                    if count == 0:
                        right_string = right_string[:j]+'{'+right_string[j+1:]
                    count += 1
                if sym == ')':
                    if count == 1:
                        right_string = right_string[:j]+'}'+right_string[j+1:]
                        break
                    else:
                        count -= 1
            string = left_string+right_string

    string = '$$' + string + '$$'
    return string
