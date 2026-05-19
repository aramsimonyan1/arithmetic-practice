import random
import operator
import customtkinter as ctk
from tkinter import messagebox

# -----------------------------
# Configuration
# -----------------------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# -----------------------------
# Math Operations
# -----------------------------
OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv
}

# -----------------------------
# Question Generator
# -----------------------------
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
            next_num = get_random_number(max_result or 20)

            # Apply operation carefully
            try:
                if op == "+":
                    result = current_value + next_num

                elif op == "-":
                    result = current_value - next_num

                elif op == "*":
                    result = current_value * next_num

                elif op == "/":
                    # Ensure clean division
                    if next_num == 0 or current_value % next_num != 0:
                        raise ValueError

                    result = current_value // next_num

                # Validate result limits
                if max_result is not None:
                    if result < 0 or result > max_result:
                        raise ValueError

                current_value = result

                expr.append(op)
                expr.append(str(next_num))

            except:
                break # invalid step → restart whole expression

        else:
            return " ".join(expr), current_value # successfully built full expression


# -----------------------------
# Main App
# -----------------------------
class MathPracticeApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Arithmetic Practice")
        self.geometry("700x550")

        self.score = 0
        self.total_questions = 0
        self.current_answer = None

        # -----------------------------
        # Title
        # -----------------------------
        self.title_label = ctk.CTkLabel(
            self,
            text="Arithmetic Practice",
            font=("Arial", 28, "bold")
        )
        self.title_label.pack(pady=20)

        # -----------------------------
        # Settings Frame
        # -----------------------------
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.pack(padx=20, pady=10, fill="x")

        # Max Result
        self.max_result_label = ctk.CTkLabel(
            self.settings_frame,
            text="Max Result:"
        )
        self.max_result_label.grid(row=0, column=0, padx=10, pady=10)

        self.max_result_entry = ctk.CTkEntry(
            self.settings_frame,
            placeholder_text="Optional"
        )
        self.max_result_entry.grid(row=0, column=1, padx=10, pady=10)

        # Number of Operators
        self.operator_count_label = ctk.CTkLabel(
            self.settings_frame,
            text="Operators per Question:"
        )
        self.operator_count_label.grid(row=1, column=0, padx=10, pady=10)

        self.operator_count_menu = ctk.CTkOptionMenu(
            self.settings_frame,
            values=["1", "2", "3", "4"]
        )
        self.operator_count_menu.grid(row=1, column=1, padx=10, pady=10)

        # -----------------------------
        # Operators
        # -----------------------------
        self.operators_label = ctk.CTkLabel(
            self.settings_frame,
            text="Choose Operators:"
        )
        self.operators_label.grid(row=2, column=0, padx=10, pady=10)

        self.plus_var = ctk.BooleanVar(value=True)
        self.minus_var = ctk.BooleanVar(value=False)
        self.multiply_var = ctk.BooleanVar(value=False)
        self.divide_var = ctk.BooleanVar(value=False)

        self.plus_check = ctk.CTkCheckBox(
            self.settings_frame,
            text="+",
            variable=self.plus_var
        )
        self.plus_check.grid(row=2, column=1, sticky="w")

        self.minus_check = ctk.CTkCheckBox(
            self.settings_frame,
            text="-",
            variable=self.minus_var
        )
        self.minus_check.grid(row=2, column=2, sticky="w")

        self.multiply_check = ctk.CTkCheckBox(
            self.settings_frame,
            text="*",
            variable=self.multiply_var
        )
        self.multiply_check.grid(row=2, column=3, sticky="w")

        self.divide_check = ctk.CTkCheckBox(
            self.settings_frame,
            text="/",
            variable=self.divide_var
        )
        self.divide_check.grid(row=2, column=4, sticky="w")

        # -----------------------------
        # Question Display
        # -----------------------------
        self.question_label = ctk.CTkLabel(
            self,
            text="Press 'New Question'",
            font=("Arial", 22)
        )
        self.question_label.pack(pady=30)

        # -----------------------------
        # Answer Entry
        # -----------------------------
        self.answer_entry = ctk.CTkEntry(
            self,
            width=200,
            font=("Arial", 20)
        )
        self.answer_entry.pack(pady=10)

        # -----------------------------
        # Buttons
        # -----------------------------
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=20)

        self.new_question_button = ctk.CTkButton(
            self.button_frame,
            text="New Question",
            command=self.new_question
        )
        self.new_question_button.grid(row=0, column=0, padx=10)

        self.submit_button = ctk.CTkButton(
            self.button_frame,
            text="Submit Answer",
            command=self.check_answer
        )
        self.submit_button.grid(row=0, column=1, padx=10)

        # -----------------------------
        # Score Label
        # -----------------------------
        self.score_label = ctk.CTkLabel(
            self,
            text="Score: 0 / 0",
            font=("Arial", 20, "bold")
        )
        self.score_label.pack(pady=20)

    # -----------------------------
    # Create New Question
    # -----------------------------
    def new_question(self):

        selected_ops = []

        if self.plus_var.get():
            selected_ops.append("+")

        if self.minus_var.get():
            selected_ops.append("-")

        if self.multiply_var.get():
            selected_ops.append("*")

        if self.divide_var.get():
            selected_ops.append("/")

        if not selected_ops:
            messagebox.showwarning(
                "No Operators",
                "Please select at least one operator."
            )
            return

        max_result_text = self.max_result_entry.get()

        max_result = (
            int(max_result_text)
            if max_result_text.strip()
            else None
        )

        num_operators = int(self.operator_count_menu.get())

        expression, answer = generate_expression(
            max_result=max_result,
            num_operators=num_operators,
            allowed_ops=selected_ops
        )

        self.current_answer = answer

        self.question_label.configure(text=expression)

        self.answer_entry.delete(0, "end")

    # -----------------------------
    # Check User Answer
    # -----------------------------
    def check_answer(self):

        if self.current_answer is None:
            messagebox.showinfo(
                "No Question",
                "Please generate a question first."
            )
            return

        user_input = self.answer_entry.get()

        try:
            user_answer = int(user_input)

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid number."
            )
            return

        self.total_questions += 1

        if user_answer == self.current_answer:
            self.score += 1

            messagebox.showinfo(
                "Correct",
                "✅ Correct Answer!"
            )

        else:
            messagebox.showerror(
                "Wrong",
                f"❌ Wrong!\nCorrect answer was: {self.current_answer}"
            )

        self.score_label.configure(
            text=f"Score: {self.score} / {self.total_questions}"
        )

        self.current_answer = None


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app = MathPracticeApp()
    app.mainloop()