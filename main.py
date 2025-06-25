import tkinter as tk
import pyperclip
from bs4 import BeautifulSoup


class LocatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Locator Generator")
        self.root.geometry("800x240")  # Set default window size

        self.label = tk.Label(root, text="Clipboard HTML Locators:")
        self.label.pack()

        self.canvas = tk.Canvas(root)
        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas)

        self.scroll_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        self.pause_button = tk.Button(root, text="Pause", command=self.toggle_pause)
        self.pause_button.pack()

        self.is_paused = False

        self.priority_attributes = ["for", "data-test-id", "data-testid", "id", "name", "title", "aria-label",
                                    "placeholder", "value", "data-cy", "class"]

        self.recent_clipboard = ""
        self.poll_clipboard()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_button.config(text="Resume" if self.is_paused else "Pause")

    def poll_clipboard(self):
        if not self.is_paused:
            html = pyperclip.paste()
            if html and html != self.recent_clipboard and self.is_valid_html(html):
                self.recent_clipboard = html
                self.generate_locators(html)
        self.root.after(100, self.poll_clipboard)

    def is_valid_html(self, html):
        return html.strip().startswith("<") and html.strip().endswith(">") and '"' in html

    def generate_locators(self, html):
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.find(True)
        if not tag:
            return

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        tag_name = tag.name
        attributes = tag.attrs

        main_locator = None
        locators = []
        extra_locators = []

        used_attrs = set()

        for attr in self.priority_attributes:
            if attr in attributes:
                used_attrs.add(attr)
                value = attributes[attr]
                if isinstance(value, list):
                    value = " ".join(value)

                if attr == "id":
                    if "." in value:
                        locator = f'page.locator("{tag_name}[id={repr(value)}]")'
                    else:
                        locator = f'page.locator("{tag_name}#{value}")'
                elif attr == "class":
                    locator = f'page.locator("{tag_name}.' + ".".join(value.split()) + '")'
                else:
                    locator = f'page.locator("{tag_name}[{attr}={repr(value)}]")'

                if not main_locator:
                    main_locator = locator
                else:
                    extra_locators.append(locator)

        remaining_attrs = [attr for attr in attributes if attr not in used_attrs]

        for attr in remaining_attrs:
            value = attributes[attr]
            if isinstance(value, list):
                value = " ".join(value)
            if value == "":
                locator = f'page.locator("{tag_name}[{attr}]")'
            else:
                locator = f'page.locator("{tag_name}[{attr}={repr(value)}]")'
            extra_locators.append(locator)

        if not attributes:
            main_locator = f'page.locator("{tag_name}")'
            locators.append(main_locator)

        locators.append(main_locator)
        locators.extend(extra_locators)

        if main_locator:
            pyperclip.copy(main_locator)
            self.add_locator_to_ui(main_locator, copied=True)

        for locator in locators:
            if locator != main_locator:
                self.add_locator_to_ui(locator)

    def add_locator_to_ui(self, locator, copied=False):
        frame = tk.Frame(self.scroll_frame)
        frame.pack(fill=tk.X, padx=5, pady=2, anchor="w")

        label_text = locator + ("  (Copied)" if copied else "")
        label = tk.Label(frame, text=label_text, anchor="w", justify="left", wraplength=600)
        label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        copy_button = tk.Button(frame, text="Copy", command=lambda: self.copy_to_clipboard(locator))
        copy_button.pack(side=tk.RIGHT)

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)


if __name__ == "__main__":
    root = tk.Tk()
    app = LocatorGUI(root)
    root.mainloop()
