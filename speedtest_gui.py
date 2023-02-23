import tkinter as tk
import os, sys, path

def spdtest():
    import speedtest
    from time import sleep
    from threading import Thread as Process
    from tkinter import ttk

    threads = None

    spdtst_win = tk.Tk()
    spdtst_win.title("Speedtest by Ookla")
    try:
        resource_path = path.Path("speedtest_logo.png").get_path()
        ookla_logo = tk.PhotoImage(file=resource_path)
    except:
        ookla_logo = tk.PhotoImage(file="./thumbnails/other/speedtest_logo.png")
    spdtst_canvas = tk.Canvas(spdtst_win, height=400, width=400)
    spdtst_canvas.pack()
    spdtst_img = tk.Label(spdtst_win, image=ookla_logo, bg='black')
    spdtst_img.place(relheight=1, relwidth=1, relx=0, rely=0)
    while_label = tk.Label(spdtst_win, text="Press start to begin")
    while_label.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.2)
    output_label = tk.Label(spdtst_win, bg='white')
    bar_d = ttk.Progressbar(spdtst_win, length=300, mode='determinate', orient='horizontal')
    bar_ind = ttk.Progressbar(spdtst_win, length=300, mode='indeterminate', orient='horizontal')

    def test():
        output_label.place_forget()
        while_label.place_forget()
        while_label.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.2)
        button.place_forget()
        what0 = "Initializing...Please wait"
        while_label.configure(text=what0)
        spdtst_win.update()
        s = speedtest.Speedtest()
        message = "Finding optimal server. \nThis might take some time"
        while_label.configure(text=message)
        spdtst_win.update()
        def server():
            s.get_best_server()
        server_p = Process(target=server)
        server_p.start()
        bar_ind.place(anchor='c', relx=0.5, rely=0.6)
        while server_p.is_alive():
            bar_ind['value'] += 0.1
            spdtst_win.update()
            sleep(0.0005)
        bar_ind.place_forget()
        spdtst_win.update()
        msg0 = "Running Download test"
        while_label.configure(text=msg0)
        spdtst_win.update()
        def download_test():
            s.download(threads=threads)
        down_p = Process(target=download_test)
        down_p.start()
        bar_d.place(anchor='c', relx=0.5, rely=0.6)
        bar_d['value'] = 0
        for _ in range(1000):
            bar_d['value'] += 0.1
            spdtst_win.update()
            sleep(0.01)
        down_p.join()
        msg1 = "Running Upload test"
        while_label.configure(text=msg1)
        spdtst_win.update()
        def upload_test():
            s.upload(threads=threads, pre_allocate=False)
        up_p = Process(target=upload_test)
        up_p.start()
        bar_d['value'] = 0
        for _ in range(1000):
            bar_d['value'] += 0.1
            spdtst_win.update()
            sleep(0.01)
        bar_d.place_forget()
        up_p.join()
        msg2 = "Done!"
        while_label.configure(text=msg2)
        spdtst_win.update()
        s.results.share()
        results_dict = s.results.dict()
        server_dic = results_dict['server']
        client_dic = results_dict['client']
        server = f"{server_dic['sponsor']} \n- {server_dic['name']},{server_dic['country']}"
        ping = results_dict['ping']
        u = results_dict['upload']
        d = results_dict['download']
        ip = client_dic['ip']

        #download
        if d >= 1024*1024:
            down = f"{round(d/1024/1024, 2)}Mbps"
        elif d >= 1024:
            down = f"{round(d/1024, 2)}Kbps"
        else:
            down = f"{round(d, 4)}bps"
        #upload
        if u >= 1024*1024:
            up = f"{round(u/1024/1024, 2)}Mbps"
        elif u >= 1024:
            up = f"{round(u/1024, 2)}Kbps"
        else:
            up = f"{round(u, 4)}bps"

        while_label.place_forget()
        
        result = f"Ping : {ping}ms \nDownload speed : {down} \nUpload speed : {up} \nUser ip address: {ip} \nServer : {server}"

        output_label.configure(text=result)        
        output_label.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.4)

        button.configure(text="test again")
        button.place(anchor='c', relx=0.75, rely=0.8)

    button = tk.Button(spdtst_win, text="Start", command=test)
    button.place(anchor='c', relx=0.75, rely=0.8)

    spdtst_win.mainloop()

try:
    spdtest()
except Exception as e:
    root = tk.Tk()
    root.title("Error")
    label = tk.Label(root, text=f"Something went wrong :-/\nError code:{e}", bg='red')
    label.pack()
    root.mainloop()