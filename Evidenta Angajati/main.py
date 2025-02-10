from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
from datetime import datetime

class App(Tk):
	def __init__(self):
		super().__init__()
		self.title("Fereastra Principala")
		self.geometry("400x400")
		# se afiseaza pe fereastra chenarul(frame-ul) invizibil care contine widget-urile create mai jos
		self.start = Start(self)
		# se ruleaza fereastra
		self.mainloop()

class Start(Frame):
	def __init__(self, start):
		super().__init__(start)
		self.pack()
		self.etichete_fereastra_principala()

	@staticmethod
	def etichete_fereastra_principala():
		# se creaza etichetele
		lbl_titlu = Label(text="Ce vrei sa faci?")
		btn_adauga_angajat = Button(text="Adauga angajat", command=lambda :AdaugaAngajat(), bg="#8ef595", width=15)
		btn_afiseaza_angajati = Button(text="Afiseaza angajati", command= AfiseazaAngajati, bg="#8ef595", width=15)
		btn_modifica_angajat = Button(text="Modifica angajat", command=lambda: ModificaAngajat(), bg="#c0c0c0", width=15)
		btn_sterge_angajat = Button(text="Sterge angajat", command=lambda: StergeAngajat(),  bg="#8ef595", width=15)
		btn_iesire_aplicatie = Button(text="Iesire aplicatie",command=quit, bg="#8ef595", width=15)

		# se plaseaza pe ecran
		lbl_titlu.pack(pady=5)
		btn_adauga_angajat.pack(pady=5)
		btn_afiseaza_angajati.pack(pady=5)
		btn_modifica_angajat.pack(pady=5)
		btn_sterge_angajat.pack(pady=5)
		btn_iesire_aplicatie.pack(pady=5)

class AdaugaAngajat(Tk):
	def __init__(self):
		super().__init__()
		self.title("Adauga Angajat")
		self.geometry("700x400")

		self.menu = Adauga(self)
		self.mainloop()

