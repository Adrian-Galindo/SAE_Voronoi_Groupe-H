import tkinter as tk
from gui import VoronoiApp


def main():
    root = tk.Tk()
    VoronoiApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()