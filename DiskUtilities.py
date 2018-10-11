import psutil
import tkinter as tk


def label_byte_sizes(size, precision=2):
    i = 0
    symbols = ('B', 'K', 'M', 'G', 'T')
    while size > 1024 and i < 4:
        i += 1
        size = size / 1024.0
    return "%.*f%s" % (precision, size, symbols[i])


def check_battery():
    battery = psutil.sensors_battery()
    print("BATTERY METRICS", "\nPercent charged:", battery.percent,
          "\nPlugged in:", battery.power_plugged, "\nTime remaining with charge:", battery.secsleft)


def find_users():
    users = psutil.users()
    print("USER METRICS")
    for user in users:
        print("User name:", user.name, "User terminal:", user.terminal, "User host:", user.host)


def check_cpu():
    logical_cores = psutil.cpu_count()
    physical_cores = psutil.cpu_count(logical=False)
    cpu_usage = psutil.cpu_times_percent()
    print("CPU METRICS")
    print("Logical cores:", logical_cores)
    print("Physical cores:", physical_cores)
    print("User CPU usage: ", cpu_usage.user, " System CPU usage:", cpu_usage.system)
    print("Total CPU usage:", cpu_usage.user + cpu_usage.system, "%")


def check_storage():
    storage_usage = psutil.disk_usage('/')
    print("STORAGE METRICS")
    print("Free storage space:", label_byte_sizes(storage_usage.free))
    print("Storage space used:", label_byte_sizes(storage_usage.used))
    print("Total storage space:", label_byte_sizes(storage_usage.total))
    print("Percent used:", storage_usage.percent, "%")


def check_processes():
    process_list = []
    process_info = {}
    for process in psutil.process_iter():
        try:
            process_info = process.as_dict(attrs=['pid', 'name', 'username'])
        except psutil.NoSuchProcess:
            pass
        process_list.append(process_info)


def create_gui():
    window = tk.Tk()
    window.title('Python Task Manager')
    window.geometry('400x400')

    processes_button = tk.Button(text="Processes")
    processes_button.grid(column=0, row=0)

    processes = check_processes()
    i = 1
    for process in processes:
        process_name = tk.Text(master=window, height=1, width=5)
        # process_cpu = tk.Text(master=window, height=1, width=10)
        process_name.grid(column=0, row=i)
        # process_cpu.grid(column=2, row=i)
        i += 1
        process_name.insert(tk.END, process.name())
        # process_cpu.insert(tk.END, process.cpu_percent())

    performance_button = tk.Button(text="Performance")
    performance_button.grid(column=1, row=0)
    window.mainloop()


check_battery()
find_users()
check_cpu()
check_storage()
# create_gui()
check_processes()