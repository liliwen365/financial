import itertools as its


# 密码生成器
# :param min_digits: 密码最小长度
# :param max_digits: 密码最大长度
# :param words: 密码可能涉及的字符
# :return: 密码
def get_password(min_digits, max_digits, words):
    while min_digits <= max_digits:
        pwds = its.product(words, repeat=min_digits)
        for pwd in pwds:
            yield ''.join(pwd)

        min_digits += 1


def main():
    # 密码范围
    # words = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    words = '0123456789'
    pwds = get_password(8, 8, words)

    # 写入 txt 文本
    a = open('C:/Users/931304/Desktop/password.txt', 'a')
    while True:
        try:
            pwd = next(pwds)
            a.write(str(pwd) + '\n')
        except StopIteration:
            break
    a.close()


main()