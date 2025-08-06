import tkinter as tk
import tkinter.font as tkFont

# --- Main Application Class ---
class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("350x500")
        self.configure(bg="#1E1E1E")
        self.resizable(False, False)

        self.expression = ""
        self.display_var = tk.StringVar()

        self._create_widgets()

    def _create_widgets(self):
        # --- Display Screen ---
        display_font = tkFont.Font(family="Helvetica", size=28)
        display_frame = tk.Frame(self, bg="#1E1E1E")
        display_frame.pack(expand=True, fill="both")

        display_label = tk.Label(
            display_frame, 
            textvariable=self.display_var, 
            font=display_font, 
            anchor="se", 
            bg="#1E1E1E", 
            fg="#FFFFFF",
            padx=10, 
            pady=10
        )
        display_label.pack(expand=True, fill="both")

        # --- Buttons Frame ---
        buttons_frame = tk.Frame(self, bg="#1E1E1E")
        buttons_frame.pack(expand=True, fill="both")

        # --- Button Layout ---
        buttons = [
            ('C', 1, 0), ('⌫', 1, 1), ('%', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 2), ('.', 5, 2), ('=', 5, 3)
        ]

        for i in range(6):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)

        for (text, row, col, *span) in buttons:
            self._create_button(text, row, col, span[0] if span else 1, buttons_frame)

    def _create_button(self, text, row, col, span, frame):
        btn_font = tkFont.Font(family="Helvetica", size=16)
        btn_props = {
            'font': btn_font,
            'bd': 0,
            'fg': '#FFFFFF',
            'activeforeground': '#FFFFFF',
            'highlightthickness': 0
        }

        if text in '0123456789.':
            btn_props['bg'] = '#3B3B3B'
            btn_props['activebackground'] = '#555555'
        elif text in '+-*/%':
            btn_props['bg'] = '#FF8C00' # Operator color
            btn_props['activebackground'] = '#FFA500'
        elif text == '=':
            btn_props['bg'] = '#FF4500' # Equals color
            btn_props['activebackground'] = '#FF6347'
        else:
            btn_props['bg'] = '#A9A9A9' # Other controls
            btn_props['activebackground'] = '#C0C0C0'

        button = tk.Button(frame, text=text, **btn_props, command=lambda t=text: self._on_click(t))
        button.grid(row=row, column=col, columnspan=span, sticky="nsew", padx=2, pady=2)

    def _on_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '⌫':
            self.expression = self.expression[:-1]
        elif char == '%':
            self._handle_percentage()
        elif char == '=':
            try:
                result = str(eval(self.expression))
                self.expression = result
            except (SyntaxError, ZeroDivisionError):
                self.expression = "Error"
            except Exception:
                self.expression = "Error"
        else:
            if self.expression == "Error":
                self.expression = ""
            self.expression += str(char)
        
        self.display_var.set(self.expression)

    def _handle_percentage(self):
        if not self.expression or self.expression == "Error":
            return

        try:
            # Find the last number in the expression
            last_op_index = -1
            for op in ['+', '-', '*', '/']:
                last_op_index = max(last_op_index, self.expression.rfind(op))

            if last_op_index == -1:
                # No operator, just a number (e.g., "50%")
                num = float(self.expression)
                self.expression = str(num / 100)
            else:
                # Expression with an operator (e.g., "100+50%")
                base_expr = self.expression[:last_op_index+1]
                last_num_str = self.expression[last_op_index+1:]
                
                # If there's no number after the operator, do nothing
                if not last_num_str:
                    return

                last_num = float(last_num_str)
                
                # For + and -, percentage is of the preceding result
                if self.expression[last_op_index] in ['+', '-']:
                    # Evaluate the base part of the expression
                    base_value = eval(self.expression[:last_op_index])
                    percentage = base_value * (last_num / 100)
                    self.expression = f"{base_expr}{percentage}"
                # For * and /, percentage is a simple division by 100
                else:
                    percentage = last_num / 100
                    self.expression = f"{base_expr}{percentage}"

        except Exception:
            self.expression = "Error"

# --- Run the Application ---
if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
