import itertools
from collections import defaultdict

from utils.input import read_file, read_batches
from utils.narrow_down import narrow_down_sets


def parse_ingredients(line):
    ingredients, contains = line.split("(")
    contains = contains.split(" ")
    contains = [c[:-1] for c in contains[1:]]
    ingredients = ingredients.strip().split(" ")
    return ingredients, contains


def find_allergen_ingredients(ingredient_allergens):
    allergens = set()
    for i_a in ingredient_allergens:
        _allergens = i_a[1]
        for allergen in _allergens:
            allergens.add(allergen)
    print(allergens)
    allergen_possibilities = {a: None for a in allergens}
    for i_a in ingredient_allergens:
        _allergens = i_a[1]
        for a in _allergens:
            if allergen_possibilities[a] is None:
                allergen_possibilities[a] = set(i_a[0])
            else:
                allergen_possibilities[a] = allergen_possibilities[a].intersection(set(i_a[0]))
    return allergen_possibilities


def main():
    lines = read_file("input.txt")
    ingredient_allergens = [parse_ingredients(line) for line in lines]
    allergen_possibilities = find_allergen_ingredients(ingredient_allergens)
    allergen_ingredients = set()
    for allergen, ingredients in allergen_possibilities.items():
        for i in ingredients:
            allergen_ingredients.add(i)
    total = 0
    for i_a in ingredient_allergens:
        ingredients = i_a[0]
        for i in ingredients:
            if i not in allergen_ingredients:
                total += 1
    print(total)
    narrowed_down = narrow_down_sets(allergen_possibilities)
    for a in sorted(narrowed_down.keys()):
        print(f"{a}: {narrowed_down[a]}")


if __name__ == "__main__":
    main()
