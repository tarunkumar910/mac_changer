import subprocess
import argparse
import re
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress

console = Console()

def display_intro():
    console.print(
        Panel("[bold cyan]MAC Changer[/bold cyan]\n[italic green]A utility to change your MAC address easily[/italic green]",
              title="Welcome", style="bold blue")
    )
    console.print("[bold yellow]Initializing the tool...[/bold yellow]\n", style="bold cyan")

def get_arg():
    parser = argparse.ArgumentParser(
        description="MAC Changer Utility",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-i", "--interface",
        dest="interface",
        required=True,
        help="Specify the network interface (e.g., eth0, wlan0)"
    )

    parser.add_argument(
        "-m", "--mac",
        dest="mac",
        required=True,
        help="Enter the MAC address you want to change to"
    )

    args = parser.parse_args()
    return args

def chn_mac(interface, mac):
    console.print(f"[bold green][+] Changing MAC address for {interface} to {mac}...[/bold green]")
    with Progress() as progress:
        task = progress.add_task("[cyan]Changing MAC address...", total=3)
        subprocess.call(["ifconfig", interface, "down"])
        progress.update(task, advance=1)
        subprocess.call(["ifconfig", interface, "hw", "ether", mac])
        progress.update(task, advance=1)
        subprocess.call(["ifconfig", interface, "up"])
        progress.update(task, advance=1)

def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
        mac_add = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

        if mac_add:
            return mac_add.group(0)
        else:
            console.print("[bold red][-] Could not read MAC address.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        return None


display_intro()


arg = get_arg()
current_mac = get_current_mac(arg.interface)

if current_mac:
    console.print(
        Panel(f"Current MAC: [bold yellow]{current_mac}[/bold yellow]", title="MAC Address", style="bold green")
    )

    chn_mac(arg.interface, arg.mac)

   
    updated_mac = get_current_mac(arg.interface)

    if updated_mac == arg.mac:
        console.print(
            Panel(f"[bold green][+] MAC address successfully changed to {updated_mac}[/bold green]", style="bold blue")
        )
    else:
        console.print(
            Panel("[bold red][-] MAC address did not change.[/bold red]", style="bold red")
        )
