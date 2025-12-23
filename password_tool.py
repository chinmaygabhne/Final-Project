import zxcvbn
import argparse
import tkinter as tk
from tkinter import messagebox

def analyze_password(password):
    
    results = zxcvbn.zxcvbn(password)
    score = results['score']  
    crack_time = results['crack_times_display']['offline_slow_hashing_1e4_per_second']
    
    output = f"\n--- Password Analysis ---\nPassword: {password}\nStrength Score: {score}/4\nEstimated Crack Time: {crack_time}\n"
    
    if results['feedback']['suggestions']:
        output += "Suggestions: " + ", ".join(results['feedback']['suggestions']) + "\n"
    output += "--------------------------\n"
    
    return output

def generate_wordlist(user_data, output_file):
    
    base_words = user_data.split(',')
    years = ['2023', '2024', '2025', '123', '!']
    leetspeak = {'a': '@', 's': '$', 'e': '3', 'i': '1', 'o': '0'}
    
    wordlist = []
    for word in base_words:
        word = word.strip()
        wordlist.append(word)
        
        
        for year in years:
            wordlist.append(f"{word}{year}")
            
        
        leet_word = word
        for char, replacement in leetspeak.items():
            leet_word = leet_word.lower().replace(char, replacement)
        wordlist.append(leet_word)

    
    with open(output_file, 'w') as f:
        for item in set(wordlist): 
            f.write(f"{item}\n")
    return f"Success! Custom wordlist saved to {output_file}"

def gui():
    app = PasswordToolGUI()
    app.run()

class PasswordToolGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cybersecurity Password Tool")

        
        tk.Label(self.root, text="Password Analysis").pack(pady=10)
        tk.Label(self.root, text="Enter Password:").pack()
        self.analyze_entry = tk.Entry(self.root, width=50)
        self.analyze_entry.pack()
        analyze_button = tk.Button(self.root, text="Analyze Password", command=self.analyze_gui)
        analyze_button.pack(pady=5)
        self.analyze_result = tk.Text(self.root, height=10, width=60)
        self.analyze_result.pack()

        
        tk.Label(self.root, text="Wordlist Generation").pack(pady=10)
        tk.Label(self.root, text="User Data (comma separated):").pack()
        self.generate_entry = tk.Entry(self.root, width=50)
        self.generate_entry.pack()
        tk.Label(self.root, text="Output File:").pack()
        self.out_entry = tk.Entry(self.root, width=50)
        self.out_entry.insert(0, "wordlist.txt")
        self.out_entry.pack()
        generate_button = tk.Button(self.root, text="Generate Wordlist", command=self.generate_gui)
        generate_button.pack(pady=5)

    def run(self):
        self.root.mainloop()

    def analyze_gui(self):
        password = self.analyze_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password to analyze.")
            return
        result = analyze_password(password)
        self.analyze_result.delete(1.0, tk.END)
        self.analyze_result.insert(tk.END, result)

    def generate_gui(self):
        user_data = self.generate_entry.get()
        output_file = self.out_entry.get()
        if not user_data:
            messagebox.showerror("Error", "Please enter user data.")
            return
        try:
            message = generate_wordlist(user_data, output_file)
            messagebox.showinfo("Success", message)
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    
    parser = argparse.ArgumentParser(description="Cybersecurity Password Tool")
    parser.add_argument("--analyze", help="Analyze a specific password")
    parser.add_argument("--generate", help="Input keywords separated by commas (e.g. name,pet,year)")
    parser.add_argument("--out", help="Output filename for wordlist", default="wordlist.txt")
    
    args = parser.parse_args()

    if args.analyze:
        print(analyze_password(args.analyze))
    elif args.generate:
        print(generate_wordlist(args.generate, args.out))
    else:
        gui()

if __name__ == "__main__":
    main()
