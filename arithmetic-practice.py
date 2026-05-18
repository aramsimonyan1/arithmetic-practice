import random
import operator

# Available operations
OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv  # integer division
}

def get_random_number(max_val):
    return random.randint(1, max_val if max_val else 100)

def generate_expression(max_result=None, num_operators=1, allowed_ops=None):
    if not allowed_ops:
        allowed_ops = ["+", "-", "*", "/"]

    while True: # retry until valid expression is generated
        expr = []
        current_value = get_random_number(max_result or 50)
        expr.append(str(current_value))

        for _ in range(num_operators):
            op = random.choice(allowed_ops)
            next_num = get_random_number(max_result or 50)

            # Apply operation carefully
            try:
                if op == "+":
                    result = current_value + next_num
                elif op == "-":
                    result = current_value - next_num
                elif op == "*":
                    result = current_value * next_num
                elif op == "/":
                    if next_num == 0 or current_value % next_num != 0:
                        raise ValueError
                    result = current_value // next_num

                # Enforce constraints
                if max_result is not None and (result < 0 or result > max_result):
                    raise ValueError

                current_value = result
                expr.append(op)
                expr.append(str(next_num))

            except:
                break # invalid step → restart whole expression
        else:
            # successfully built full expression
            return " ".join(expr), current_value


def main():
    # --- User settings ---
    max_result = input("Enter max result (or press Enter for no limit): ")
    max_result = int(max_result) if max_result else None

    num_ops = int(input("How many operators per question? ")) 

    print("Choose operators (+, -, *, /). Example: + - *") # separate operators with spaces 
    ops_input = input("Operators: ").split()

    mode = input("Same operator only? (y/n): ").lower()

    if mode == "y":
        chosen_op = random.choice(ops_input)
        allowed_ops = [chosen_op]
    else:
        allowed_ops = ops_input

    rounds = int(input("How many questions would you like to answer? "))

    # --- Score tracking ---
    score = 0
    correct_answers = 0
    wrong_answers = 0

    # --- Generate a question ---
    for question_num in range(1, rounds + 1):
        expr, answer = generate_expression(max_result, num_ops, allowed_ops)

        print(f"\nQuestion {question_num}/{rounds}")
        print(f"Solve: {expr}")

        try:
            user_answer = int(input("Your answer: "))
        except ValueError:
            user_answer = None

        if user_answer == answer:
            print("✅ Correct!")
            score += 1
            correct_answers += 1
        else:
            print(f"❌ Wrong! Correct answer: {answer}")
            wrong_answers += 1

        print(f"Current Score: {score}/{question_num}")

    # --- Final Results ---
    percentage = (score / rounds) * 100

    print("\n===== FINAL SCORE =====")
    print(f"Correct Answers : {correct_answers}")
    print(f"Wrong Answers   : {wrong_answers}")
    print(f"Total Score     : {score}/{rounds}")
    print(f"Percentage      : {percentage:.1f}%")

if __name__ == "__main__":
    main()