class Adauga(Frame):
	def __init__(self, adauga):
		super().__init__(adauga)
		self.lbl_id_liber = None
		self.entry_id = None
		self.entry_first_name = None
		self.entry_last_name = None
		self.entry_date_of_employment = None
		self.entry_salary = None
		self.entry_department = None
		self.entry_city = None
		self.entry_county = None
		self.entry_district = None
		self.entry_street = None
		self.entry_street_number = None
		self.entry_block = None
		self.entry_block_scale = None
		self.entry_floor = None
		self.entry_apartment = None
		self.lbl_raspuns = None
		self.btn_save = None
		self.btn_quit = None
		self.pack()
		self.etichete_adauga()
		self.aplica_date = None
		self.dictionar_date = None
		self.dictionar_adresa = None

	def cauta_angajat(self):
		return self.cauta_id_liber()

	@staticmethod
	def cauta_id_liber():
		try:
			with open("angajati_cu_dic.json", "r") as file:
				existing_data = json.load(file)
			if existing_data:
				largest_key = max(existing_data.keys(), key=int)
				next_id = int(largest_key) + 1
			else:
				next_id = 1
			return next_id

		except (ValueError, FileNotFoundError, json.JSONDecodeError):
			return 1

	def quit(self):
		self.master.destroy()

	def aduna_datele(self):
		if not self.entry_first_name.get() or not self.entry_last_name.get():
			messagebox.showinfo("Eroare", "Numele si prenumele sunt obligatorii!")
			return
		try:
			float(self.entry_salary.get())
		except ValueError:
			messagebox.showinfo("Eroare", "Salariul trebuie sa fie un numar!")
			return

		try:
			datetime.strptime(self.entry_date_of_employment.get(), "%d.%m.%Y")  # initial %Y-%m-%d
		except ValueError:
			messagebox.showinfo("Eroare", "Data angajari trebuie sa fie in format DD.MM.YYYY!")
			return

		angajat = Angajat(self.entry_first_name.get(), self.entry_last_name.get(),
						  self.entry_date_of_employment.get(), self.entry_salary.get(), self.entry_department.get(),
						  self.entry_city.get())

		address = Address(self.entry_county.get(), self.entry_district.get(),
						  self.entry_street.get(), self.entry_street_number.get(), self.entry_block.get(),
						  self.entry_block_scale.get(), self.entry_floor.get(), self.entry_apartment.get())

		# se instatiaza clasa Address, Angajat
		angajat_data = angajat.transforma_date_angajat_in_dict()
		address_data = address.transforma_adresa_in_dict()

		angajat_data["address"] = address_data
		data_to_save = angajat_data
		print(angajat_data)

		try:
			with open("angajati_cu_dic.json", "r") as file:
				existing_data = json.load(file)
		except (FileNotFoundError, json.JSONDecodeError):
			existing_data = {}

		next_id = str(self.cauta_angajat())
		existing_data[next_id] = data_to_save

		with open("angajati_cu_dic.json", "w") as file:
			# noinspection PyTypeChecker
			json.dump(existing_data, file, indent=4)

		messagebox.showinfo("Felicitari", "Datele au fost salvate cu succes!")
		self.btn_save.destroy()

	def etichete_adauga(self):
		# se creaza etichetele si se afiseaza widget-urile
		self.lbl_id_liber = Label(self, text=f"Urmatoarea pozitie libera este: {self.cauta_angajat()}", width=30)
		self.lbl_id_liber.grid(row=0, column=1, padx=5, pady=5, columnspan=3)

		self.entry_id = Entry(self, width=10)
		self.entry_id.grid(row=1, column=2, padx=5, pady=5)

		lbl_first_name = Label(self, text="Nume")
		lbl_first_name.grid(row=2, column=0, padx=5, pady=5)

		lbl_last_name = Label(self, text="Prenume")
		lbl_last_name.grid(row=2, column=1, padx=5, pady=5)

		lbl_date_of_employment = Label(self, text="Data angajari")
		lbl_date_of_employment.grid(row=2, column=2, padx=5, pady=5)

		lbl_salary = Label(self, text="Salariul")
		lbl_salary.grid(row=2, column=3, padx=5, pady=5)

		lbl_department = Label(self, text="Departamentul")
		lbl_department.grid(row=2, column=4, padx=5, pady=5)

		self.entry_first_name = Entry(self)
		self.entry_first_name.grid(row=3, column=0, padx=5, pady=5)

		self.entry_last_name = Entry(self)
		self.entry_last_name.grid(row=3, column=1, padx=5, pady=5)

		self.entry_date_of_employment = Entry(self)
		self.entry_date_of_employment.grid(row=3, column=2, padx=5, pady=5)

		self.entry_salary = Entry(self)
		self.entry_salary.grid(row=3, column=3, padx=5, pady=5)

		self.entry_department = Entry(self)
		self.entry_department.grid(row=3, column=4, padx=5, pady=5)

		lbl_address = Label(self, text="Adresa de domiciliu: ")
		lbl_address.grid(row=4, column=2, padx=5, pady=5)

		lbl_city = Label(self, text="Oras")
		lbl_city.grid(row=5, column=0, padx=5, pady=5)

		lbl_county = Label(self, text="Judet")
		lbl_county.grid(row=5, column=1, padx=5, pady=5)

		lbl_district = Label(self, text="Sector")
		lbl_district.grid(row=5, column=2, padx=5, pady=5)

		lbl_street = Label(self, text="Strada")
		lbl_street.grid(row=5, column=3, padx=5, pady=5)

		lbl_number = Label(self, text="Numar")
		lbl_number.grid(row=5, column=4, padx=5, pady=5)

		self.entry_city = Entry(self)
		self.entry_city.grid(row=6, column=0, padx=5, pady=5)

		self.entry_county = Entry(self)
		self.entry_county.grid(row=6, column=1, padx=5, pady=5)

		self.entry_district = Entry(self)
		self.entry_district.grid(row=6, column=2, padx=5, pady=5)

		self.entry_street = Entry(self)
		self.entry_street.grid(row=6, column=3, padx=5, pady=5)

		self.entry_street_number = Entry(self)
		self.entry_street_number.grid(row=6, column=4, padx=5, pady=5)

		lbl_block = Label(self, text="Bloc")
		lbl_block.grid(row=7, column=0, padx=5, pady=5)

		lbl_block_scale = Label(self, text="Scara")
		lbl_block_scale.grid(row=7, column=1, padx=5, pady=5)

		lbl_floor = Label(self, text="Etaj")
		lbl_floor.grid(row=7, column=2, padx=5, pady=5)

		lbl_apartment = Label(self, text="Apartament")
		lbl_apartment.grid(row=7, column=3, padx=5, pady=5)

		self.entry_block = Entry(self)
		self.entry_block.grid(row=8, column=0, padx=5, pady=5)

		self.entry_block_scale = Entry(self)
		self.entry_block_scale.grid(row=8, column=1, padx=5, pady=5)

		self.entry_floor = Entry(self)
		self.entry_floor.grid(row=8, column=2, padx=5, pady=5)

		self.entry_apartment = Entry(self)
		self.entry_apartment.grid(row=8, column=3, padx=5, pady=5)

		self.btn_save = Button(self, text="  Salveaza  ", command=lambda: self.aduna_datele(), bg="#8ef595")
		self.btn_save.grid(row=9, column=2, padx=5, pady=5)

		self.btn_quit = Button(self, text="  Renunta  ", command=self.quit, bg="#8ef595")
		self.btn_quit.grid(row=10, column=2, padx=5, pady=5)

