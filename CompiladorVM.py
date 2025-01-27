import tkinter as tk
from tkinter import filedialog, messagebox
from Principal import Lexical, TabelaSimbolos
import os
import sys
from io import StringIO


class Compilador:
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador Freitas")
        self.root.geometry("800x700")

       
        self.create_menu()

        
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(fill="both", expand=True)

      
        self.line_numbers = tk.Text(
            self.text_frame, width=4, padx=3, takefocus=0, border=0, background="#f0f0f0", state="disabled"
        )
        self.line_numbers.pack(side="left", fill="y")

        self.text_area = tk.Text(self.text_frame, wrap="none", undo=True)
        self.text_area.pack(side="right", fill="both", expand=True)

        self.text_area.bind("<KeyRelease>", self.update_line_numbers)
        self.text_area.bind("<MouseWheel>", self.update_line_numbers)
        self.text_area.bind("<ButtonRelease>", self.update_line_numbers)

        self.message_area_frame = tk.Frame(self.root)
        self.message_area = tk.Text(
            self.message_area_frame, bg="#f0f0f0", relief="sunken", height=8
        )
        self.message_area.pack(fill="both", expand=True)
        self.message_area_frame.pack(fill="x")

        self.reset_compiler_state()

        self.update_line_numbers()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Arquivo", menu=file_menu)

        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)

        compile_menu = tk.Menu(menu, tearoff=0)
        menu.add_command(label="Compilar", command=self.compile_code)
        

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                    self.update_line_numbers()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir o arquivo: {e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, "w") as file:
                    content = self.get_assembly_output()
                    file.write(content)
                    messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")

    def compile_code(self):
        code = self.text_area.get(1.0, tk.END).strip()
        if not code:
            self.update_message_area("Nenhum código para compilar.\n")
            return

        temp_file = "temp.txt"
        with open(temp_file, "w") as file:
            file.write(code)

        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        try:
            self.lexer = Lexical(temp_file)

            from main import main as compile_main
            compile_main()

            output = sys.stdout.getvalue()
            self.update_message_area(output)
        except Exception as e:
            error_output = sys.stderr.getvalue()
            self.update_message_area(f"Erro: {str(e)}\n{error_output}")
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            if os.path.exists(temp_file):
                os.remove(temp_file)

    def update_line_numbers(self, event=None):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete(1.0, tk.END)

        line_count = int(self.text_area.index("end-1c").split(".")[0])
        for line in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, f"{line}\n")

        self.line_numbers.config(state="disabled")

    def reset_compiler_state(self):
        self.lexer = None
        self.symbol_table = TabelaSimbolos()

    def update_message_area(self, message):
        self.message_area.delete(1.0, tk.END)
        self.message_area.insert(tk.END, message)

    def get_assembly_output(self):
        assembly_file = "gera2.obj"
        if os.path.exists(assembly_file):
            with open(assembly_file, "r") as file:
                return file.read()
        return "Nenhum código assembly gerado."
    

if __name__ == "__main__":
    root = tk.Tk()
    app = Compilador(root)
    root.mainloop()
