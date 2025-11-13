import tkinter as tk
from tkinter import ttk, messagebox

class ArithmeticCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Arithmetic Calculator")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12))
        self.style.configure('TCombobox', font=('Arial', 12))
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Basic Arithmetic Calculator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # First number
        ttk.Label(main_frame, text="First Number:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.num1_entry = ttk.Entry(main_frame, font=('Arial', 12), width=15)
        self.num1_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Operation selection
        ttk.Label(main_frame, text="Operation:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.operation_var = tk.StringVar()
        self.operation_combo = ttk.Combobox(main_frame, textvariable=self.operation_var,
                                           state="readonly", width=13)
        self.operation_combo['values'] = ('Addition (+)', 'Subtraction (-)', 
                                         'Multiplication (*)', 'Division (/)')
        self.operation_combo.current(0)  # Set default to Addition
        self.operation_combo.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Second number
        ttk.Label(main_frame, text="Second Number:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.num2_entry = ttk.Entry(main_frame, font=('Arial', 12), width=15)
        self.num2_entry.grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Calculate button
        calc_button = ttk.Button(main_frame, text="Calculate", command=self.calculate)
        calc_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Result frame
        result_frame = ttk.LabelFrame(main_frame, text="Result", padding="10")
        result_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.result_var = tk.StringVar(value="Result will be displayed here")
        result_label = ttk.Label(result_frame, textvariable=self.result_var, 
                                font=('Arial', 12, 'bold'), foreground='blue')
        result_label.pack()
        
        # Clear button
        clear_button = ttk.Button(main_frame, text="Clear", command=self.clear_fields)
        clear_button.grid(row=6, column=0, columnspan=2, pady=10)
    
    def calculate(self):
        try:
            # Get input values
            num1_str = self.num1_entry.get().strip()
            num2_str = self.num2_entry.get().strip()
            operation = self.operation_var.get()
            
            # Validate inputs
            if not num1_str or not num2_str:
                messagebox.showerror("Input Error", "Please enter both numbers")
                return
            
            # Convert to float
            num1 = float(num1_str)
            num2 = float(num2_str)
            
            # Perform calculation based on selected operation
            if operation == 'Addition (+)':
                result = num1 + num2
                symbol = '+'
            elif operation == 'Subtraction (-)':
                result = num1 - num2
                symbol = '-'
            elif operation == 'Multiplication (*)':
                result = num1 * num2
                symbol = '*'
            elif operation == 'Division (/)':
                if num2 == 0:
                    messagebox.showerror("Math Error", "Division by zero is not allowed")
                    return
                result = num1 / num2
                symbol = '/'
            else:
                messagebox.showerror("Operation Error", "Please select a valid operation")
                return
            
            # Display result
            self.result_var.set(f"{num1} {symbol} {num2} = {result}")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def clear_fields(self):
        self.num1_entry.delete(0, tk.END)
        self.num2_entry.delete(0, tk.END)
        self.operation_combo.current(0)
        self.result_var.set("Result will be displayed here")

def main():
    root = tk.Tk()
    app = ArithmeticCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()