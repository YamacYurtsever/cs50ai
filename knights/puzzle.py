from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is a knight or knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    # If A is a knight, it is both a knight and a knave
    Implication(AKnight, And(AKnight, AKnave)),
    # If A is a knave, it is false that it is both a knight and a knave
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A and B are knights or knaves but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # If A is a knight, both A and B are knaves
    Implication(AKnight, And(AKnave, BKnave)),
    # If A is a knave, it is false that both A and B are knaves
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A and B are knights or knaves but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # If A is a knight, either both A and B are knight or they are both knaves
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # If A is a knave, it is false that either both A and B are knight or they are both knaves
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

    # If B is a knight, either A is a knight and B is a knave or A is a knave and B is a knight
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # If B is a knave, it is false that either A is a knight and B is a knave or A is a knave and B is a knight
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A, B and C are knights or knaves but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    # If B is a knight, A said that it is a knave
    # Which means that if A is a knight, it is a knave
    # And If A is a knave, it is a knight
    Implication(BKnight, And(Implication(AKnight, AKnave),
                             Implication(AKnave, Not(AKnave)))),
    # Also if B is a knight, C is a knave
    Implication(BKnight, CKnave),

    # If B is a knave, it is false that A said that it is a knave
    # Which means that if A is a knight, it is a knave
    # And If A is a knave, it is a knight
    Implication(BKnave, And(Implication(AKnight, AKnight),
                            Implication(AKnave, Not(AKnight)))),
    # Also if B is a knave, it is false that C is a knave
    Implication(BKnave, Not(CKnave)),

    # If C is a knight, A is a knight
    Implication(CKnight, AKnight),
    # If C is a knave, it is false that A is a knight
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
