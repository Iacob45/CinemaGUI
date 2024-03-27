import customtkinter
import tkinter.ttk as ttk
import tkinter as tk
import mysql.connector
from PIL import Image, ImageTk
import datetime

class Aplicatie:


    def start(self, root=None, frame=None):
        if(frame != None):
            frame.destroy()
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("dark-blue")


        if(root == None):
            root = customtkinter.CTk()
            root.geometry("1980x1080")

        frame = customtkinter.CTkFrame(master=root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        button1 = customtkinter.CTkButton(master=frame, width=400, height=100, fg_color="#FF66CC",
                                          hover_color="#FFC1CC", font=("Roboto", 33), text="Movies",
                                          command=lambda: self.features(frame, root, "Movies"))
        button1.pack(pady=12, padx=10)
        button1.place(relx=0.5, rely=0.20, anchor='center')

        button2 = customtkinter.CTkButton(master=frame, width=400, height=100, fg_color="#77C3EC",
                                          hover_color="#446CCF", font=("Roboto", 33), text="Locations",
                                          command=lambda: self.features(frame, root, "Locations"))
        button2.pack(pady=12, padx=10)
        button2.place(relx=0.5, rely=0.45, anchor='center')

        button3 = customtkinter.CTkButton(master=frame, width=400, height=100, fg_color="#66FF00",
                                          hover_color="#B0FC38", font=("Roboto", 33), text="Screenings",
                                          command=lambda: self.features(frame, root, "Screenings"))
        button3.pack(pady=12, padx=10)
        button3.place(relx=0.5, rely=0.70, anchor='center')


        root.mainloop()


    def features(self, frame, root, app):
        frame.destroy()
        customtkinter.set_default_color_theme("green")


        frame = customtkinter.CTkFrame(master=root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        button1 = customtkinter.CTkButton(master=frame, width=300, height=60, fg_color="#C80815", hover_color="#B90E0A", font=("Roboto", 25),
                                          text=app + " View",
                                          command=lambda: self.viewtabel(frame, root, app))
        button1.pack(pady=12, padx=10)
        button1.place(relx=0.3, rely=0.3, anchor='center')

        button2 = customtkinter.CTkButton(master=frame, width=300, height=60, fg_color="#C80815", hover_color="#B90E0A", font=("Roboto", 25),
                                          text="Modify " + app,
                                          command=lambda: self.modifytabel(frame, root, app))
        button2.pack(pady=12, padx=10)
        button2.place(relx=0.3, rely=0.42, anchor='center')

        button3 = customtkinter.CTkButton(master=frame, width=300, height=60, fg_color="#C80815", hover_color="#B90E0A", font=("Roboto", 25),
                                          text="Insert Into " + app,
                                          command=lambda: self.insertintotabel(frame, root, app))
        button3.pack(pady=12, padx=10)
        button3.place(relx=0.3, rely=0.54, anchor='center')

        button4 = customtkinter.CTkButton(master=frame, width=300, height=60, fg_color="#C80815", hover_color="#B90E0A", font=("Roboto", 25),
                                          text="Delete From " + app,
                                          command=lambda: self.deletefromtabel(frame, root, app))
        button4.pack(pady=12, padx=10)
        button4.place(relx=0.3, rely=0.66, anchor='center')


        back_img = customtkinter.CTkImage(Image.open("assets/backarrow.png"), size=(30, 30))
        back_button = customtkinter.CTkButton(master=frame, width=66, height=26, text="", image=back_img,
                                              fg_color="#FC8EAC", hover_color="#FC6C85",
                                              command=lambda: self.start(root, frame))
        back_button.pack()
        back_button.place(relx=0.07, rely=0.12, anchor='w')



    def viewtabel(self, frame, root, app):
        frame.destroy()


        frame = customtkinter.CTkFrame(master=root)

        frame.grid(row=1, column=0, padx=15, pady=15)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Roboto", 14))
        style.configure("Treeview", font=("Roboto", 11))

        label = customtkinter.CTkLabel(master=frame, text=app + " View", font=("Roboto", 30))
        label.grid(row=0, column=0, padx=45, pady=10)

        add_menu_display211 = customtkinter.CTkFrame(master=frame,
                                                          corner_radius=15,
                                                          height=1800,
                                                          width=900)
        add_menu_display211.grid(pady=30, padx=30, sticky="nsew")




        if app == "Movies":
            columns = ('id_movie', 'name', 'length', 'director', 'rating', 'genre', 'launch_date')

            table = ttk.Treeview(master=add_menu_display211,
                                 columns=columns,
                                 selectmode='browse',
                                 show='headings')

            table.column("#1", anchor="c", minwidth=100, width=100)
            table.column("#2", anchor="w", minwidth=270, width=270)
            table.column("#3", anchor="c", minwidth=120, width=120)
            table.column("#4", anchor="c", minwidth=270, width=270)
            table.column("#5", anchor="c", minwidth=220, width=220)
            table.column("#6", anchor="c", minwidth=320, width=320)
            table.column("#7", anchor="c", minwidth=320, width=320)

            table.heading('id_movie', text='Movie ID')
            table.heading('name', text='Name')
            table.heading('length', text='Length')
            table.heading('director', text='Director')
            table.heading('rating', text='Rating')
            table.heading('genre', text='Genre')
            table.heading('launch_date', text='Launch Date')

            self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                      database="cinema")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                                        SELECT id_movie FROM movies
                                        """)
            results = [row[0] for row in self.cursor.fetchall()]
            self.connection.close()
            vector = []

            for x in results:
                d = Movie()
                d.load_movie(x)
                vector.append((d.id_movie, d.name, d.length, d.director, d.rating, d.genre, d.launch_date))

            for x in vector:
                table.insert('', tk.END, values=x)

            table.grid(row=1, column=0, padx=10, pady=10)
            table.bind('<Motion>', 'break')

        if app == "Locations":
            columns = ('id_location', 'name', 'phone_number', 'city', 'adress')

            table = ttk.Treeview(master=add_menu_display211,
                                 columns=columns,
                                 selectmode='browse',
                                 show='headings')

            table.column("#1", anchor="c", minwidth=150, width=100)
            table.column("#2", anchor="w", minwidth=270, width=270)
            table.column("#3", anchor="c", minwidth=180, width=180)
            table.column("#4", anchor="c", minwidth=170, width=170)
            table.column("#5", anchor="c", minwidth=790, width=790)

            table.heading('id_location', text='Location ID')
            table.heading('name', text='Name')
            table.heading('phone_number', text='Phone Number')
            table.heading('city', text='City')
            table.heading('adress', text='Adress')


            self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                      database="cinema")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                                SELECT id_location FROM locations
                                """)
            results = [row[0] for row in self.cursor.fetchall()]
            self.connection.close()
            vector = []

            for x in results:
                d = Location()
                d.load_location(x)
                vector.append((d.id_location, d.name, d.phone_number, d.city, d.adress))

            for x in vector:
                table.insert('', tk.END, values=x)

            table.grid(row=1, column=0, padx=10, pady=10)
            table.bind('<Motion>', 'break')


        if app == "Screenings":
            columns = ('id_screening', 'start_time', 'ticket_price', 'id_movie', 'id_location', "movie_name", "location_name", "city")

            table = ttk.Treeview(master=add_menu_display211,
                                 columns=columns,
                                 selectmode='browse',
                                 show='headings')

            table.column("#1", anchor="c", minwidth=150, width=100)
            table.column("#2", anchor="c", minwidth=170, width=170)
            table.column("#3", anchor="c", minwidth=150, width=150)
            table.column("#4", anchor="c", minwidth=130, width=130)
            table.column("#5", anchor="c", minwidth=130, width=130)
            table.column("#6", anchor="w", minwidth=350, width=350)
            table.column("#7", anchor="w", minwidth=350, width=350)
            table.column("#8", anchor="c", minwidth=220, width=220)

            table.heading('id_screening', text='Screening ID')
            table.heading('start_time', text='Start Time')
            table.heading('ticket_price', text='Ticket Price')
            table.heading('id_movie', text='Movie ID')
            table.heading('id_location', text='Location ID')
            table.heading('movie_name', text='Movie Name')
            table.heading('location_name', text='Location Name')
            table.heading('city', text='City')

            self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                      database="cinema")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                                SELECT id_screening FROM screenings
                                """)
            results = [row[0] for row in self.cursor.fetchall()]
            self.connection.close()
            vector = []

            for x in results:
                d = Screening()
                d.load_screening(x)
                j = Movie()
                j.load_movie(d.id_movie)
                i = Location()
                i.load_location(d.id_location)
                vector.append((d.id_screening, d.start_time, d.ticket_price, d.id_movie, d.id_location, j.name, i.name, i.city))

            for x in vector:
                table.insert('', tk.END, values=x)

            table.grid(row=1, column=0, padx=10, pady=10)
            table.bind('<Motion>', 'break')

        back_img = customtkinter.CTkImage(Image.open("assets/backarrow.png"), size=(30, 30))
        back_button = customtkinter.CTkButton(master=frame, width=66, height=26, text="", image=back_img,
                                              fg_color="#FC8EAC", hover_color="#FC6C85",
                                              command=lambda: self.features(frame, root, app))
        back_button.grid(row=0, column=0, padx=45, pady=10, sticky="w")

        frame.grid(row=0, column=0, sticky="NESW")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        frame.pack(pady=20, padx=60, expand=True)


    def modifytabel(self, frame, root, app):
        frame.destroy()

        frame = customtkinter.CTkFrame(master=root)

        frame.grid(row=5, column=0, padx=15, pady=15)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Roboto", 14))
        style.configure("Treeview", font=("Roboto", 11))

        label = customtkinter.CTkLabel(master=frame, text=app, font=("Roboto", 30))
        label.grid(row=0, column=0, padx=45, pady=10)

        add_menu_display211 = customtkinter.CTkFrame(master=frame,
                                                     corner_radius=15,
                                                     height=1920,
                                                     width=1080)
        add_menu_display211.grid(pady=30, padx=30, sticky="nsew")

        if app == "Movies":
            columns = ('id_movie', 'name', 'length', 'director', 'rating', 'genre', 'launch_date')

            table = ttk.Treeview(master=add_menu_display211,
                                 columns=columns,
                                 selectmode='browse',
                                 show='headings')

            table.column("#1", anchor="c", minwidth=100, width=100)
            table.column("#2", anchor="w", minwidth=270, width=270)
            table.column("#3", anchor="c", minwidth=120, width=120)
            table.column("#4", anchor="c", minwidth=270, width=270)
            table.column("#5", anchor="c", minwidth=220, width=220)
            table.column("#6", anchor="c", minwidth=320, width=320)
            table.column("#7", anchor="c", minwidth=320, width=320)

            table.heading('id_movie', text='Movie ID')
            table.heading('name', text='Name')
            table.heading('length', text='Length')
            table.heading('director', text='Director')
            table.heading('rating', text='Rating')
            table.heading('genre', text='Genre')
            table.heading('launch_date', text='Launch Date')

            self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                      database="cinema")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                                                SELECT id_movie FROM movies
                                                """)
            results = [row[0] for row in self.cursor.fetchall()]
            self.connection.close()
            vector = []

            for x in results:
                d = Movie()
                d.load_movie(x)
                vector.append((d.id_movie, d.name, d.length, d.director, d.rating, d.genre, d.launch_date))

            for x in vector:
                table.insert('', tk.END, values=x)

            table.grid(row=1, column=0, padx=10, pady=10)
            table.bind('<Motion>', 'break')

            label1 = customtkinter.CTkLabel(master=frame, text="Modify Row", font=("Roboto", 30))
            label1.grid(row=2, column=0, padx=45, pady=10)

            add_menu_display212 = customtkinter.CTkFrame(master=frame,
                                                         corner_radius=15,
                                                         height=1920,
                                                         width=1080)
            add_menu_display212.grid(pady=30, padx=30, sticky="nsew")
            table2 = ttk.Treeview(master=add_menu_display212,
                                  columns=columns,
                                  height=0,
                                  selectmode='browse',
                                  show='headings')
            table2.column("#1", anchor="c", minwidth=100, width=100)
            table2.column("#2", anchor="w", minwidth=100, width=100)
            table2.column("#3", anchor="c", minwidth=100, width=100)
            table2.column("#4", anchor="c", minwidth=100, width=100)
            table2.column("#5", anchor="c", minwidth=100, width=100)
            table2.column("#6", anchor="c", minwidth=100, width=100)
            table2.column("#7", anchor="c", minwidth=150, width=150)

            table2.heading('id_movie', text='Movie ID')
            table2.heading('name', text='Name')
            table2.heading('length', text='Length')
            table2.heading('director', text='Director')
            table2.heading('rating', text='Rating')
            table2.heading('genre', text='Genre')
            table2.heading('launch_date', text='Launch Date')
            table2.grid(row=3, column=0, padx=10, pady=0)
            table2.bind('<Motion>', 'break')

            entry1 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Movie ID")
            entry1.grid(row=4, column=0, padx=38, pady=10, sticky='w')
            entry2 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Name")
            entry2.grid(row=4, column=0, padx=118, pady=10, sticky='w')
            entry3 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Length")
            entry3.grid(row=4, column=0, padx=198, pady=10, sticky='w')
            entry4 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Director")
            entry4.grid(row=4, column=0, padx=278, pady=10, sticky='w')
            entry5 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Rating")
            entry5.grid(row=4, column=0, padx=358, pady=10, sticky='w')
            entry6 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Genre")
            entry6.grid(row=4, column=0, padx=438, pady=10, sticky='w')
            entry7 = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="YYYY-MM-DD")
            entry7.grid(row=4, column=0, padx=518, pady=10, sticky='w')

            entry_button = customtkinter.CTkButton(master=frame, width=100, height=26, text="Modify",
                                                  fg_color="#FC8EAC", hover_color="#FC6C85",
                                                  command=lambda: self.checkmodify(frame, root, app, results, entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), entry6.get(), entry7.get()))
            entry_button.grid(row=5, column=0, padx=40, pady=15, sticky="w")




        if app == "Locations":
            columns = ('id_location', 'name', 'phone_number', 'city', 'adress')

            table = ttk.Treeview(master=add_menu_display211,
                                 columns=columns,
                                 selectmode='browse',
                                 show='headings')

            table.column("#1", anchor="c", minwidth=150, width=100)
            table.column("#2", anchor="w", minwidth=270, width=270)
            table.column("#3", anchor="c", minwidth=180, width=180)
            table.column("#4", anchor="c", minwidth=170, width=170)
            table.column("#5", anchor="c", minwidth=790, width=790)

            table.heading('id_location', text='Location ID')
            table.heading('name', text='Name')
            table.heading('phone_number', text='Phone Number')
            table.heading('city', text='City')
            table.heading('adress', text='Adress')

            self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                      database="cinema")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                                        SELECT id_location FROM locations
                                        """)
            results = [row[0] for row in self.cursor.fetchall()]
            self.connection.close()
            vector = []

            for x in results:
                d = Location()
                d.load_location(x)
                vector.append((d.id_location, d.name, d.phone_number, d.city, d.adress))

            for x in vector:
                table.insert('', tk.END, values=x)

            table.grid(row=1, column=0, padx=10, pady=10)
            table.bind('<Motion>', 'break')

            label1 = customtkinter.CTkLabel(master=frame, text="Modify Row", font=("Roboto", 30))
            label1.grid(row=2, column=0, padx=45, pady=10)

            add_menu_display212 = customtkinter.CTkFrame(master=frame,
                                                         corner_radius=15,
                                                         height=1920,
                                                         width=1080)
            add_menu_display212.grid(pady=30, padx=30, sticky="nsew")
            table2 = ttk.Treeview(master=add_menu_display212,
                                  columns=columns,
                                  height=0,
                                  selectmode='browse',
                                  show='headings')
            table2.column("#1", anchor="c", minwidth=120, width=120)
            table2.column("#2", anchor="w", minwidth=100, width=100)
            table2.column("#3", anchor="c", minwidth=150, width=150)
            table2.column("#4", anchor="c", minwidth=100, width=100)
            table2.column("#5", anchor="c", minwidth=100, width=100)

            table2.heading('id_location', text='Location ID')
            table2.heading('name', text='Name')
            table2.heading('phone_number', text='Phone Number')
            table2.heading('city', text='City')
            table2.heading('adress', text='Adress')
            table2.grid(row=3, column=0, padx=10, pady=0)
            table2.bind('<Motion>', 'break')

            entry1 = customtkinter.CTkEntry(master=frame, width=100, placeholder_text="Location ID")
            entry1.grid(row=4, column=0, padx=38, pady=10, sticky='w')
            entry2 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Name")
            entry2.grid(row=4, column=0, padx=138, pady=10, sticky='w')
            entry3 = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Phone Number")
            entry3.grid(row=4, column=0, padx=218, pady=10, sticky='w')
            entry4 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="City")
            entry4.grid(row=4, column=0, padx=338, pady=10, sticky='w')
            entry5 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Adress")
            entry5.grid(row=4, column=0, padx=408, pady=10, sticky='w')


            entry_button = customtkinter.CTkButton(master=frame, width=100, height=26, text="Modify",
                                                   fg_color="#FC8EAC", hover_color="#FC6C85",
                                                   command=lambda: self.checkmodify1(frame, root, app, results,
                                                                                    entry1.get(), entry2.get(),
                                                                                    entry3.get(), entry4.get(),
                                                                                    entry5.get()))
            entry_button.grid(row=5, column=0, padx=40, pady=15, sticky="w")


        if app == "Screenings":
            columns = (
            'id_screening', 'start_time', 'ticket_price', 'id_movie', 'id_location', "movie_name", "location_name",
            "city")

            table = ttk.Treeview(master=add_menu_display211,
                                 columns=columns,
                                 selectmode='browse',
                                 show='headings')

            table.column("#1", anchor="c", minwidth=150, width=100)
            table.column("#2", anchor="c", minwidth=170, width=170)
            table.column("#3", anchor="c", minwidth=150, width=150)
            table.column("#4", anchor="c", minwidth=130, width=130)
            table.column("#5", anchor="c", minwidth=130, width=130)
            table.column("#6", anchor="w", minwidth=350, width=350)
            table.column("#7", anchor="w", minwidth=350, width=350)
            table.column("#8", anchor="c", minwidth=220, width=220)

            table.heading('id_screening', text='Screening ID')
            table.heading('start_time', text='Start Time')
            table.heading('ticket_price', text='Ticket Price')
            table.heading('id_movie', text='Movie ID')
            table.heading('id_location', text='Location ID')
            table.heading('movie_name', text='Movie Name')
            table.heading('location_name', text='Location Name')
            table.heading('city', text='City')

            self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                      database="cinema")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                                        SELECT id_screening FROM screenings
                                        """)
            results = [row[0] for row in self.cursor.fetchall()]
            self.connection.close()
            vector = []

            for x in results:
                d = Screening()
                d.load_screening(x)
                j = Movie()
                j.load_movie(d.id_movie)
                i = Location()
                i.load_location(d.id_location)
                vector.append(
                    (d.id_screening, d.start_time, d.ticket_price, d.id_movie, d.id_location, j.name, i.name, i.city))

            for x in vector:
                table.insert('', tk.END, values=x)

            table.grid(row=1, column=0, padx=10, pady=10)
            table.bind('<Motion>', 'break')

            label1 = customtkinter.CTkLabel(master=frame, text="Modify Row", font=("Roboto", 30))
            label1.grid(row=2, column=0, padx=45, pady=10)

            add_menu_display212 = customtkinter.CTkFrame(master=frame,
                                                         corner_radius=15,
                                                         height=1920,
                                                         width=1080)
            add_menu_display212.grid(pady=30, padx=30, sticky="nsew")
            table2 = ttk.Treeview(master=add_menu_display212,
                                  columns=columns,
                                  height=0,
                                  selectmode='browse',
                                  show='headings')
            table2.column("#1", anchor="c", minwidth=120, width=120)
            table2.column("#2", anchor="w", minwidth=120, width=120)
            table2.column("#3", anchor="c", minwidth=120, width=120)
            table2.column("#4", anchor="c", minwidth=100, width=100)
            table2.column("#5", anchor="c", minwidth=120, width=120)
            table2.column("#6", anchor="c", minwidth=100, width=100)
            table2.column("#7", anchor="c", minwidth=120, width=120)
            table2.column("#8", anchor="c", minwidth=100, width=100)

            table2.heading('id_screening', text='Screening ID')
            table2.heading('start_time', text='Start Time')
            table2.heading('ticket_price', text='Ticket Price')
            table2.heading('id_movie', text='Movie ID')
            table2.heading('id_location', text='Location ID')
            table2.heading('movie_name', text='Movie Name')
            table2.heading('location_name', text='Location Name')
            table2.heading('city', text='City')
            table2.grid(row=3, column=0, padx=10, pady=0)
            table2.bind('<Motion>', 'break')

            entry1 = customtkinter.CTkEntry(master=frame, width=100, placeholder_text="Screening ID")
            entry1.grid(row=4, column=0, padx=38, pady=10, sticky='w')
            entry2 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Start Time")
            entry2.grid(row=4, column=0, padx=138, pady=10, sticky='w')
            entry3 = customtkinter.CTkEntry(master=frame, width=100, placeholder_text="Ticket Price")
            entry3.grid(row=4, column=0, padx=218, pady=10, sticky='w')
            entry4 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Movie ID")
            entry4.grid(row=4, column=0, padx=318, pady=10, sticky='w')
            entry5 = customtkinter.CTkEntry(master=frame, width=100, placeholder_text="Location ID")
            entry5.grid(row=4, column=0, padx=398, pady=10, sticky='w')
            entry6 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Movie Name")
            entry6.grid(row=4, column=0, padx=498, pady=10, sticky='w')
            entry7 = customtkinter.CTkEntry(master=frame, width=100, placeholder_text="Location Name")
            entry7.grid(row=4, column=0, padx=578, pady=10, sticky='w')
            entry8 = customtkinter.CTkEntry(master=frame, width=60, placeholder_text="City")
            entry8.grid(row=4, column=0, padx=678, pady=10, sticky='w')

            entry_button = customtkinter.CTkButton(master=frame, width=100, height=26, text="Modify",
                                                   fg_color="#FC8EAC", hover_color="#FC6C85",
                                                   command=lambda: self.checkmodify2(frame, root, app, results,
                                                                                     entry1.get(), entry2.get(),
                                                                                     entry3.get(), entry4.get(),
                                                                                     entry5.get(), entry6.get(),
                                                                                     entry7.get(), entry8.get()))
            entry_button.grid(row=5, column=0, padx=40, pady=15, sticky="w")

        back_img = customtkinter.CTkImage(Image.open("assets/backarrow.png"), size=(30, 30))
        back_button = customtkinter.CTkButton(master=frame, width=66, height=26, text="", image=back_img,
                                              fg_color="#FC8EAC", hover_color="#FC6C85",
                                              command=lambda: self.features(frame, root, app))
        back_button.grid(row=0, column=0, padx=45, pady=10, sticky="w")

        frame.grid(row=0, column=0, sticky="NESW")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        frame.pack(pady=20, padx=60, expand=True)

    def checkmodify(self, frame, root, app, results, e1, e2, e3 ,e4, e5, e6, e7):
        if e1 != '':
            k = 0
            for x in results:
                if int(e1) == x:
                    d = Movie()
                    d.load_movie(x)
                    if e2 != '':
                        d.name = e2
                    if e3 != '':
                        d.length = e3
                    if e4 != '':
                        d.director = e4
                    if e5 != '':
                        d.rating = e5
                    if e6 != '':
                        d.genre = e6
                    if e7 != '':
                        d.launch_date = e7
                    d.update_movie()
                    k = 1
                    label1 = customtkinter.CTkLabel(master=frame, width=300, text="Row modified",
                                                    text_color='green', font=("Roboto", 16))
                    label1.grid(row=5, column=0, padx=45, pady=10)
                    break

            if k == 0:
                label1 = customtkinter.CTkLabel(master=frame, width=300, text="There are no row with the selected ID",
                                                text_color='red', font=("Roboto", 16))
                label1.grid(row=5, column=0, padx=45, pady=10)

    def checkmodify1(self, frame, root, app, results, e1, e2, e3 ,e4, e5):
        if e1 != '':
            k = 0
            for x in results:
                if int(e1) == x:
                    d = Location()
                    d.load_location(x)
                    if e2 != '':
                        d.name = e2
                    if e3 != '':
                        d.phone_number = e3
                    if e4 != '':
                        d.city = e4
                    if e5 != '':
                        d.adress = e5
                    d.update_location()
                    k = 1
                    label1 = customtkinter.CTkLabel(master=frame, width=300, text="Row modified",
                                                    text_color='green', font=("Roboto", 16))
                    label1.grid(row=5, column=0, padx=45, pady=10)
                    break

            if k == 0:
                label1 = customtkinter.CTkLabel(master=frame, width=300, text="There are no row with the selected ID",
                                                text_color='red', font=("Roboto", 16))
                label1.grid(row=5, column=0, padx=45, pady=10)


    def checkmodify2(self, frame, root, app, results, e1, e2, e3 ,e4, e5, e6, e7, e8):
        if e1 != '':
            k = 0
            for x in results:
                if int(e1) == x:
                    d = Screening()
                    d.load_screening(x)
                    i = Location()
                    i.load_location(d.id_location)
                    j = Movie()
                    j.load_movie(d.id_movie)
                    if e2 != '':
                        d.start_time = e2
                    if e3 != '':
                        d.ticket_price = e3
                    if e4 != '':
                        d.id_movie = e4
                    if e5 != '':
                        d.id_location = e5
                    if e6 != '':
                        j.name = e6
                    if e7 != '':
                        i.name = e7
                    if e8 != '':
                        i.location = e8
                    d.update_screening()
                    i.update_location()
                    j.update_movie()
                    k = 1
                    label1 = customtkinter.CTkLabel(master=frame, width=300, text="Row modified",
                                                    text_color='green', font=("Roboto", 16))
                    label1.grid(row=5, column=0, padx=45, pady=10)
                    break

            if k == 0:
                label1 = customtkinter.CTkLabel(master=frame, width=300, text="There are no row with the selected ID",
                                                text_color='red', font=("Roboto", 16))
                label1.grid(row=5, column=0, padx=45, pady=10)

    def insertintotabel(self, frame, root, app):
        frame.destroy()

        frame = customtkinter.CTkFrame(master=root)

        frame.grid(row=5, column=0, padx=15, pady=15)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Roboto", 14))
        style.configure("Treeview", font=("Roboto", 11))

        label = customtkinter.CTkLabel(master=frame, text=app, font=("Roboto", 30))
        label.grid(row=0, column=0, padx=45, pady=10)

        add_menu_display211 = customtkinter.CTkFrame(master=frame,
                                                     corner_radius=15,
                                                     height=1920,
                                                     width=1080)
        add_menu_display211.grid(pady=30, padx=30, sticky="nsew")

        if app == "Movies":
            columns = ('id_movie', 'name', 'length', 'director', 'rating', 'genre', 'launch_date')
            columns2 = ('name', 'length', 'director', 'rating', 'genre', 'launch_date')

            table = ttk.Treeview(master=add_menu_display211,
                                 columns=columns,
                                 selectmode='browse',
                                 show='headings')

            table.column("#1", anchor="c", minwidth=100, width=100)
            table.column("#2", anchor="w", minwidth=270, width=270)
            table.column("#3", anchor="c", minwidth=120, width=120)
            table.column("#4", anchor="c", minwidth=270, width=270)
            table.column("#5", anchor="c", minwidth=220, width=220)
            table.column("#6", anchor="c", minwidth=320, width=320)
            table.column("#7", anchor="c", minwidth=320, width=320)

            table.heading('id_movie', text='Movie ID')
            table.heading('name', text='Name')
            table.heading('length', text='Length')
            table.heading('director', text='Director')
            table.heading('rating', text='Rating')
            table.heading('genre', text='Genre')
            table.heading('launch_date', text='Launch Date')

            self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                      database="cinema")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                                                        SELECT id_movie FROM movies
                                                        """)
            results = [row[0] for row in self.cursor.fetchall()]
            self.connection.close()
            vector = []

            for x in results:
                d = Movie()
                d.load_movie(x)
                vector.append((d.id_movie, d.name, d.length, d.director, d.rating, d.genre, d.launch_date))

            for x in vector:
                table.insert('', tk.END, values=x)

            table.grid(row=1, column=0, padx=10, pady=10)
            table.bind('<Motion>', 'break')

            label1 = customtkinter.CTkLabel(master=frame, text="Insert Row", font=("Roboto", 30))
            label1.grid(row=2, column=0, padx=45, pady=10)

            add_menu_display212 = customtkinter.CTkFrame(master=frame,
                                                         corner_radius=15,
                                                         height=1920,
                                                         width=1080)
            add_menu_display212.grid(pady=30, padx=30, sticky="nsew")
            table2 = ttk.Treeview(master=add_menu_display212,
                                  columns=columns2,
                                  height=0,
                                  selectmode='browse',
                                  show='headings')
            table2.column("#1", anchor="w", minwidth=100, width=100)
            table2.column("#2", anchor="c", minwidth=100, width=100)
            table2.column("#3", anchor="c", minwidth=100, width=100)
            table2.column("#4", anchor="c", minwidth=100, width=100)
            table2.column("#5", anchor="c", minwidth=100, width=100)
            table2.column("#6", anchor="c", minwidth=150, width=150)

            table2.heading('name', text='Name')
            table2.heading('length', text='Length')
            table2.heading('director', text='Director')
            table2.heading('rating', text='Rating')
            table2.heading('genre', text='Genre')
            table2.heading('launch_date', text='Launch Date')
            table2.grid(row=3, column=0, padx=10, pady=0)
            table2.bind('<Motion>', 'break')

            entry2 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Name")
            entry2.grid(row=4, column=0, padx=38, pady=10, sticky='w')
            entry3 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Length")
            entry3.grid(row=4, column=0, padx=118, pady=10, sticky='w')
            entry4 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Director")
            entry4.grid(row=4, column=0, padx=198, pady=10, sticky='w')
            entry5 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Rating")
            entry5.grid(row=4, column=0, padx=278, pady=10, sticky='w')
            entry6 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Genre")
            entry6.grid(row=4, column=0, padx=358, pady=10, sticky='w')
            entry7 = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="YYYY-MM-DD")
            entry7.grid(row=4, column=0, padx=438, pady=10, sticky='w')

            entry_button = customtkinter.CTkButton(master=frame, width=100, height=26, text="Insert",
                                                   fg_color="#03AC13", hover_color="#5DBB63",
                                                   command=lambda: self.checkinsert(frame, root, app, results,
                                                                                    entry2.get(),
                                                                                    entry3.get(), entry4.get(),
                                                                                    entry5.get(), entry6.get(),
                                                                                    entry7.get()))
            entry_button.grid(row=5, column=0, padx=40, pady=15, sticky="w")

        if app == "Locations":
            columns = ('id_location', 'name', 'phone_number', 'city', 'adress')
            columns2 = ('name', 'phone_number', 'city', 'adress')

            table = ttk.Treeview(master=add_menu_display211,
                                 columns=columns,
                                 selectmode='browse',
                                 show='headings')

            table.column("#1", anchor="c", minwidth=150, width=100)
            table.column("#2", anchor="w", minwidth=270, width=270)
            table.column("#3", anchor="c", minwidth=180, width=180)
            table.column("#4", anchor="c", minwidth=170, width=170)
            table.column("#5", anchor="c", minwidth=790, width=790)

            table.heading('id_location', text='Location ID')
            table.heading('name', text='Name')
            table.heading('phone_number', text='Phone Number')
            table.heading('city', text='City')
            table.heading('adress', text='Adress')

            self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                      database="cinema")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                                                SELECT id_location FROM locations
                                                """)
            results = [row[0] for row in self.cursor.fetchall()]
            self.connection.close()
            vector = []

            for x in results:
                d = Location()
                d.load_location(x)
                vector.append((d.id_location, d.name, d.phone_number, d.city, d.adress))

            for x in vector:
                table.insert('', tk.END, values=x)

            table.grid(row=1, column=0, padx=10, pady=10)
            table.bind('<Motion>', 'break')

            label1 = customtkinter.CTkLabel(master=frame, text="Insert Row", font=("Roboto", 30))
            label1.grid(row=2, column=0, padx=45, pady=10)

            add_menu_display212 = customtkinter.CTkFrame(master=frame,
                                                         corner_radius=15,
                                                         height=1920,
                                                         width=1080)
            add_menu_display212.grid(pady=30, padx=30, sticky="nsew")
            table2 = ttk.Treeview(master=add_menu_display212,
                                  columns=columns2,
                                  height=0,
                                  selectmode='browse',
                                  show='headings')
            table2.column("#1", anchor="w", minwidth=100, width=100)
            table2.column("#2", anchor="c", minwidth=150, width=150)
            table2.column("#3", anchor="c", minwidth=100, width=100)
            table2.column("#4", anchor="c", minwidth=100, width=100)

            table2.heading('name', text='Name')
            table2.heading('phone_number', text='Phone Number')
            table2.heading('city', text='City')
            table2.heading('adress', text='Adress')
            table2.grid(row=3, column=0, padx=10, pady=0)
            table2.bind('<Motion>', 'break')

            entry2 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Name")
            entry2.grid(row=4, column=0, padx=38, pady=10, sticky='w')
            entry3 = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Phone Number")
            entry3.grid(row=4, column=0, padx=118, pady=10, sticky='w')
            entry4 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="City")
            entry4.grid(row=4, column=0, padx=238, pady=10, sticky='w')
            entry5 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Adress")
            entry5.grid(row=4, column=0, padx=318, pady=10, sticky='w')

            entry_button = customtkinter.CTkButton(master=frame, width=100, height=26, text="Insert",
                                                   fg_color="#03AC13", hover_color="#5DBB63",
                                                   command=lambda: self.checkinsert1(frame, root, app, results,
                                                                                     entry2.get(),
                                                                                     entry3.get(), entry4.get(),
                                                                                     entry5.get()))
            entry_button.grid(row=5, column=0, padx=40, pady=15, sticky="w")

        if app == "Screenings":
            columns = (
                'id_screening', 'start_time', 'ticket_price', 'id_movie', 'id_location', "movie_name", "location_name",
                "city")
            columns2 = (
                'start_time', 'ticket_price', 'id_movie', 'id_location')

            table = ttk.Treeview(master=add_menu_display211,
                                 columns=columns,
                                 selectmode='browse',
                                 show='headings')

            table.column("#1", anchor="c", minwidth=150, width=100)
            table.column("#2", anchor="c", minwidth=170, width=170)
            table.column("#3", anchor="c", minwidth=150, width=150)
            table.column("#4", anchor="c", minwidth=130, width=130)
            table.column("#5", anchor="c", minwidth=130, width=130)
            table.column("#6", anchor="w", minwidth=350, width=350)
            table.column("#7", anchor="w", minwidth=350, width=350)
            table.column("#8", anchor="c", minwidth=220, width=220)

            table.heading('id_screening', text='Screening ID')
            table.heading('start_time', text='Start Time')
            table.heading('ticket_price', text='Ticket Price')
            table.heading('id_movie', text='Movie ID')
            table.heading('id_location', text='Location ID')
            table.heading('movie_name', text='Movie Name')
            table.heading('location_name', text='Location Name')
            table.heading('city', text='City')

            self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                      database="cinema")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                                                SELECT id_screening FROM screenings
                                                """)
            results = [row[0] for row in self.cursor.fetchall()]
            self.connection.close()
            vector = []

            for x in results:
                d = Screening()
                d.load_screening(x)
                j = Movie()
                j.load_movie(d.id_movie)
                i = Location()
                i.load_location(d.id_location)
                vector.append(
                    (d.id_screening, d.start_time, d.ticket_price, d.id_movie, d.id_location, j.name, i.name, i.city))

            for x in vector:
                table.insert('', tk.END, values=x)

            table.grid(row=1, column=0, padx=10, pady=10)
            table.bind('<Motion>', 'break')

            label1 = customtkinter.CTkLabel(master=frame, text="Insert Row", font=("Roboto", 30))
            label1.grid(row=2, column=0, padx=45, pady=10)

            add_menu_display212 = customtkinter.CTkFrame(master=frame,
                                                         corner_radius=15,
                                                         height=1920,
                                                         width=1080)
            add_menu_display212.grid(pady=30, padx=30, sticky="nsew")
            table2 = ttk.Treeview(master=add_menu_display212,
                                  columns=columns2,
                                  height=0,
                                  selectmode='browse',
                                  show='headings')

            table2.column("#1", anchor="w", minwidth=120, width=120)
            table2.column("#2", anchor="c", minwidth=120, width=120)
            table2.column("#3", anchor="c", minwidth=100, width=100)
            table2.column("#4", anchor="c", minwidth=120, width=120)


            table2.heading('start_time', text='Start Time')
            table2.heading('ticket_price', text='Ticket Price')
            table2.heading('id_movie', text='Movie ID')
            table2.heading('id_location', text='Location ID')
            table2.grid(row=3, column=0, padx=10, pady=0)
            table2.bind('<Motion>', 'break')

            entry2 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Start Time")
            entry2.grid(row=4, column=0, padx=38, pady=10, sticky='w')
            entry3 = customtkinter.CTkEntry(master=frame, width=100, placeholder_text="Ticket Price")
            entry3.grid(row=4, column=0, padx=118, pady=10, sticky='w')
            entry4 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Movie ID")
            entry4.grid(row=4, column=0, padx=218, pady=10, sticky='w')
            entry5 = customtkinter.CTkEntry(master=frame, width=100, placeholder_text="Location ID")
            entry5.grid(row=4, column=0, padx=298, pady=10, sticky='w')

            entry_button = customtkinter.CTkButton(master=frame, width=100, height=26, text="Insert",
                                                   fg_color="#03AC13", hover_color="#5DBB63",
                                                   command=lambda: self.checkinsert2(frame, root, app, results,
                                                                                     entry2.get(),
                                                                                     entry3.get(), entry4.get(),
                                                                                     entry5.get()))
            entry_button.grid(row=5, column=0, padx=40, pady=15, sticky="w")

        back_img = customtkinter.CTkImage(Image.open("assets/backarrow.png"), size=(30, 30))
        back_button = customtkinter.CTkButton(master=frame, width=66, height=26, text="", image=back_img,
                                              fg_color="#FC8EAC", hover_color="#FC6C85",
                                              command=lambda: self.features(frame, root, app))
        back_button.grid(row=0, column=0, padx=45, pady=10, sticky="w")

        frame.grid(row=0, column=0, sticky="NESW")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        frame.pack(pady=20, padx=60, expand=True)


    def checkinsert(self, frame, root, app, results, e2, e3 ,e4, e5, e6, e7):
            if e2 != '' and e3 != '' and e4 != '' and e5 != '' and e6 != '' and e7 != '':
                d = Movie()
                d.name = e2
                d.length = e3
                d.director = e4
                d.rating = e5
                d.genre = e6
                d.launch_date = e7
                d.insert_movie()
                label1 = customtkinter.CTkLabel(master=frame, width=300, text="Row inserted",
                                                text_color='green', font=("Roboto", 16))
                label1.grid(row=5, column=0, padx=45, pady=10)
            else:
                label1 = customtkinter.CTkLabel(master=frame, width=300,
                                                text="You have to complet the blank spaces",
                                                text_color='red', font=("Roboto", 16))
                label1.grid(row=5, column=0, padx=45, pady=10)

    def checkinsert1(self, frame, root, app, results, e2, e3 ,e4, e5):
        if e2 != '' and e3 != '' and e4 != '' and e5 != '':
            d = Location()
            d.name = e2
            d.phone_number = e3
            d.city = e4
            d.adress = e5
            d.insert_location()
            label1 = customtkinter.CTkLabel(master=frame, width=300, text="Row inserted",
                                            text_color='green', font=("Roboto", 16))
            label1.grid(row=5, column=0, padx=45, pady=10)
        else:
            label1 = customtkinter.CTkLabel(master=frame, width=300,
                                            text="You have to complet the blank spaces",
                                            text_color='red', font=("Roboto", 16))
            label1.grid(row=5, column=0, padx=45, pady=10)


    def checkinsert2(self, frame, root, app, results, e2, e3 ,e4, e5):
        k=0

        self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                  database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                            SELECT id_movie FROM movies
                            """)
        results = [row[0] for row in self.cursor.fetchall()]
        self.connection.close()

        for x in results:
            if x == int(e4):
                k = k + 1
                break

        self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                  database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                            SELECT id_location FROM locations
                            """)
        results = [row[0] for row in self.cursor.fetchall()]
        self.connection.close()

        for x in results:
            if x == int(e5):
                k = k + 1
                break



        if k == 2:
            if e2 != '' and e3 != '' and e4 != '' and e5 != '':
                d = Screening()
                d.start_time = e2
                d.ticket_price = e3
                d.id_movie = e4
                d.id_location = e5
                d.insert_screening()
                label1 = customtkinter.CTkLabel(master=frame, width=300, text="Row inserted",
                                                text_color='green', font=("Roboto", 16))
                label1.grid(row=5, column=0, padx=45, pady=10)
            else:
                label1 = customtkinter.CTkLabel(master=frame, width=300,
                                                text="You have to complet the blank spaces",
                                                text_color='red', font=("Roboto", 16))
                label1.grid(row=5, column=0, padx=45, pady=10)
        else:
            label1 = customtkinter.CTkLabel(master=frame, width=300,
                                            text="You have to use existing Movie ID and Location ID",
                                            text_color='red', font=("Roboto", 16))
            label1.grid(row=5, column=0, padx=45, pady=10)


    def deletefromtabel(self, frame, root, app):
        frame.destroy()

        frame = customtkinter.CTkFrame(master=root)

        frame.grid(row=5, column=0, padx=15, pady=15)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Roboto", 14))
        style.configure("Treeview", font=("Roboto", 11))

        label = customtkinter.CTkLabel(master=frame, text=app, font=("Roboto", 30))
        label.grid(row=0, column=0, padx=45, pady=10)

        add_menu_display211 = customtkinter.CTkFrame(master=frame,
                                                     corner_radius=15,
                                                     height=1920,
                                                     width=1080)
        add_menu_display211.grid(pady=30, padx=30, sticky="nsew")

        if app == "Movies":
            columns = ('id_movie', 'name', 'length', 'director', 'rating', 'genre', 'launch_date')
            columns2 = ('id_movie')

            table = ttk.Treeview(master=add_menu_display211,
                                 columns=columns,
                                 selectmode='browse',
                                 show='headings')

            table.column("#1", anchor="c", minwidth=100, width=100)
            table.column("#2", anchor="w", minwidth=270, width=270)
            table.column("#3", anchor="c", minwidth=120, width=120)
            table.column("#4", anchor="c", minwidth=270, width=270)
            table.column("#5", anchor="c", minwidth=220, width=220)
            table.column("#6", anchor="c", minwidth=320, width=320)
            table.column("#7", anchor="c", minwidth=320, width=320)

            table.heading('id_movie', text='Movie ID')
            table.heading('name', text='Name')
            table.heading('length', text='Length')
            table.heading('director', text='Director')
            table.heading('rating', text='Rating')
            table.heading('genre', text='Genre')
            table.heading('launch_date', text='Launch Date')

            self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                      database="cinema")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                                                SELECT id_movie FROM movies
                                                """)
            results = [row[0] for row in self.cursor.fetchall()]
            self.connection.close()
            vector = []

            for x in results:
                d = Movie()
                d.load_movie(x)
                vector.append((d.id_movie, d.name, d.length, d.director, d.rating, d.genre, d.launch_date))

            for x in vector:
                table.insert('', tk.END, values=x)

            table.grid(row=1, column=0, padx=10, pady=10)
            table.bind('<Motion>', 'break')

            label1 = customtkinter.CTkLabel(master=frame, text="Delete Row", font=("Roboto", 30))
            label1.grid(row=2, column=0, padx=45, pady=10)

            add_menu_display212 = customtkinter.CTkFrame(master=frame,
                                                         corner_radius=15,
                                                         height=1920,
                                                         width=1080)
            add_menu_display212.grid(pady=30, padx=30, sticky="nsew")
            table2 = ttk.Treeview(master=add_menu_display212,
                                  columns=columns2,
                                  height=0,
                                  selectmode='browse',
                                  show='headings')
            table2.column("#1", anchor="c", minwidth=100, width=100)


            table2.heading('id_movie', text='Movie ID')
            table2.grid(row=3, column=0, padx=10, pady=0)
            table2.bind('<Motion>', 'break')

            entry1 = customtkinter.CTkEntry(master=frame, width=80, placeholder_text="Movie ID")
            entry1.grid(row=4, column=0, padx=38, pady=10, sticky='w')

            entry_button = customtkinter.CTkButton(master=frame, width=100, height=26, text="Delete",
                                                  fg_color="#C80815", hover_color="#FF0800",
                                                  command=lambda: self.checkdelete(frame, root, app, results, entry1.get()))
            entry_button.grid(row=5, column=0, padx=40, pady=15, sticky="w")




        if app == "Locations":
            columns = ('id_location', 'name', 'phone_number', 'city', 'adress')
            columns2 = ('id_location')

            table = ttk.Treeview(master=add_menu_display211,
                                 columns=columns,
                                 selectmode='browse',
                                 show='headings')

            table.column("#1", anchor="c", minwidth=150, width=100)
            table.column("#2", anchor="w", minwidth=270, width=270)
            table.column("#3", anchor="c", minwidth=180, width=180)
            table.column("#4", anchor="c", minwidth=170, width=170)
            table.column("#5", anchor="c", minwidth=790, width=790)

            table.heading('id_location', text='Location ID')
            table.heading('name', text='Name')
            table.heading('phone_number', text='Phone Number')
            table.heading('city', text='City')
            table.heading('adress', text='Adress')

            self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                      database="cinema")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                                        SELECT id_location FROM locations
                                        """)
            results = [row[0] for row in self.cursor.fetchall()]
            self.connection.close()
            vector = []

            for x in results:
                d = Location()
                d.load_location(x)
                vector.append((d.id_location, d.name, d.phone_number, d.city, d.adress))

            for x in vector:
                table.insert('', tk.END, values=x)

            table.grid(row=1, column=0, padx=10, pady=10)
            table.bind('<Motion>', 'break')

            label1 = customtkinter.CTkLabel(master=frame, text="Delete Row", font=("Roboto", 30))
            label1.grid(row=2, column=0, padx=45, pady=10)

            add_menu_display212 = customtkinter.CTkFrame(master=frame,
                                                         corner_radius=15,
                                                         height=1920,
                                                         width=1080)
            add_menu_display212.grid(pady=30, padx=30, sticky="nsew")
            table2 = ttk.Treeview(master=add_menu_display212,
                                  columns=columns2,
                                  height=0,
                                  selectmode='browse',
                                  show='headings')
            table2.column("#1", anchor="c", minwidth=120, width=120)

            table2.heading('id_location', text='Location ID')
            table2.grid(row=3, column=0, padx=10, pady=0)
            table2.bind('<Motion>', 'break')

            entry1 = customtkinter.CTkEntry(master=frame, width=100, placeholder_text="Location ID")
            entry1.grid(row=4, column=0, padx=38, pady=10, sticky='w')


            entry_button = customtkinter.CTkButton(master=frame, width=100, height=26, text="Delete",
                                                   fg_color="#C80815", hover_color="#FF0800",
                                                   command=lambda: self.checkdelete1(frame, root, app, results,
                                                                                    entry1.get()))
            entry_button.grid(row=5, column=0, padx=40, pady=15, sticky="w")


        if app == "Screenings":
            columns = (
            'id_screening', 'start_time', 'ticket_price', 'id_movie', 'id_location', "movie_name", "location_name",
            "city")
            columns2 = ('id_screening')

            table = ttk.Treeview(master=add_menu_display211,
                                 columns=columns,
                                 selectmode='browse',
                                 show='headings')

            table.column("#1", anchor="c", minwidth=150, width=100)
            table.column("#2", anchor="c", minwidth=170, width=170)
            table.column("#3", anchor="c", minwidth=150, width=150)
            table.column("#4", anchor="c", minwidth=130, width=130)
            table.column("#5", anchor="c", minwidth=130, width=130)
            table.column("#6", anchor="w", minwidth=350, width=350)
            table.column("#7", anchor="w", minwidth=350, width=350)
            table.column("#8", anchor="c", minwidth=220, width=220)

            table.heading('id_screening', text='Screening ID')
            table.heading('start_time', text='Start Time')
            table.heading('ticket_price', text='Ticket Price')
            table.heading('id_movie', text='Movie ID')
            table.heading('id_location', text='Location ID')
            table.heading('movie_name', text='Movie Name')
            table.heading('location_name', text='Location Name')
            table.heading('city', text='City')

            self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                      database="cinema")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                                        SELECT id_screening FROM screenings
                                        """)
            results = [row[0] for row in self.cursor.fetchall()]
            self.connection.close()
            vector = []

            for x in results:
                d = Screening()
                d.load_screening(x)
                j = Movie()
                j.load_movie(d.id_movie)
                i = Location()
                i.load_location(d.id_location)
                vector.append(
                    (d.id_screening, d.start_time, d.ticket_price, d.id_movie, d.id_location, j.name, i.name, i.city))

            for x in vector:
                table.insert('', tk.END, values=x)

            table.grid(row=1, column=0, padx=10, pady=10)
            table.bind('<Motion>', 'break')

            label1 = customtkinter.CTkLabel(master=frame, text="Delete Row", font=("Roboto", 30))
            label1.grid(row=2, column=0, padx=45, pady=10)

            add_menu_display212 = customtkinter.CTkFrame(master=frame,
                                                         corner_radius=15,
                                                         height=1920,
                                                         width=1080)
            add_menu_display212.grid(pady=30, padx=30, sticky="nsew")
            table2 = ttk.Treeview(master=add_menu_display212,
                                  columns=columns2,
                                  height=0,
                                  selectmode='browse',
                                  show='headings')
            table2.column("#1", anchor="c", minwidth=120, width=120)

            table2.heading('id_screening', text='Screening ID')
            table2.grid(row=3, column=0, padx=10, pady=0)
            table2.bind('<Motion>', 'break')

            entry1 = customtkinter.CTkEntry(master=frame, width=100, placeholder_text="Screening ID")
            entry1.grid(row=4, column=0, padx=38, pady=10, sticky='w')

            entry_button = customtkinter.CTkButton(master=frame, width=100, height=26, text="Delete",
                                                   fg_color="#C80815", hover_color="#FF0800",
                                                   command=lambda: self.checkdelete2(frame, root, app, results,
                                                                                     entry1.get()))
            entry_button.grid(row=5, column=0, padx=40, pady=15, sticky="w")

        back_img = customtkinter.CTkImage(Image.open("assets/backarrow.png"), size=(30, 30))
        back_button = customtkinter.CTkButton(master=frame, width=66, height=26, text="", image=back_img,
                                              fg_color="#FC8EAC", hover_color="#FC6C85",
                                              command=lambda: self.features(frame, root, app))
        back_button.grid(row=0, column=0, padx=45, pady=10, sticky="w")

        frame.grid(row=0, column=0, sticky="NESW")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        frame.pack(pady=20, padx=60, expand=True)

    def checkdelete(self, frame, root, app, results, e1):
        k = 0
        self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                  database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                            SELECT id_movie FROM movies
                            """)
        results = [row[0] for row in self.cursor.fetchall()]
        self.connection.close()

        for x in results:
            if x == int(e1):
                k = 1
                break

        if k == 1:
            d = Movie()
            d.delete_movie(e1)
            label1 = customtkinter.CTkLabel(master=frame, width=300, text="Row deleted",
                                            text_color='green', font=("Roboto", 16))
            label1.grid(row=5, column=0, padx=45, pady=10)
        else:
            label1 = customtkinter.CTkLabel(master=frame, width=300,
                                            text="ID doesn't exist",
                                            text_color='red', font=("Roboto", 16))
            label1.grid(row=5, column=0, padx=45, pady=10)


    def checkdelete1(self, frame, root, app, results, e1):
        k = 0
        self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                  database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                            SELECT id_location FROM locations
                            """)
        results = [row[0] for row in self.cursor.fetchall()]
        self.connection.close()

        for x in results:
            if x == int(e1):
                k = 1
                break

        if k == 1:
            d = Location()
            d.delete_location(e1)
            label1 = customtkinter.CTkLabel(master=frame, width=300, text="Row deleted",
                                            text_color='green', font=("Roboto", 16))
            label1.grid(row=5, column=0, padx=45, pady=10)
        else:
            label1 = customtkinter.CTkLabel(master=frame, width=300,
                                            text="ID doesn't exist",
                                            text_color='red', font=("Roboto", 16))
            label1.grid(row=5, column=0, padx=45, pady=10)


    def checkdelete2(self, frame, root, app, results, e1):
        k = 0
        self.connection = mysql.connector.connect(host="localhost", user="root", passwd="a2mEfc@#uo%*cQ",
                                                  database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                            SELECT id_screening FROM screenings
                            """)
        results = [row[0] for row in self.cursor.fetchall()]
        self.connection.close()

        for x in results:
            if x == int(e1):
                k = 1
                break

        if k == 1:
            d = Screening()
            d.delete_screening(e1)
            label1 = customtkinter.CTkLabel(master=frame, width=300, text="Row deleted",
                                            text_color='green', font=("Roboto", 16))
            label1.grid(row=5, column=0, padx=45, pady=10)
        else:
            label1 = customtkinter.CTkLabel(master=frame, width=300,
                                            text="ID doesn't exist",
                                            text_color='red', font=("Roboto", 16))
            label1.grid(row=5, column=0, padx=45, pady=10)



class Movie:

    def __init__(self, id_movie=0, name="", length="", director="",rating="", genre="", launch_date=""):
        self.id_movie = id_movie
        self.name = name
        self.length = length
        self.director = director
        self.rating = rating
        self.genre = genre
        self.launch_date = launch_date



    def load_movie(self, id_movie):
        self.connection = mysql.connector.connect(host="localhost",user="root",passwd="a2mEfc@#uo%*cQ",database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        SELECT * FROM movies
        WHERE id_movie = {}
        """.format(id_movie))

        results = self.cursor.fetchone()

        self.id_movie = id_movie
        self.name = results[1]
        self.length = results[2]
        self.director = results[3]
        self.rating = results[4]
        self.genre = results[5]
        self.launch_date = results[6]

        self.connection.close()

    def insert_movie(self):
        self.connection = mysql.connector.connect(host="localhost",user="root",passwd="a2mEfc@#uo%*cQ",database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        INSERT INTO movies(name,length,director,rating,genre,launch_date) 
        VALUES('{}','{}','{}','{}','{}','{}')
        """.format(self.name, self.length,self.director,self.rating,self.genre,self.launch_date))

        self.connection.commit()
        self.connection.close()

    def update_movie(self):
        self.connection = mysql.connector.connect(host="localhost",user="root",passwd="a2mEfc@#uo%*cQ",database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        UPDATE movies SET name = '{}', length = '{}',director = '{}',rating = '{}',genre = '{}',launch_date = '{}' WHERE id_movie = {}
        """.format(self.name, self.length,self.director,self.rating,self.genre,self.launch_date,self.id_movie))

        self.connection.commit()
        self.connection.close()

    def delete_movie(self, id_movie):
        self.connection = mysql.connector.connect(host="localhost",user="root",passwd="a2mEfc@#uo%*cQ",database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        DELETE FROM movies WHERE id_movie = {}
        """.format(id_movie))

        self.connection.commit()
        self.connection.close()


class Location:

    def __init__(self, id_location=0, name="", phone_number="", city="",adress=""):
        self.id_location = id_location
        self.name = name
        self.phone_number = phone_number
        self.city = city
        self.adress = adress



    def load_location(self, id_location):
        self.connection = mysql.connector.connect(host="localhost",user="root",passwd="a2mEfc@#uo%*cQ",database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        SELECT * FROM locations
        WHERE id_location = {}
        """.format(id_location))

        results = self.cursor.fetchone()

        self.id_location = id_location
        self.name = results[1]
        self.phone_number = results[2]
        self.city = results[3]
        self.adress = results[4]


        self.connection.close()

    def insert_location(self):
        self.connection = mysql.connector.connect(host="localhost",user="root",passwd="a2mEfc@#uo%*cQ",database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        INSERT INTO locations VALUES(name,phone_number,city,adress)
        ('{}','{}','{}','{}')
        """.format(self.name, self.phone_number,self.city,self.adress))

        self.connection.commit()
        self.connection.close()

    def update_location(self):
        self.connection = mysql.connector.connect(host="localhost",user="root",passwd="a2mEfc@#uo%*cQ",database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        UPDATE locations SET name = '{}',phone_number = '{}',city = '{}',adress = '{}' WHERE id_location = {}
        """.format(self.name,self.phone_number,self.city,self.adress,self.id_location))

        self.connection.commit()
        self.connection.close()

    def delete_location(self, id_location):
        self.connection = mysql.connector.connect(host="localhost",user="root",passwd="a2mEfc@#uo%*cQ",database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        DELETE FROM locations WHERE id_location = {}
        """.format(id_location))

        self.connection.commit()
        self.connection.close()


class Screening:

    def __init__(self, id_screening=0, start_time="", ticket_price=0, id_movie=0, id_location=0):
        self.id_screening = id_screening
        self.start_time = start_time
        self.ticket_price = ticket_price
        self.id_movie = id_movie
        self.id_location = id_location



    def load_screening(self, id_screening):
        self.connection = mysql.connector.connect(host="localhost",user="root",passwd="a2mEfc@#uo%*cQ",database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        SELECT * FROM screenings
        WHERE id_screening = {}
        """.format(id_screening))

        results = self.cursor.fetchone()

        self.id_screening = id_screening
        self.start_time = results[1]
        self.ticket_price = results[2]
        self.id_movie = results[3]
        self.id_location = results[4]

        self.connection.close()

    def insert_screening(self):
        self.connection = mysql.connector.connect(host="localhost",user="root",passwd="a2mEfc@#uo%*cQ",database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        INSERT INTO screenings(start_time,ticket_price,id_movie,id_location) VALUES('{}',{},{},{})
        """.format(self.start_time, self.ticket_price,self.id_movie,self.id_location))

        self.connection.commit()
        self.connection.close()

    def update_screening(self):
        self.connection = mysql.connector.connect(host="localhost",user="root",passwd="a2mEfc@#uo%*cQ",database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        UPDATE screenings SET start_time = '{}',ticket_price = {},id_movie = {},id_location = {} WHERE id_screening = {}
        """.format(self.start_time,self.ticket_price,self.id_movie,self.id_location,self.id_screening))

        self.connection.commit()
        self.connection.close()

    def delete_screening(self, id_screening):
        self.connection = mysql.connector.connect(host="localhost",user="root",passwd="a2mEfc@#uo%*cQ",database="cinema")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        DELETE FROM screenings WHERE id_screening = {}
        """.format(id_screening))

        self.connection.commit()
        self.connection.close()




MAIN = Aplicatie()
MAIN.start()
