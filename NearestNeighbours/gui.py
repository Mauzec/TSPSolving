import tkinter as tk
from tkinter import ttk
import json
from algo import NN
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt

class CustomUI:
    def __init__(self, master: tk.Tk, title: str):
        self.vertices_count = 0
        self.edges = list()
        self.vertices = list()

        self.master = master
        self.master.title(title)
        
        self.master['background'] = "#D6EAF8"
        self.create_widgets()
        self.canvas.bind("<Button-1>", self.add_vertex)
        self.master.mainloop()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=600, height=400, bg='#EBF5FB')
        self.canvas.grid(row=0, column=0, rowspan=6, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(self.master, columns=('From', 'To', 'Weight'), show='headings', style='Custom.Treeview')
        self.tree.heading('From', text='From')
        self.tree.heading('To', text='To')
        self.tree.heading('Weight', text='Weight')
        self.tree.grid(row=0, column=1, rowspan=6, padx=10, pady=10, sticky="nsew")

        ttk.Label(self.master, text="From:", style='Custom.TLabel', background='#D6EAF8').grid(row=0, column=2, pady=5, sticky="w")
        self.from_entry = ttk.Entry(self.master, background="blue")
        self.from_entry.grid(row=0, column=3, pady=5, sticky="w")

        ttk.Label(self.master, text="To:", style='Custom.TLabel', background="#D6EAF8").grid(row=1, column=2, pady=5, sticky="w")
        self.to_entry = ttk.Entry(self.master, background="grey")
        self.to_entry.grid(row=1, column=3, pady=5, sticky="w")

        ttk.Label(self.master, text="Weight:", style='Custom.TLabel', background="#D6EAF8").grid(row=2, column=2, pady=5, sticky="w")
        self.weight_entry = ttk.Entry(self.master, background="grey")
        self.weight_entry.grid(row=2, column=3, pady=5, sticky="w")

        ttk.Button(self.master, text="Add Edge", command=self.handle_add_edge, style='Custom.TButton', cursor='hand2', takefocus=False).grid(row=3, column=2, columnspan=2, pady=10, sticky="nsew")
        ttk.Button(self.master, text="Read JSON", command=self.read_json, style='Custom.TButton', cursor='hand2', takefocus=False).grid(row=4, column=2, columnspan=2, pady=10, sticky="nsew")
        ttk.Button(self.master, text='Search', command=self.search, style='Custom.TButton', cursor='hand2', takefocus=False).grid(row=5, column=2, columnspan=2, pady=10, sticky="nsew")

    def search(self):
        nn = NN()
        print(self.vertices)
        print(self.edges)
        print(self.vertices_count)
        nn.add_edges_nodes(self.vertices_count, self.edges)
        edges = nn.search(self.vertices_count)
        self.canvas.delete('all')
        self.vertices_count = 0
        self.edges.clear()
        self.tree.delete(*self.tree.get_children())
        weight = 0
        for i in range(len(self.vertices)):
            self.draw_vertex(self.vertices[i], append=False)
        for i in range(len(edges)):
            self.draw_edge(from_vertex=edges[i][0], to_vertex=edges[i][1], weight=edges[i][2])
            weight += edges[i][2]
        root.update()
        showinfo("Search Result", f"Weight: {weight}")

        

    def add_vertex(self, event):
        x, y = event.x, event.y
        self.draw_vertex((x, y))

    def draw_vertex(self, coordinates: tuple, append=True):
        x, y = coordinates
        if append: self.vertices.append((x, y))
        self.vertices_count += 1
        self.canvas.create_oval(x-10, y-10, x+10, y+10, fill='#58D68D')  # Green color
        self.canvas.create_text(x, y, text=str(self.vertices_count), fill='white') 

    def handle_add_edge(self):
        from_vertex = int(self.from_entry.get())
        to_vertex = int(self.to_entry.get())
        weight = int(self.weight_entry.get())
        
        if 0 < from_vertex <= self.vertices_count and 0 < to_vertex <= self.vertices_count:
            self.draw_edge(from_vertex, to_vertex, weight)
        else:
            return

    def draw_edge(self, from_vertex: int, to_vertex: int, weight: int):
        self.tree.insert('', 'end', values=(from_vertex, to_vertex, weight))
        self.edges.append({"from": from_vertex, "to": to_vertex, "weight": weight})

        from_x, from_y = self.get_vertex_coordinates(from_vertex)
        to_x, to_y = self.get_vertex_coordinates(to_vertex)
        
        to_x, to_y = self.get_coordinate_edge(from_x, from_y, to_x, to_y)

        line = self.canvas.create_line(from_x, from_y, to_x, to_y, width=2, fill='#E74C3C' if from_vertex < to_vertex else '#3498DB', arrow='last', tag='line')
        self.canvas.create_text((to_x + from_x) / 2 + 5, (to_y + from_y) / 2 + 5, text=str(weight), fill='#E74C3C' if from_vertex < to_vertex else '#3498DB')
        self.canvas.tag_lower(line)

    def get_vertex_coordinates(self, vertex: int):
        return self.vertices[vertex - 1]

    def get_coordinate_edge(self, x1, y1, x2, y2, r=10):
        k = (y2-y1) / (x2 - x1)
        d = (x2 + k**2 * x1 + k * (y2 - y1))**2 - (k**2 + 1) * (x2**2 + (k*x1)**2 + 2*k*x1*(y2-y1) + (y2-y1)**2 - r**2)
        
        x = (x2 + k**2 * x1 + k * (y2 - y1) - d**0.5) / (k**2 + 1)
        y = (x - x1) * k + y1
        o_1 = (x, y)
        
        x = (x2 + k**2 * x1 + k * (y2 - y1) + d**0.5) / (k**2 + 1)
        y = (x - x1) * k + y1
        o_2 = (x, y)
        
        return o_1 if (x1 - o_1[0])**2 + (y1 - o_1[1]) ** 2 < (x1 - o_2[0])**2 + (y1 - o_2[1]) ** 2 else o_2

    def read_json(self, name="graph.json"):
        self.vertices_count = 0
        self.vertices.clear()
        self.edges.clear()
        self.canvas.delete('all')
        self.tree.delete(*self.tree.get_children())
        with open(f"{name}", 'r') as file:
            data = json.load(file)
            
            for i in range(len(data["vertexes"])):
                vertex = (data["vertexes"][i]["x"], data["vertexes"][i]["y"])
                self.draw_vertex(vertex)
            
            for i in range(len(data["edges"])):
                edge = data["edges"][i]
                self.draw_edge(edge["from"], edge["to"], edge["weight"])

if __name__ == "__main__":
    root = tk.Tk()
    gui = CustomUI(root, "Customized Nearest Neighbors Algorithm")
