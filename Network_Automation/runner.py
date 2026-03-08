from netmiko import ConnectHandler
import time

def run_switch_commands(host, username, password, interface):
    switch = {
        "device_type": "hp_procurve",
        "host": host,
        "username": username,
        "password": password
    }

    try:
        conn = ConnectHandler(**switch)
        output = f"\n=== Switch: {host} ===\n"
        output += "\n--- Interface Status ---\n"
        output += conn.send_command(f"show interface {interface} brief")
        conn.send_command("diagnostics",expect_string=r"#")

        conn.send_command_timing("diagnostics")

        # Run cable test
        output += "\n\n--- Running Cable Test ---\n"
        result = conn.send_command_timing(f"diag cable-diagnostic test {interface}")

        if "Continue (y/n)?" in result:
            result += conn.send_command_timing("y")

        output += result

       
        time.sleep(2)

        # Show results
        output += "\n\n--- Cable Diagnostic Result ---\n"
        output += conn.send_command(f"diag cable-diagnostic show {interface}")

        output += "\n--- Interface Errors ---\n"
        output += conn.send_command(f"show interfaces {interface} counter errors")
        conn.disconnect()
        return output
    except Exception as e:
        return f"Error connecting to {host}: {str(e)}\n"