class Angajat:
	def __init__(self, first_name, last_name, date_of_employment, salary, department, city):
		self.first_name = first_name
		self.last_name = last_name
		self.date_of_employment = date_of_employment
		self.salary = salary
		self.department = department
		self.city = city

	def transforma_date_angajat_in_dict(self):
		dictionar_date = {"first_name": self.first_name, "last_name": self.last_name,
							   "date_of_employment": self.date_of_employment,
							   "salary": self.salary,
							   "department": self.department, "city": self.city}
		return dictionar_date

class Address:
	def __init__(self, county, district, street, street_number, block, block_scale, floor, apartment):
		self.county = county
		self.district = district
		self.street = street
		self.street_number = street_number
		self.block = block
		self.block_scale = block_scale
		self.floor = floor
		self.apartment = apartment

	def transforma_adresa_in_dict(self):
		dictionar_adresa = dict({"county": self.county, "district": self.district,
								 "street": self.street, "street_number": self.street_number, "block": self.block,
								 "block_scale": self.block_scale, "floor": self.floor, "apartment": self.apartment})
		return dictionar_adresa


class AfiseazaAngajati(Tk):
	def __init__(self):
		super().__init__()
		self.title("Afiseaza Angajati")
		self.geometry("575x400")
		self.menu = Afiseaza(self)
		self.mainloop()

