from gui import TrayPrinter
from model import cliprinter

Gui = 'gui'

def create_printer(printer_type = cliprinter.Printer):
    """creates appropriate printer object for logger"""

    if printer_type == Gui:
        return TrayPrinter.TrayPrinter()
    else:
        return cliprinter.CliPrinter()
