
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
from os import system
import calendar
import datetime






pencere = Tk()
pencere.title("Beyzanın Kur Hesaplayıcısı")
pencere.geometry("500x500")
pencere.resizable(width=False, height=False)










messagebox.showinfo("Message", "Coded By Mertoğlu")


def show_calendar(currency):
    # Takvim penceresini oluşturun
    calendar_window = Toplevel(pencere)
    calendar_window.title("Takvim")

    # Takvim bileşenini oluşturun
    cal = calendar.Calendar()

    # Bugünkü tarihi alın
    today = datetime.date.today()

    # Ay ve yıl seçimini yapmak için combobox bileşenini oluşturun
    month_combo = ttk.Combobox(calendar_window, values=calendar.month_name[1:], state="readonly")
    month_combo.current(today.month - 1)
    month_combo.pack()

    year_combo = ttk.Combobox(calendar_window, values=list(range(1900, today.year + 1)), state="readonly")
    year_combo.current(today.year - 1900)
    year_combo.pack()

    # Takvimi güncellemek için fonksiyon oluşturun
    def update_calendar():
        selected_month = month_combo.current() + 1
        selected_year = int(year_combo.get())

        frame = Frame(calendar_window, padx=10, pady=10)
        frame.pack()

        # Ay ismini ve yılı gösteren etiketi oluşturun
        month_label = Label(frame, text=calendar.month_name[selected_month] + " " + str(selected_year), font="bold 14")
        month_label.grid(row=0, column=0, columnspan=7, pady=10)

        # Hafta günlerini gösteren etiketleri oluşturun
        weekdays = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
        for i, day in enumerate(weekdays):
            label = Label(frame, text=day, font="bold 12")
            label.grid(row=1, column=i, padx=5, pady=5)

        # Takvimdeki günleri gösterin
        for week_index, week in enumerate(cal.monthdayscalendar(selected_year, selected_month)):
            for day_index, day in enumerate(week):
                if day == 0:
                    label = Label(frame, width=4)
                else:
                    label = Label(frame, width=4, text=str(day), relief="solid")
                    label.bind("<Button-1>", lambda e, selected_day=day: select_date(selected_day, selected_month, selected_year, currency))

                if day == today.day and selected_month == today.month and selected_year == today.year:
                    label.configure(bg="lightblue")
                label.grid(row=week_index+2, column=day_index, padx=5, pady=5)

    update_button = ttk.Button(calendar_window, text="Güncelle", command=update_calendar)
    update_button.pack()

    update_calendar()


def select_date(day, selected_month, selected_year, currency):
    messagebox.showinfo("Seçilen Tarih", f"Tarih: {day}/{selected_month}/{selected_year}")

    # Kur değerlerini almak için web scraping yapın
    url = f"https://www.bloomberght.com/doviz/{selected_year}-{selected_month:02d}-{day:02d}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        if currency == "USD":
            kur_element = soup.find("span", class_="value up")
            if kur_element:
                kur = kur_element.text.strip()
                dolar.delete(0, END)
                dolar.insert(END, kur)
            else:
                messagebox.showinfo("Hata", "USD değeri bulunamadı.")
        elif currency == "gram-altin":
            kur_element = soup.find("td", string="Gram Altın")
            if kur_element:
                kur = kur_element.find_next_sibling("td").text.strip()
                g_altın.delete(0, END)
                g_altın.insert(END, kur)
            else:
                messagebox.showinfo("Hata", "Gram Altın değeri bulunamadı.")
        elif currency == "EUR":
            kur_element = soup.find("td", string="Euro")
            if kur_element:
                kur = kur_element.find_next_sibling("td").text.strip()
                euro.delete(0, END)
                euro.insert(END, kur)
            else:
                messagebox.showinfo("Hata", "EUR değeri bulunamadı.")
        elif currency == "GBP":
            kur_element = soup.find("td", string="Sterlin")
            if kur_element:
                kur = kur_element.find_next_sibling("td").text.strip()
                sterlın.delete(0, END)
                sterlın.insert(END, kur)
            else:
                messagebox.showinfo("Hata", "GBP değeri bulunamadı.")
    except:
        messagebox.showinfo("Hata", f"{currency} değeri alınamadı.")
