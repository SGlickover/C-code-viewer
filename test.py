import tkinter as tk
import re

def show_line_content(line):
    line_content_label.config(text=line, font=("Arial", 14), bg="lightblue", relief="solid")
    create_word_buttons(line)
    find_and_display_cpp_functions(line)

def toggle_minimized_code():
    if content_label.winfo_ismapped():
        content_label.grid_forget()
        maximize_button.config(text="See the Original Code")
    else:
        content_label.grid(row=0, column=1, rowspan=len(lines), sticky="ne", padx=10, pady=10)
        maximize_button.config(text="Minimize the Code")

def search_for_word(word):
    results = []
    for i, line in enumerate(lines):
        if word.lower() in line.lower():
            results.append(i)
    return results

def highlight_line(line_number):
    for button in line_buttons:
        button.config(relief="solid")
    line_buttons[line_number].config(relief="groove")
    clear_word_buttons()

def create_word_buttons(line):
    clear_word_buttons()
    line_words = line.strip().split()
    for j, word in enumerate(line_words):
        if not any(char.isalnum() for char in word):
            continue  # Skip special characters
        word_button = tk.Button(window, text=word, command=lambda word=word: search_and_show_results(word), bg="lightgreen", fg="black", relief="raised")
        word_button.grid(row=i, column=j+1, sticky="w", padx=2, pady=2)
        word_buttons.append(word_button)

def clear_word_buttons():
    for button in word_buttons:
        button.destroy()
    word_buttons.clear()

def search_and_show_results(word):
    clear_results_labels()
    results = search_for_word(word)
    for result in results:
        result_label = tk.Label(window, text=lines[result], font=("Arial", 12), bg="lightyellow", relief="solid")
        result_label.grid(row=result, column=2, sticky="w", padx=5, pady=2)
        result_labels.append(result_label)

def clear_results_labels():
    for label in result_labels:
        label.destroy()
    result_labels.clear()

def find_and_display_cpp_functions(line):
    functions = find_deployed_functions(line)
    if functions:
        function_label = tk.Label(window, text="Functions: ".join(functions), justify="left", font=("Arial", 12), bg="white", relief="solid", fg="red")
        function_label.grid(row=len(lines)+1, columnspan=3, sticky="w", padx=5, pady=2)

def find_deployed_functions(line):
    functions = []
    pattern = r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)"
    matches = re.findall(pattern, line)
    for match in matches:
        function_name = match[0]
        arguments = match[1]
        functions.append(function_name + "(" + arguments + ")")
    return functions

window = tk.Tk()
window.title("Code Viewer")
window.configure(bg="#E0B0FF")

with open("hello.txt", "r") as file:
    lines = file.readlines()

line_buttons = []
for i, line in enumerate(lines):
    line = line.strip()
    line_button = tk.Button(window, text=str(i+1), command=lambda line=line: show_line_content(line), bg="lightblue", fg="black", relief="raised")
    line_button.grid(row=i, column=0, sticky="w", padx=5, pady=5)
    line_buttons.append(line_button)
    line_label = tk.Label(window, text=line, font=("Arial", 12), bg="white")
    line_label.grid(row=i, column=1, sticky="w", padx=5, pady=5)

line_content_label = tk.Label(window, text="", font=("Arial", 12), bg="white", relief="solid")
line_content_label.grid(row=len(lines), columnspan=3, sticky="w", padx=5, pady=5)

content_label = tk.Label(window, text="\n".join(lines), font=("Arial", 12), bg="white", relief="solid")
content_label.grid(row=0, column=2, rowspan=len(lines), sticky="ne", padx=10, pady=10)

maximize_button = tk.Button(window, text="Minimize the Code", command=toggle_minimized_code, bg="lightblue", fg="black", relief="raised")
maximize_button.grid(row=0, column=3, sticky="ne", padx=5, pady=5)

word_buttons = []
result_labels = []

window.mainloop()