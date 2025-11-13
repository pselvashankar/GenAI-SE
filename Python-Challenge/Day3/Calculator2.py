import tkinter as tk
from tkinter import ttk, messagebox

class ArithmeticCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Arithmetic Calculator")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        
        # Configure colors
        self.success_color = "#2E8B57"  # Sea Green
        self.error_color = "#DC143C"    # Crimson
        self.normal_color = "#000080"   # Navy Blue
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🧮 Basic Arithmetic Calculator", 
                               font=('Arial', 18, 'bold'), foreground='#2C3E50')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 25))
        
        # Input Frame
        input_frame = ttk.LabelFrame(main_frame, text=" Input Values ", padding="15")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # First number
        ttk.Label(input_frame, text="First Number:", font=('Arial', 12)).grid(row=0, column=0, sticky=tk.W, pady=8)
        self.num1_entry = ttk.Entry(input_frame, font=('Arial', 14), width=20, justify='center')
        self.num1_entry.grid(row=0, column=1, pady=8, padx=(15, 0))
        self.num1_entry.focus()
        
        # Operation selection
        ttk.Label(input_frame, text="Operation:", font=('Arial', 12)).grid(row=1, column=0, sticky=tk.W, pady=8)
        self.operation_var = tk.StringVar()
        self.operation_combo = ttk.Combobox(input_frame, textvariable=self.operation_var,
                                           state="readonly", width=17, font=('Arial', 12))
        self.operation_combo['values'] = ('Addition (+)', 'Subtraction (-)', 
                                         'Multiplication (×)', 'Division (÷)')
        self.operation_combo.current(0)
        self.operation_combo.grid(row=1, column=1, pady=8, padx=(15, 0))
        
        # Second number
        ttk.Label(input_frame, text="Second Number:", font=('Arial', 12)).grid(row=2, column=0, sticky=tk.W, pady=8)
        self.num2_entry = ttk.Entry(input_frame, font=('Arial', 14), width=20, justify='center')
        self.num2_entry.grid(row=2, column=1, pady=8, padx=(15, 0))
        
        # Buttons Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Calculate button
        calc_button = ttk.Button(button_frame, text="🚀 Calculate", command=self.calculate, width=15)
        calc_button.grid(row=0, column=0, padx=10)
        
        # Clear button
        clear_button = ttk.Button(button_frame, text="🗑️ Clear All", command=self.clear_fields, width=15)
        clear_button.grid(row=0, column=1, padx=10)
        
        # Result Frame
        result_frame = ttk.LabelFrame(main_frame, text=" Calculation Result ", padding="20")
        result_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        # Result display with better formatting
        self.result_var = tk.StringVar(value="Waiting for calculation...")
        self.result_label = ttk.Label(result_frame, textvariable=self.result_var, 
                                     font=('Arial', 16, 'bold'), 
                                     foreground=self.normal_color,
                                     justify='center',
                                     wraplength=350)
        self.result_label.pack()
        
        # Detailed result
        self.detailed_var = tk.StringVar()
        self.detailed_label = ttk.Label(result_frame, textvariable=self.detailed_var,
                                       font=('Arial', 12),
                                       foreground='#666666',
                                       justify='center',
                                       wraplength=350)
        self.detailed_label.pack()
        
        # Bind Enter key to calculate
        self.root.bind('<Return>', lambda event: self.calculate())
        
        # Bind tab key for navigation
        self.num1_entry.bind('<Tab>', self.focus_next_widget)
        self.operation_combo.bind('<Tab>', self.focus_next_widget)
    
    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"
    
    def calculate(self):
        try:
            # Get input values
            num1_str = self.num1_entry.get().strip()
            num2_str = self.num2_entry.get().strip()
            operation = self.operation_var.get()
            
            # Validate inputs
            if not num1_str or not num2_str:
                self.show_error("❌ Please enter both numbers")
                return
            
            # Convert to float
            num1 = float(num1_str)
            num2 = float(num2_str)
            
            # Perform calculation based on selected operation
            operation_symbols = {
                'Addition (+)': ('+', '+'),
                'Subtraction (-)': ('-', '-'),
                'Multiplication (×)': ('×', '*'),
                'Division (÷)': ('÷', '/')
            }
            
            if operation in operation_symbols:
                display_symbol, calc_symbol = operation_symbols[operation]
                
                if calc_symbol == '+':
                    result = num1 + num2
                elif calc_symbol == '-':
                    result = num1 - num2
                elif calc_symbol == '*':
                    result = num1 * num2
                elif calc_symbol == '/':
                    if num2 == 0:
                        self.show_error("❌ Division by zero is not allowed!")
                        return
                    result = num1 / num2
                
                # Display results clearly
                self.show_success(num1, display_symbol, num2, result)
                
            else:
                self.show_error("❌ Please select a valid operation")
            
        except ValueError:
            self.show_error("❌ Please enter valid numbers (e.g., 4.5, -3, 100)")
        except Exception as e:
            self.show_error(f"❌ An unexpected error occurred: {str(e)}")
    
    def show_success(self, num1, symbol, num2, result):
        """Display successful calculation with clear formatting"""
        # Main result
        result_text = f"🎯 Result: {result}"
        self.result_var.set(result_text)
        self.result_label.configure(foreground=self.success_color, font=('Arial', 16, 'bold'))
        
        # Detailed calculation
        detailed_text = f"📝 Calculation: {num1} {symbol} {num2} = {result}"
        
        # Add formatting for large numbers
        if abs(result) >= 1000000 or (abs(result) < 0.001 and result != 0):
            detailed_text += f"\n📊 Scientific Notation: {result:.2e}"
        
        self.detailed_var.set(detailed_text)
        
        # Show success message
        messagebox.showinfo("Calculation Complete", 
                          f"Calculation successful!\n\n{num1} {symbol} {num2} = {result}")
    
    def show_error(self, message):
        """Display error message with clear formatting"""
        self.result_var.set(message)
        self.result_label.configure(foreground=self.error_color, font=('Arial', 14, 'bold'))
        self.detailed_var.set("Please check your input and try again.")
    
    def clear_fields(self):
        """Clear all input fields and reset result display"""
        self.num1_entry.delete(0, tk.END)
        self.num2_entry.delete(0, tk.END)
        self.operation_combo.current(0)
        self.result_var.set("Waiting for calculation...")
        self.detailed_var.set("")
        self.result_label.configure(foreground=self.normal_color, font=('Arial', 16, 'bold'))
        self.num1_entry.focus()

def main():
    root = tk.Tk()
    app = ArithmeticCalculator(root)
    
    # Center the window on screen
    root.eval('tk::PlaceWindow . center')
    
    root.mainloop()

if __name__ == "__main__":
    main()