def hesapla_kur():
    try:
        #system("calc.exe")
        url = requests.get("https://www.doviz.com/").content
        soup = BeautifulSoup(url, "html.parser")
        kur1 = soup.find("span", attrs={"data-socket-key": "USD"})
        kur2 = soup.find("span", attrs={"data-socket-key": "gram-altin"})
        kur3 = soup.find("span", attrs={"data-socket-key": "EUR"})
        kur4 = soup.find("span", attrs={"data-socket-key": "GBP"})
        kur5 = soup.find("span", attrs={"data-socket-key": "XU100"})
        kur6 = soup.find("span", attrs={"data-socket-key": "bitcoin"})
        kur7 = soup.find("span", attrs={"data-socket-key": "gumus"})
        kur8 = soup.find("span", attrs={"data-socket-key": "TAHVIL"})
        #########Dolar#############
        dolar.delete(0, END)
        dolar.insert(END, kur1.text)
        ###########Gram_altın###########
        g_altın.delete(0, END)
        g_altın.insert(END, kur2.text)
        ############Euro#############
        euro.delete(0, END)
        euro.insert(END, kur3.text)
        ############Sterlın################
        sterlın.delete(0, END)
        sterlın.insert(END, kur4.text)


    except:
        messagebox.showinfo("Message", "Bir Hata Oluştur?")


def exıt():
    try:
        pencere.destroy()
    except:
        messagebox.showinfo("Message", "Pencereyi Kapatırken Bir Hata Oluştur?")


def clear():
    try:
        dolar.delete(0, END)
        g_altın.delete(0, END)
        euro.delete(0, END)
        sterlın.delete(0, END)

    except:
        messagebox.showinfo("Message", "Boşluklar Temizlenirken Bir Hata Oluştur?")


welcome = Label(pencere, text="Kur Hesaplayıcıya Hoş Geldin", font="bold 20", bg="lightblue", padx=10, pady=10)
welcome.pack()

frame = Frame(pencere)
frame.pack(pady=10)

label1 = Label(frame, text="USD:", font="bold 16")
label1.grid(row=0, column=0, padx=5, pady=5)

dolar = Entry(frame, width=10, font="bold 16")
dolar.grid(row=0, column=1, padx=5, pady=5)

label2 = Label(frame, text="GOLD:", font="bold 16")
label2.grid(row=1, column=0, padx=5, pady=5)

g_altın = Entry(frame, width=10, font="bold 16")
g_altın.grid(row=1, column=1, padx=5, pady=5)

label3 = Label(frame, text="EUR:", font="bold 16")
label3.grid(row=2, column=0, padx=5, pady=5)

euro = Entry(frame, width=10, font="bold 16")
euro.grid(row=2, column=1, padx=5, pady=5)

label4 = Label(frame, text="GBP:", font="bold 16")
label4.grid(row=3, column=0, padx=5, pady=5)

sterlın = Entry(frame, width=10, font="bold 16")
sterlın.grid(row=3, column=1, padx=5, pady=5)

button_frame = Frame(pencere)
button_frame.pack(pady=10)

hesapla = ttk.Button(button_frame, text="Hesapla", command=hesapla_kur)
hesapla.grid(row=0, column=0, padx=5, pady=5)

temızle = ttk.Button(button_frame, text="Temizle", command=clear)
temızle.grid(row=0, column=1, padx=5, pady=5)

usd_calendar_button = ttk.Button(button_frame, text="USD Takvimi Göster", command=lambda: show_calendar("USD"))
usd_calendar_button.grid(row=1, column=0, padx=5, pady=5)

gold_calendar_button = ttk.Button(button_frame, text="GOLD Takvimi Göster", command=lambda: show_calendar("gram-altin"))
gold_calendar_button.grid(row=1, column=1, padx=5, pady=5)

eur_calendar_button = ttk.Button(button_frame, text="EUR Takvimi Göster", command=lambda: show_calendar("EUR"))
eur_calendar_button.grid(row=2, column=0, padx=5, pady=5)

gbp_calendar_button = ttk.Button(button_frame, text="GBP Takvimi Göster", command=lambda: show_calendar("GBP"))
gbp_calendar_button.grid(row=2, column=1, padx=5, pady=5)








mainloop()