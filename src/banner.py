from pyfiglet import figlet_format
from rich import print

def banner(text):
    print(f"[bold cyan]{figlet_format(text)}[/bold cyan]")
