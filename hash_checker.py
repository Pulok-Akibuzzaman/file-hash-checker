import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class HashCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Hash Checker")
        self.root.geometry("650x360")
        self.root.resizable(False, False)

        self.selected_file = tk.StringVar()
        self.selected_hash = tk.StringVar()
        self.expected_hash = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="File:").grid(
            row=0, column=0, sticky="w", pady=8
        )

        ttk.Entry(
            main,
            textvariable=self.selected_file,
            width=65,
            state="readonly"
        ).grid(row=0, column=1, padx=8, pady=8)

        ttk.Button(
            main,
            text="Browse",
            command=self.choose_file
        ).grid(row=0, column=2, pady=8)

        ttk.Label(main, text="Hash algorithm:").grid(
            row=1, column=0, sticky="w", pady=8
        )

        algorithm_box = ttk.Combobox(
            main,
            textvariable=self.selected_hash,
            values=["md5", "sha1", "sha256", "sha512"],
            state="readonly",
            width=15
        )
        algorithm_box.grid(row=1, column=1, sticky="w", padx=8, pady=8)
        algorithm_box.set("sha256")

        ttk.Button(
            main,
            text="Calculate Hash",
            command=self.calculate_hash
        ).grid(row=2, column=1, sticky="w", padx=8, pady=12)

        ttk.Label(main, text="Calculated hash:").grid(
            row=3, column=0, sticky="w", pady=8
        )

        self.calculated_hash_entry = ttk.Entry(
            main,
            width=65,
            state="readonly"
        )
        self.calculated_hash_entry.grid(
            row=3, column=1, padx=8, pady=8
        )

        ttk.Button(
            main,
            text="Copy",
            command=self.copy_hash
        ).grid(row=3, column=2, pady=8)

        ttk.Label(main, text="Expected hash:").grid(
            row=4, column=0, sticky="w", pady=8
        )

        ttk.Entry(
            main,
            textvariable=self.expected_hash,
            width=65
        ).grid(row=4, column=1, padx=8, pady=8)

        ttk.Button(
            main,
            text="Verify",
            command=self.verify_hash
        ).grid(row=5, column=1, sticky="w", padx=8, pady=12)

        self.status_label = ttk.Label(
            main,
            text="Select a file to begin.",
            foreground="gray"
        )
        self.status_label.grid(
            row=6, column=0, columnspan=3, pady=20
        )

    def choose_file(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            self.selected_file.set(file_path)
            self.clear_calculated_hash()
            self.status_label.config(
                text="File selected. Click Calculate Hash.",
                foreground="gray"
            )

    def calculate_hash(self):
        file_path = self.selected_file.get()
        algorithm = self.selected_hash.get()

        if not file_path:
            messagebox.showwarning(
                "No file selected",
                "Please select a file first."
            )
            return

        try:
            hash_function = hashlib.new(algorithm)

            with open(file_path, "rb") as file:
                while chunk := file.read(1024 * 1024):
                    hash_function.update(chunk)

            calculated_hash = hash_function.hexdigest()

            self.calculated_hash_entry.config(state="normal")
            self.calculated_hash_entry.delete(0, tk.END)
            self.calculated_hash_entry.insert(0, calculated_hash)
            self.calculated_hash_entry.config(state="readonly")

            self.status_label.config(
                text="Hash calculated successfully.",
                foreground="green"
            )

        except OSError as error:
            messagebox.showerror(
                "File error",
                f"Could not read the file:\n{error}"
            )

    def copy_hash(self):
        calculated_hash = self.get_calculated_hash()

        if not calculated_hash:
            messagebox.showwarning(
                "No hash available",
                "Calculate a hash first."
            )
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(calculated_hash)
        self.status_label.config(
            text="Hash copied to clipboard.",
            foreground="green"
        )

    def verify_hash(self):
        calculated_hash = self.get_calculated_hash()
        expected_hash = self.expected_hash.get().strip().lower()

        if not calculated_hash:
            messagebox.showwarning(
                "No calculated hash",
                "Calculate the file hash first."
            )
            return

        if not expected_hash:
            messagebox.showwarning(
                "No expected hash",
                "Enter an expected hash first."
            )
            return

        if calculated_hash.lower() == expected_hash:
            self.status_label.config(
                text="MATCH: The hashes are identical.",
                foreground="green"
            )
        else:
            self.status_label.config(
                text="NO MATCH: The hashes are different.",
                foreground="red"
            )

    def get_calculated_hash(self):
        return self.calculated_hash_entry.get().strip()

    def clear_calculated_hash(self):
        self.calculated_hash_entry.config(state="normal")
        self.calculated_hash_entry.delete(0, tk.END)
        self.calculated_hash_entry.config(state="readonly")


if __name__ == "__main__":
    root = tk.Tk()
    app = HashCheckerApp(root)
    root.mainloop()