class Afiseaza(Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		self.entry_first_name = None
		self.entry_last_name = None
		self.entry_city = None
		self.treeview_frame = None
		self.btn_search = None
		self.btn_exit = None
		self.pack()
		self.etichete_afiseaza()

	def quit(self):
		self.master.destroy()

	def take_first_name(self):
		return self.entry_first_name.get()

	def take_last_name(self):
		return self.entry_last_name.get()

	def take_city(self):
		return self.entry_city.get()

	def search_by_criteria(self):
		first_name = self.take_first_name()
		last_name = self.take_last_name()
		city = self.take_city()
		self.treeview_frame.clear_treeview()

		try:
			with open("angajati_cu_dic.json", "r") as file:
				lista_angajati = json.load(file)
				found = False  # Flag to track if we found any matching employee


				# messagebox.showinfo("Informare", "Daca nu se introduce un criteriu de cautare \n"
				#                                  " o sa se afiseaza toate inregistrarile.")

				for id_unic, values in lista_angajati.items():
					# Match first name, last name, and city (case-insensitive)
					if (first_name.lower() in values.get("first_name", "").lower()) and \
							(last_name.lower() in values.get("last_name", "").lower()) and \
							(city.lower() in values.get("city", "").lower()):
						self.treeview_frame.insert_employee(id_unic, values)
						found = True

				if not found:
					messagebox.showinfo("Eroare", "Nu s-au gasit angajati cu acest criteriu.")
					self.treeview_frame.insert_employee("Nu s-au gasit angajati cu acest criteriu.")
		except Exception as e:
			print(f"Error: {e}")

	def etichete_afiseaza(self):
		lbl_title = Label(self, text="Introdu criteriul de cautare al angajatului:")
		lbl_title.grid(row=0, column=0, padx=5, pady=5, columnspan=4)

		lbl_first_name = Label(self, text="Nume")
		lbl_first_name.grid(row=1, column=0, padx=5, pady=5)

		lbl_last_name = Label(self, text="Prenume")
		lbl_last_name.grid(row=1, column=1, padx=5, pady=5)

		lbl_city = Label(self, text="Oraș")
		lbl_city.grid(row=1, column=2, padx=5, pady=5)

		self.entry_first_name = Entry(self)
		self.entry_first_name.grid(row=2, column=0, padx=5, pady=5)

		self.entry_last_name = Entry(self)
		self.entry_last_name.grid(row=2, column=1, padx=5, pady=5)

		self.entry_city = Entry(self)
		self.entry_city.grid(row=2, column=2, padx=5, pady=5)

		self.btn_search = Button(self, text="  Cauta  ", bg="#8ef595", command=lambda: self.search_by_criteria())
		self.btn_search.grid(row=0, column=3, padx=5, pady=5)

		self.treeview_frame = TreeviewFrame(self)
		self.treeview_frame.grid(row=4, column=0, padx=5, pady=5, columnspan=4)

		self.btn_exit = Button(self, text="  Iesire  ", bg="#8ef595", command= self.quit)
		self.btn_exit.grid(row=6, column=3, padx=5, pady=5)

class TreeviewFrame(Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.treeview = None
		self.create_treeview()

	def create_treeview(self):
		columns = ("id", "first_name", "last_name", "date_of_employment", "salary", "city")
		self.treeview = ttk.Treeview(self, columns=columns, show='headings')
		self.treeview.heading("id", text="ID-unic")
		self.treeview.heading("first_name", text="Nume")
		self.treeview.heading("last_name", text="Prenume")
		self.treeview.heading("date_of_employment", text="Data angajări")
		self.treeview.heading("salary", text="Salariul")
		self.treeview.heading("city", text="Orașul")

		vertical_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
		vertical_scrollbar.pack(side="right", fill="x")

		self.treeview.column("id", width=50, anchor="center")
		self.treeview.column("first_name", width=100, anchor="center")
		self.treeview.column("last_name", width=140, anchor="center")
		self.treeview.column("date_of_employment", width=80,anchor="center")
		self.treeview.column("salary", width=70,anchor="center")
		self.treeview.column("city", width=110,anchor="center")

		self.treeview.pack(fill=BOTH, expand=True)

	def insert_employee(self, id_unic, values):
		# If no match is found, we insert a message instead of employee data
		if isinstance(values, dict):
			self.treeview.insert("", "end", values=(
				id_unic,
				values.get("first_name", ""),
				values.get("last_name", ""),
				values.get("date_of_employment", ""),
				values.get("salary", ""),
				values.get("city", "")
			))
		else:
			# If no match found, we insert the error message into the treeview
			self.treeview.insert("", "end", values=(values,))

	def clear_treeview(self):
		# Clear the Treeview before inserting new results
		for row in self.treeview.get_children():
			self.treeview.delete(row)

class ModificaAngajat:
	pass

class StergeAngajat(Tk):
	def __init__(self):
		super().__init__()
		self.title("Sterge Angajat")
		self.geometry("600x600")
		self.menu = AfiseazaSterge(self)
		self.mainloop()

class AfiseazaSterge(Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		self.entry_id = None
		self.result_label = None
		self.pack()
		self.sterge_widget()

	def exit(self):
		self.master.quit()

	def sterge_widget(self):
		lbl_title = Label(self, text="Introdu ID-ul unic al angajatului:")
		lbl_title.grid(row=0, column=0, padx=5, pady=5)

		self.entry_id = Entry(self, width=15)
		self.entry_id.grid(row=1, column=0, padx=5, pady=5)

		btn_sterge = Button(self, text="  Sterge  ", bg="#8ef595", command=self.sterge_angajat)
		btn_sterge.grid(row=3, column=0, padx=5, pady=5)

		btn_quit = Button(self, text="  Iesire  ", bg="#8ef595", command=self.exit)
		btn_quit.grid(row=4, column=0, padx=5, pady=5)

	def sterge_angajat(self):
		angajat_id = self.entry_id.get()
		if not angajat_id:
			messagebox.showerror("Eroare", "ID-ul nu poate fi gol.")
			return
		Functii.cauta_angajat_dupa_id(angajat_id)

class Functii:
	@staticmethod
	def open_file():
		with open("angajati_cu_dic.json", "r") as file:
			lista_angajati = json.load(file)
		return lista_angajati

	@staticmethod
	def write_file(lista_noua):
		with open("angajati_cu_dic.json", "w") as file:
			# noinspection PyTypeChecker
			json.dump(lista_noua, file, indent=4)

	@staticmethod
	def cauta_angajat_dupa_id(id_unic):
		lista = Functii.open_file()

		if id_unic in lista:
			employee_data = lista[id_unic]
			confirm = messagebox.askquestion(
				"Confirmare",
				f"Se va sterge ID-ul {id_unic}, care contine: \n{employee_data}.\n Esti sigur?"
			)
			if confirm == 'yes':
				del lista[id_unic]
				Functii.write_file(lista)
				messagebox.showinfo("Succes", f"Angajatul cu ID-ul {id_unic} a fost sters.")
			else:
				messagebox.showinfo("Anulare", f"Angajatul cu ID-ul {id_unic}, NU va fi sters.")
		else:
			messagebox.showinfo("Eroare!", f"Angajatul cu ID-ul {id_unic}, nu a fost gasit")

App()