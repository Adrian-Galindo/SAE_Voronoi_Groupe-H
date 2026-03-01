"""Point d'entrée de l'application Diagramme de Voronoï."""
from ui.app import VoronoiApp


def main() -> None:
    app = VoronoiApp()
    app.mainloop()


if __name__ == "__main__":
    main()
