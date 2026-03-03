from random import randint
from collections import Counter

async def generate_examples_and_keyboards(factor, kb_class):
    examples = []
    keyboard_with_answers = []
    counter = Counter()

    while len(examples) < 10:
        num = randint(1, 9)
        ans = factor * num
        for example in examples:
            if example[1] == num:
                counter[num] += 1
        if counter[num] < 2 and not examples: 
            examples.append([factor, num, ans])
            keyboard_with_answers.append(kb_class.generate_multiplicate_answers(ans))
        elif counter[num] < 2 and examples and examples[-1][1] != num: 
            examples.append([factor, num, ans])
            keyboard_with_answers.append(kb_class.generate_multiplicate_answers(ans))

    return examples, keyboard_with_answers