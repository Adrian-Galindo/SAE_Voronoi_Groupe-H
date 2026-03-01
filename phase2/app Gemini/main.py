import tkinter as tk
from voronoi_gui import VoronoiApp

def main():
    """Point d'entrée principal de l'application."""
    root = tk.Tk()
    app = VoronoiApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()