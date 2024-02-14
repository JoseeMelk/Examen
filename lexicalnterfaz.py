import tkinter as tk
from tkinter import scrolledtext
from tabulate import tabulate
from lexicalAnalicer import AnalizadorLexico

class LexicalInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Analizador Lexico - José Melquiades Castellanos Morales 6'M'")
        self.window.geometry("800x600")
        
        self.text_entry = scrolledtext.ScrolledText(self.window, width=40, height=10)
        self.text_entry.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.analyze_button = tk.Button(self.window, text="Analizar", command=self.analyze)
        self.analyze_button.pack(pady=5)
        
        self.result_display = scrolledtext.ScrolledText(self.window, width=40, height=10, state='disabled')
        self.result_display.pack(expand=True, fill='both', padx=10, pady=10)

        self.analyzer = AnalizadorLexico()
    
    def analyze(self):
        self.analyzer.delete()
        input_text = self.text_entry.get("1.0", tk.END)
        
        self.analyzer.analyzer(input_text)
        result_data = self.analyzer.states_list
        tables = ''
        table = []
            
        headers = ["TOKEN", "PALABRA_R", "IDENTIFICADOR", "OPERADOR", "NUMERO", "SIMBOLO"]
        
        x = 'x'
        vacio = ''
        
        for data in result_data:
            if data.get('token') == 'PALABRA_R':  
                tables = [data.get('lexema'), x, vacio, vacio, vacio, vacio]
                table.append(tables)
            if data.get('token') == 'IDENTIFICADOR':  
                tables = [data.get('lexema'), vacio, x, vacio, vacio, vacio]
                table.append(tables)
            if data.get('token') == 'OPERADOR':  
                tables = [data.get('lexema'), vacio, vacio, x, vacio, vacio]
                table.append(tables)
            if data.get('token') == 'NUMERO':  
                tables = [data.get('lexema'), vacio, vacio, vacio, x, vacio]
                table.append(tables)
            if data.get('token') == 'SIMBOLO':  
                tables = [data.get('lexema'), vacio, vacio, vacio, vacio, x]
                table.append(tables)
            
          
        #table = [[item['token'], item['lexema'], item['linea']] for item in result_data]
        table_str = tabulate(table, headers=headers, tablefmt="pipe")
            
        self.result_display.config(state='normal')
        # Elimina el contenido de la salida
        self.result_display.delete("1.0", tk.END)
            
        # Inserta la tabla formateada en el widget de resultado
        self.result_display.insert(tk.END, table_str)
        self.result_display.config(state='disabled')
        
# Create the main window
main_window = tk.Tk()
interface = LexicalInterface(main_window)
main_window.mainloop()