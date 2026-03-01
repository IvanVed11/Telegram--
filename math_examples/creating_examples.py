from random import randint
import json
class MultiplicationTable:
    def __init__(self):
         with open("math_examples/multiplication_table.json", "r") as file:
            self.table = json.load(file)
        
    def generate_examples(self):
        examples = {}
        for num1 in range(1, 10):
            for num2 in range(1, 10):
                examples.setdefault(num1, []).append([num1, num2, num1 * num2])
        with open("math_examples/multiplication_table.json", "w") as my_file:
            json.dump(examples, my_file, indent=2)

    def get_examples(self, factor):
        num1, num2, ans = self.table[str(factor)][randint(0, 8)]
        return num1, num2, ans