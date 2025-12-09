import tkinter as tk
from tkinter import messagebox

# -----------------------------
# CLASS: Menu Item
# -----------------------------
class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = float(price)

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"


# -----------------------------
# CLASS: Order
# -----------------------------
class Order:
    def __init__(self):
        self.items = []

    def add_item(self, menu_item):
        self.items.append(menu_item)

    def calculate_total(self):
        return sum(item.price for item in self.items)


# -----------------------------
# CLASS: Coffee Shop System
# -----------------------------
class CoffeeShopSystem:
    def __init__(self):
        self.menu = []
        self.current_order = Order()

    def add_menu_item(self, name, price):
        self.menu.append(MenuItem(name, price))

    def delete_menu_item(self, name):
        for item in self.menu:
            if item.name == name:
                self.menu.remove(item)
                return True
        return False


# -----------------------------
# GUI Application
# -----------------------------
class CoffeeShopGUI:
    def __init__(self, root):
        self.system = CoffeeShopSystem()
        self.root = root
        self.root.title("Sunrise Coffee Shop System")

        # Menu Frame
        menu_frame = tk.LabelFrame(root, text="Menu Management", padx=10, pady=10)
        menu_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(menu_frame, text="Item Name:").grid(row=0, column=0)
        tk.Label(menu_frame, text="Price:").grid(row=1, column=0)

        self.name_entry = tk.Entry(menu_frame)
        self.price_entry = tk.Entry(menu_frame)

        self.name_entry.grid(row=0, column=1)
        self.price_entry.grid(row=1, column=1)

        tk.Button(menu_frame, text="Add Item", command=self.add_item).grid(row=2, column=0, pady=5)
        tk.Button(menu_frame, text="Delete Item", command=self.delete_item).grid(row=2, column=1, pady=5)

        self.menu_listbox = tk.Listbox(menu_frame, width=40)
        self.menu_listbox.grid(row=3, column=0, columnspan=2, pady=10)

        # Order Frame
        order_frame = tk.LabelFrame(root, text="Customer Order", padx=10, pady=10)
        order_frame.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(order_frame, text="Add Selected to Order", command=self.add_to_order).grid(row=0, column=0, pady=5)

        self.order_listbox = tk.Listbox(order_frame, width=40)
        self.order_listbox.grid(row=1, column=0, pady=10)

        tk.Button(order_frame, text="Calculate Total", command=self.calculate_total).grid(row=2, column=0)

    # -----------------------------
    # GUI Functions
    # -----------------------------
    def add_item(self):
        name = self.name_entry.get()
        price = self.price_entry.get()

        if not name or not price:
            messagebox.showerror("Error", "Please enter both name and price.")
            return

        try:
            float(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number.")
            return

        self.system.add_menu_item(name, price)
        self.update_menu_list()
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def delete_item(self):
        selected = self.menu_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select an item to delete.")
            return

        name = self.menu_listbox.get(selected).split(" - ")[0]
        self.system.delete_menu_item(name)
        self.update_menu_list()

    def add_to_order(self):
        selected = self.menu_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a menu item first.")
            return

        item_text = self.menu_listbox.get(selected)
        name, price = item_text.split(" - $")
        price = float(price)

        item = MenuItem(name, price)
        self.system.current_order.add_item(item)

        self.order_listbox.insert(tk.END, item_text)

    def calculate_total(self):
        total = self.system.current_order.calculate_total()
        messagebox.showinfo("Order Total", f"Total: ${total:.2f}")

    def update_menu_list(self):
        self.menu_listbox.delete(0, tk.END)
        for item in self.system.menu:
            self.menu_listbox.insert(tk.END, str(item))


# -----------------------------
# RUN APPLICATION
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeShopGUI(root)
    root.mainloop()
