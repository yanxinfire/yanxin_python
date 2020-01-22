from collections import defaultdict
import re


def parse(infile, outfile):
    d = defaultdict(int)

    with open(infile, 'r', encoding='utf-8') as f1:
        last_piece = ''
        while 1:
            text = f1.read(1000).lower()
            if not text:
                d[last_piece] += 1
                break
            text = re.sub(r'[^\w\']+', ' ', text)
            combine = last_piece + text
            words = combine.split(' ')
            # Here we assume that a word can be very very long.
            if len(words) > 1:
                for word in words[:-1]:
                    d[word] += 1
                last_piece = words[-1]
            else:
                last_piece = combine
    with open(outfile, 'w', encoding='utf-8') as f2:
        for key in d:
            f2.write(f'{key} {d[key]}\n')


if __name__ == '__main__':
    parse('exam1', 'out1.txt')
