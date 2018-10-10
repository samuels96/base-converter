import os
import string
from time import sleep

def wrong_inp():
    print('\nWrong input entered')

def inp_constraints(inp, file=None):
    def dec_inp(file=None):
        while True:
            if not file:
                dec = input('\nEnter decimal value > ')
            else:
                dec = file

            try:
                dec = int(dec)
                return dec

            except:
                if file:
                    return
                wrong_inp()

    def bin_inp(file=None):
        while True:
            if not file:
                _bin = input('\nEnter binary value > ')
            else:
                _bin = file

            if _bin[:2] == '0b':
                _bin = _bin[2:]
            else:
                if file:
                    return

            if all(digits in '01' for digits in _bin):
                return _bin
            else:
                if file:
                    return
                wrong_inp()

    def hex_inp(file=None):
        while True:
            if not file:
                hexa = input('\nEnter hexadecimal value > ').lower()
            else:
                hexa = file.lower()

            if hexa[0:2] == '0x':
                hexa = hexa[2:]
            else:
                if file:
                    return

            if all(digits in string.hexdigits for digits in hexa):
                return hexa.lower()

            else:
                if file:
                    return
                wrong_inp()

    def menu_inp(file=None):
        while True:
            inp = input('>>>>>>> ')
            try:
                inp = int(inp)
                return inp
            except:
                wrong_inp()

    inp_list = {'dec':dec_inp, 'bin':bin_inp, 'hexa':hex_inp, 'menu':menu_inp}

    return inp_list[inp](file)

def operations(inp, file=None):
    def dec_to_hex(file=None):
        hexa = list('0123456789ABCDEF')
        output = ''

        dec = inp_constraints('dec', file)

        if file and not dec:
            return 'wrong_inp'

        original_inp = dec

        while dec:
            output = hexa[(dec % 16)] + output
            dec //= 16

        return (original_inp, 'hexadecimal', '0x' + output) if not file else '0x' + output

    def hex_to_dec(file=None):
        output = 0

        hexa = inp_constraints('hexa', file)

        if file and not hexa:
            return 'wrong_inp'

        original_inp = hexa

        hexa = [int(digit) if digit.isdigit() else list('abcdef').index(digit)+10 for digit in hexa]

        for i in range(len(hexa)):
            output += hexa.pop()*(16**i)

        return (original_inp, 'decimal', output) if not file else output

    def dec_to_bin(file=None):
        output = ''

        dec = inp_constraints('dec', file)

        if file and not dec:
            return 'wrong_inp'

        original_inp = dec

        while dec:
            output = str(dec & 1) + output
            dec >>= 1

        return (original_inp, 'binary', '0b' + output) if not file else '0b' + output

    def bin_to_dec(file=None):
        output = 0

        _bin = inp_constraints('bin', file)

        if file and not _bin:
            return 'wrong_inp'

        original_inp = _bin


        for i in range(len(_bin)):
            output += int(_bin[-1-i]) * (2**i)


        return (original_inp, 'decimal', output) if not file else output

    def bin_to_hex(file=None):
        output = []

        _bin = inp_constraints('bin', file)

        if file and not _bin:
            return 'wrong_inp'

        original_inp = _bin

        _bin = [[int(j) for j in _bin[i-4:i]] if len(_bin[i-4:i])==4 else [int(j) for j in _bin[0:i]] for i in range(len(_bin), -1, -4)]

        hexa = list('0123456789ABCDEF')

        for i in _bin[::-1]:
            temp = 0
            for j in range(len(i)):
                temp += i[-1-j] * (2**j)

            if temp > 0:
                output.append(temp)

        output = ''.join([hexa[i] for i in output])

        return (original_inp, 'hexadecimal', '0x' + output) if not file else '0x' + output

    def hex_to_bin(file=None):
        output = ''

        hexa = inp_constraints('hexa', file)

        if file and not hexa:
            return 'wrong_inp'

        original_inp = hexa

        hexa = [int(digit) if digit.isdigit() else list('abcdef').index(digit)+10 for digit in hexa]


        while hexa:
            digit = hexa.pop()
            temp = ''

            while digit:
                temp = str(digit & 1) + temp
                digit >>= 1

            while len(temp) < 4 and hexa:
                temp = '0' + temp

            output = temp + output

        return (original_inp, 'binary', '0b' + output) if not file else '0b' + output

    inp_list = {'d_h':dec_to_hex, 'h_d':hex_to_dec, 'd_b':dec_to_bin, 'b_d':bin_to_dec, 'b_h':bin_to_hex, 'h_b':hex_to_bin}

    return inp_list[inp](file)

def convert(file=None):

    def pipeline(n):
        return '{:>26}'.format('│')

    print('┌'+'─'*24+'─┐')
    print('│ Choose your operation   │'.format(pipeline(0)))
    print("│{0}\n│1. Decimal to Hexadecimal│\n│{0}\n│2. Hexadecimal to Decimal│\n│{0}\n│3. Decimal to Binary{1:>6}\n│{0}\n│4. Binary to Decimal{1:>6}\n│{0}\n│5. Binary to Hexadecimal │\n│{0}\n│6. Hexadecimal to Binary │".format(pipeline(0),'│'))
    print('└'+'─'*25+'┘')
    print('\n')

    while True:
        inp = inp_constraints('menu')

        if 0 < inp < 7:
            break
        else:
            wrong_inp()

    op_list = ['d_h', 'h_d', 'd_b', 'b_d', 'b_h', 'h_b']

    if not file:
        res = '\n│{} in {} is \033[92m{}\033[0m│'.format(*operations(op_list[inp - 1]))
        print('\n┌'+'─'*(len(res)-13)+'─┐' + res + '\n└'+'─'*(len(res)-12)+'┘')

    if file:
        output = []
        while file:
            try:
                line = file[0][0]
            except:
                del file[0]
                output.append('\n')
                continue
            del file[0]

            result = operations(op_list[inp -1], line)

            if result != 'wrong_inp':
                output.append(str(result))

        return output


def main():
    print('\n(Press ctrl-c to quit)')
    print('\n1. Convert values from .txt file \n\n2. Convert values directly \n')

    while True:
        inp = inp_constraints('menu')

        if 0 <= inp < 3:
            os.system('cls')
            break
        else:
            wrong_inp()

    if inp == 1:
        nums = []
        while True:
            rfile = input('\nEnter path to the file -> ')
            try:
                with open(rfile) as f:
                    for line in f:
                        nums.append(line.split())
                    print('\nReading finished...')
                    break
            except:
                print('\nFile does not exist')

        while True:
            wfile = input('\nEnter path for your output file -> ')

            os.system('cls')
            try:
                with open(wfile, 'a+') as f:
                    while nums:
                        for line in convert(nums):
                            f.write(line)
                            f.write('\n')
                print('\nConversion finished...')
                print('\nResults saved to {}'.format(wfile))
                break
            except:
                print('\nWrong file path specified')

    if inp == 2:
        convert()

    try:
        input("\nPress enter to restart the calculator\n")
    except SyntaxError:
        pass

    os.system('cls')
    main()

if __name__ == "__main__":
	main()
