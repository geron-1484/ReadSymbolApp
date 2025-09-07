from gui.app_gui import AppGUI

def main():
    app = AppGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()
