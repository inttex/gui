import dearpygui.dearpygui as dpg
from dearpygui.demo import show_demo

def main():
    dpg.create_context()
    show_demo()
    dpg.create_viewport(title='Custom Title', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()