import tkinter as tk


def main():
    def handle_click(event):
        print("The button was clicked!")

    window = tk.Tk()

    frame = tk.Frame()
    greeting = tk.Label(master=frame, text="Hello, Tkinter")
    button = tk.Button(master=frame, text="click me")
    greeting.pack()
    button.pack()
    frame.pack()

    def handle_keypress(event):
        print(f'keypress = {event.char}')

    window.bind("<Key>", handle_keypress)
    button.bind("<Button-1>", handle_click)

    window.mainloop()


if __name__ == '__main__':
    main()
