"""
Створіть функцію <morse_code>, яка приймає на вхід рядок у вигляді коду
Морзе та виводить декодоване значення (латинськими літерами).
   Особливості:
    - використовуються лише крапки, тире і пробіли (.- )
    - один пробіл означає нову літеру
    - три пробіли означають нове слово
    - результат може бути case-insensitive
    (на ваш розсуд - великими чи маленькими літерами).
    - для простоти реалізації - цифри, знаки пунктуацїї, дужки,
    лапки тощо використовуватися не будуть. Лише латинські літери.
    - додайте можливість декодування сервісного сигналу SOS (...---...)
"""
MORSE_CODE = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z',
    '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
    '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
    '.-.-.-': '.', '--..--': ',', '..--..': '?', '.----.': "'", '-.-.--': '!',
    '-..-.': '/', '-.--.': '(', '-.--.-': ')', '.-...': '&', '---...': ':',
    '-.-.-.': ';', '-...-': '=', '.-.-.': '+', '-....-': '-', '..--.-': '_',
    '.-..-.': '"', '...-..-': '$', '.--.-.': '@', '...---...': 'SOS'
}


# One-liner favorite practice :)))))
def morse_code_oneliner(morse_code):
    """ Accept dots, dashes and spaces, return human-readable message"""
    return " ".join(["".join(MORSE_CODE[letter] for letter in word.split(" ")) for word in morse_code.strip().split("   ")])


# Best practice
def morse_decode(morse_code=''):
    """ Accept dots, dashes and spaces, return human-readable message"""
    morse_code = morse_code.strip()
    if not morse_code:
        return False
    else:
        decode = ''
        lst = morse_code.strip().split('   ')
        for word in lst:
            for letter in word.split(' '):
                decode += MORSE_CODE.get(letter)
            decode += ' '
        return decode.strip()


if __name__ == '__main__':
    morse = ".. ...   .... . .-. ."
    print(morse_decode(morse))
    print(morse_code_oneliner(morse))
