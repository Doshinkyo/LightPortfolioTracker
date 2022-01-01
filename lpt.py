# # # # # # # # # # # # # #
# Import Required Modules #
# # # # # # # # # # # # # #
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkhtmlview import HTMLLabel
from pathlib import Path
import sqlite3
import yfinance as yf
import time
from datetime import datetime
from tkinter import font
from tkinter import *
from tkinter.tix import *

# # # # # # # # # # # # # # #
# Application's Main Window #
# # # # # # # # # # # # # # #
window = Tk()
window.title("Light Portfolio Tracker")
window.iconbitmap("lpt_icon.ico")
window.geometry("780x620")

default_font = font.nametofont("TkDefaultFont")
default_font.configure(family="Segoe UI", size=8, weight=font.BOLD)

tip = Balloon(window)
tip.config(bg="#757575", bd=2)
tip.label.config(bg="#757575", fg="#757575", bd=2)
for index,sub in enumerate (tip.subwidgets_all()) :
    if index > 0:
        sub.configure(bg="white")

window.columnconfigure(0, weight=2)
window.columnconfigure(1, weight=9)
window.columnconfigure(2, weight=9)
window.columnconfigure(3, weight=9)
window.columnconfigure(4, weight=9)
window.columnconfigure(5, weight=1)

window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)
window.rowconfigure(4, weight=1)
window.rowconfigure(5, weight=1)
window.rowconfigure(6, weight=10)
window.rowconfigure(7, weight=10)
window.rowconfigure(8, weight=10)
window.rowconfigure(9, weight=10)
window.rowconfigure(10, weight=10)
window.rowconfigure(11, weight=10)
window.rowconfigure(12, weight=10)
window.rowconfigure(13, weight=10)
window.rowconfigure(14, weight=10)
window.rowconfigure(15, weight=2)

frame_0=tk.Frame(window, borderwidth=1, relief="ridge")
frame_1=tk.Frame(window, borderwidth=1, relief="ridge")
frame_2=tk.Frame(window, borderwidth=1, relief="ridge")
frame_3=tk.Frame(window, borderwidth=1, relief="ridge")
frame_4=tk.Frame(window, borderwidth=1)

frame_0.grid(row=0, rowspan=6, columnspan=6, sticky="NSEW", ipadx=5, padx=5, ipady=5) # Banner
frame_1.grid(row=6, rowspan=1, columnspan=6, sticky="NSEW", ipadx=5, padx=5, ipady=5) # Portfolio Headder
frame_2.grid(row=7,  column=0, rowspan=7, columnspan=6, sticky="NSEW", ipadx=5, padx=5, ipady=5) # Treeview
frame_2.columnconfigure(0, weight=1) # Treeview Frame Column
frame_3.grid(row=14, rowspan=2, columnspan=6, sticky="NSEW", ipadx=5, padx=5, ipady=5) # Portfolio Overview
frame_4.grid(row=16, rowspan=1, columnspan=6, sticky="NSEW", ipadx=5, padx=5, ipady=5) # Status Bar

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Connect To Or Create Database In Application Root Folder  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
portfolio_db=Path("light_portfolio_database.db")
if portfolio_db.is_file():
    print("Database Connection Successfull")
else:
    print("Database Connection Failed. File Not Located In Root Directory. Creating Database.")
    conn = sqlite3.connect("light_portfolio_database.db")
    c = conn.cursor()
    c.execute("""Create TABLE portfolio ( 
                    ticker text,
                    companyName text,
                    volume integer,
                    openPrice integer,
                    currentPrice integer,
                    change integer
                    )""")

# # # # # # # # # # # # # #
# Input Labels And Fields #
# # # # # # # # # # # # # #
pad_lbl=tk.Label(text=" ", justify="center")
pad_lbl.grid(row=0, column=0, rowspan=1, columnspan=6, sticky="W")

app_banner=tk.Label(text="Fill in fields below to add a position.", justify="center")
app_banner.grid(row=1, column=1, rowspan=1, columnspan=5, sticky="W")

ticker_lbl=tk.Label(text="Ticker :")
ticker_lbl.grid(row=2, column=0, rowspan=1, columnspan=1, padx=(15,5), ipadx=5, sticky="W")

ticker_entry=tk.Entry(text="")
ticker_entry.grid(row=2, column=1, rowspan=1, columnspan=3, sticky="WE")
ticker_entry.focus()

ticker_volume=tk.Label(text="Volume :")
ticker_volume.grid(row=3, column=0, rowspan=1, columnspan=1, padx=(15,5), ipadx=5, sticky="W")

ticker_volume_entry=tk.Entry(text="")
ticker_volume_entry.grid(row=3, column=1, rowspan=1, columnspan=3, sticky="WE")

open_price=tk.Label(text="Price :") 
open_price.grid(row=4, column=0, rowspan=1, columnspan=1, padx=(15,5), ipadx=5, sticky="W")

open_price_entry=tk.Entry(text="")
open_price_entry.grid(row=4, column=1, rowspan=1, columnspan=3, ipadx=5, ipady=1, pady=5, sticky="WE")

status_bar = tk.Label(text="Displaying Portfolio")
status_bar.grid(row=16, column=0, columnspan=6, sticky=tk.W + tk.N, ipadx=10, ipady=7)

ticker_volume=tk.Label(text="~ PORTFOLIO ~")
ticker_volume.grid(row=6, column=0, rowspan=1, columnspan=1, padx=(15,5), ipadx=5, sticky="W")

logo=HTMLLabel(height=1, width=15, html='<a style="font-size: 8px;color:black;text-decoration:none;text-align:right" href="http://ResonanceIT.co.uk">www.resonanceit.co.uk</a>')
logo.grid(row=16, column=5, rowspan=1, columnspan=1, sticky=tk.E + tk.N, ipadx=10, ipady=5)

# # # # # # # # # # # # # # # # # # # # # # # # #
# Connect To Database And Draw Portfolio Table  #
# # # # # # # # # # # # # # # # # # # # # # # # #
conn = sqlite3.connect("light_portfolio_database.db")
c = conn.cursor()
c.execute("SELECT *, oid FROM portfolio")
records =  c.fetchall()
row_count = c.execute("SELECT * FROM portfolio")
num_rows = len(row_count.fetchall())

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=default_font)

tv = ttk.Treeview(frame_2, columns=(0,1,2,4,5,6), show="headings", height=num_rows +1, padding=10)
tv.grid(row=4, column=0, rowspan=1, columnspan=1, padx=(5), ipadx=5, pady=5, sticky="NSEW")

tv.column(0,minwidth=0,width=110)
tv.column(1,minwidth=0,width=150)
tv.column(2,minwidth=0,width=110)
tv.column(4,minwidth=0,width=110)
tv.column(5,minwidth=0,width=110)
tv.column(6,minwidth=0,width=110)

tv.heading(0, text="TICKER", anchor="w")
tv.heading(1, text="COMPANY", anchor="w")
tv.heading(2, text="VOLUME", anchor="w")
tv.heading(4, text="PRICE @ OPEN", anchor="w")
tv.heading(5, text="CURRENT PRICE", anchor="w")
tv.heading(6, text="CHANGE", anchor="w")
for i in records:
        tv.insert("", "end", values=i)
conn.close()

# # # # # # # # # # # # #   ********* KNOWN ISSUE: ONLY WORKS AS DESIRED ON TICKER AND COMPANY COLUMNS AS INTEGERS ARE STORED AS STRINGS SO NOT SORTING PROPERLY *********
# Column Sort Function  #
# # # # # # # # # # # # #
def treeview_column_sort(tv, col, reverse):
    data = [
        (tv.set(iid, col), iid)
        for iid in tv.get_children("")
    ]

    data.sort(reverse=reverse)

    for index, (sort_val, iid) in enumerate(data):
        tv.move(iid, "", index)

    tv.heading(col, command=lambda _col=col: \
                 treeview_column_sort(tv, _col, not reverse))

columns = (0,1,2,3,4,5,6)

for col in columns:
    tv.heading(col, command=lambda _col=col: \
                     treeview_column_sort(tv, _col, False))

# # # # # # # # # # # # #
# Refresh The Portfolio #
# # # # # # # # # # # # #
def refresh_tree():
    children = tv.get_children()
    if children:
        tv.delete(*children)
    
    conn = sqlite3.connect("light_portfolio_database.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM portfolio")
    records =  c.fetchall()
    for i in records:
            tv.insert("", "end", values=i)
    
    global now
    now =str(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    row_count = c.execute("SELECT * FROM portfolio")
    num_rows = len(row_count.fetchall())
    tv.config(height=num_rows+1)
    
    conn.close()
    
    status_bar["text"] = ("Data Refreshed As Of: " + now)

# Run edit_row() and save_update() for each row in the tree view.

def market_data_refresh():
    conn = sqlite3.connect("light_portfolio_database.db")
    c = conn.cursor()
    # c.execute("SELECT * FROM portfolio")
    # results = c.fetchall
    
    for row in c.execute("SELECT *, oid FROM portfolio"):
        record=row
        mdr_ticker=(record[0]) # REQ
        mdr_open_price=(record[3]) # REQ
        mdr_oid=str(record[6]) # REQ
        mdr_stock=yf.Ticker(mdr_ticker)
        mdr_current_price = round(float(mdr_stock.info["regularMarketPrice"]), 2)
        mdr_diff = round((mdr_current_price / mdr_open_price - 1)*100, 2)
        mdr_string_diff=str(mdr_diff)
        mdr_change=(mdr_string_diff + "%")

        status_bar["text"] = "Refreshing Market Data..."
        window.update_idletasks()
        time.sleep(0.33) 


        c.execute("""UPDATE portfolio SET 
                    openPrice = :openPrice,
                    currentPrice = :currentPrice,
                    change = :change

                    WHERE oid=""" + mdr_oid,

                    {
                    "openPrice": mdr_open_price,
                    "currentPrice": mdr_current_price,
                    "change": mdr_change
                    })
    conn.commit()
    conn.close()
    refresh_tree()
    status_bar["text"] = ("Market Data Refreshed As Of: " + now)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# # # # # # # # # # # # # #
# Add Ticker To Portfolio #
# # # # # # # # # # # # # #
def addTicker():

    conn = sqlite3.connect("light_portfolio_database.db")
    c = conn.cursor()

    if not ticker_entry.get().strip():
        messagebox.showerror(title="Empty Field(s)", message="Fill in the Ticker, Price and Volume fields to add a stock to the portfolio!")
    elif not ticker_volume_entry.get().strip():
        messagebox.showerror(title="Empty Field(s)", message="Fill in the Ticker, Price and Volume fields to add a stock to the portfolio!")
    elif not open_price_entry.get().strip():
        messagebox.showerror(title="Empty Field(s)", message="Fill in the Ticker, Price and Volume fields to add a stock to the portfolio!")
    else:
        choice = str(ticker_entry.get())
        stock = yf.Ticker(choice)
        try: 
            oepf = float(open_price_entry.get())
        except ValueError:
            messagebox.showerror(title="Invalid Price", message="The price you paid (average price), must be a number.\nPlease try again.")
            return
        try: 
            short_name = stock.info["shortName"]
        except KeyError:
            messagebox.showerror(title="Invalid Ticker", message="Unable to locate that Ticker on Yahoo Finance. Please try again.")
            return
        try:
            current_price = round(float(stock.info["regularMarketPrice"]), 2)
        except TypeError:
            messagebox.showerror(title="Invalid Price", message="The price you paid (average price), must be a number.\nPlease try again.")
            return
        diff = round((current_price / oepf - 1)*100, 2)
        string_diff = str(diff)
        change = (string_diff + "%")

        status_bar["text"] = "Adding position to portfolio..."
        window.update_idletasks()
        time.sleep(0.9) 

        c.execute("INSERT INTO portfolio VALUES (:ticker, :companyName, :volume, :openPrice, :currentPrice, :change)", 
                    {
                        "ticker": ticker_entry.get(),
                        "companyName": short_name,
                        "volume": ticker_volume_entry.get(),
                        "openPrice": open_price_entry.get(),
                        "currentPrice": current_price,
                        "change": change
                    })

        conn.commit()
        refresh_tree()
        conn.close()

        ticker_entry.delete(0, tk.END)
        ticker_volume_entry.delete(0, tk.END)
        open_price_entry.delete(0, tk.END)
        ticker_entry.focus()
        status_bar["text"] = "The position was added to your portfolio."


# # # # # # # # # # # # # # # 
# Edit A Portfolio Position #
# # # # # # # # # # # # # # #
def edit_row():
    try:
        current_row = tv.selection()[0] # Used to check that a row is selected need to error handle multiple row selections / test handling of multiple rows.
        for item in tv.selection():
            
            global editor
            editor = Tk()
            editor.title("Update A Position")
            editor.geometry("274x190")
            
            ticker_editor = tv.item(item, "values")[0]
            volume_editor = tv.item(item, "values")[2]
            open_price_editor = tv.item(item, "values")[3]
            current_row_oid = tv.item(item, "values")[6]

            editor_frame=tk.Frame(editor, borderwidth=1, relief="ridge")
            editor_frame.grid(row=0, rowspan=7, columnspan=8, sticky="NSEW", ipadx=5, padx=5, ipady=5, pady=5)
            
            ticker_lbl_editor = tk.Label(editor_frame, text="Ticker")
            ticker_lbl_editor.grid(row=1, column=1, columnspan=1, padx=20, pady=10, sticky="W")
            ticker_entry_editor = tk.Entry(editor_frame, text="")
            ticker_entry_editor.grid(row=1, column=3, columnspan=1, padx=20, pady=10)
            ticker_entry_editor.insert(0, ticker_editor)

            volume_ldl_editor = tk.Label(editor_frame, text="Volume")
            volume_ldl_editor.grid(row=2, column=1, columnspan=1, padx=20, pady=10, sticky="W")
            volume_entry_editor = tk.Entry(editor_frame, text="")
            volume_entry_editor.grid(row=2, column=3, columnspan=1, padx=20, pady=10)
            volume_entry_editor.focus()
            volume_entry_editor.insert(0, volume_editor)

            open_price_lbl_editor = tk.Label(editor_frame, text="Price")
            open_price_lbl_editor.grid(row=3, column=1, columnspan=1, padx=20, pady=10, sticky="W")
            open_price_entry_editor = tk.Entry(editor_frame, text="")
            open_price_entry_editor.grid(row=3, column=3, columnspan=1, padx=20, pady=10)
            open_price_entry_editor.insert(0, open_price_editor)

            def save_update():
                conn = sqlite3.connect("light_portfolio_database.db")
                c = conn.cursor()

                choice_editor=str(ticker_entry_editor.get())
                stock_editor=yf.Ticker(choice_editor)
                ope_editor_float=float(open_price_entry_editor.get())
                short_name_editor=stock_editor.info["shortName"]
                current_price_editor=round(float(stock_editor.info["regularMarketPrice"]), 2)
                diff_editor=round((current_price_editor / ope_editor_float -1)*100, 2)
                string_diff_editor=str(diff_editor)
                change_editor=(string_diff_editor + "%")

                status_bar["text"] = "Updating portfolio..."
                window.update_idletasks()
                time.sleep(0.33) 

                c.execute("""UPDATE portfolio SET 
                            ticker = :ticker,
                            companyName = :companyName,
                            volume = :volume,
                            openPrice = :openPrice,
                            currentPrice = :currentPrice,
                            change = :change
                                                        
                            WHERE oid=""" + current_row_oid,
                            {
                                "ticker": choice_editor,
                                "companyName": short_name_editor,
                                "volume": volume_entry_editor.get(),
                                "openPrice": open_price_entry_editor.get(),
                                "currentPrice": current_price_editor,
                                "change": change_editor
                            })

                conn.commit()
                conn.close()
                refresh_tree()
                status_bar["text"] = "Position updated."
                editor.destroy()

            commit_edit = tk.Button(editor_frame, borderwidth=1, relief="ridge", text="SAVE", bg="#DBDBDB", command=save_update)
            commit_edit.grid(row=6, column=0, columnspan=7, padx=20, pady=10, sticky="EW")

    except IndexError:
        messagebox.showerror(title="No Selection", message="Select a row in your portfolio to edit!")

# # # # # # # # # # # # # # # # # #
# Delete A Ticker From Portfolio  #
# # # # # # # # # # # # # # # # # #
def delete_row():
    try:
        current_row = tv.selection()[0]
        for item in tv.selection():
            current_row_oid = tv.item(item, "values")[6]
            current_row_ticker = tv.item(item, "values")[0]
            current_row_volume = tv.item(item, "values")[2]
            tv.delete(current_row)
            conn = sqlite3.connect("light_portfolio_database.db")
            c = conn.cursor()
            c.execute("DELETE from portfolio WHERE oid=" + current_row_oid)
            conn.commit()
            window.update_idletasks()
            refresh_tree()
            status_bar["text"] = "Deleted " + current_row_ticker + " from portfolio. Number of shares was: " + current_row_volume
            conn.close()
    except IndexError:
        messagebox.showerror(title="No Selection", message="Select a row in your portfolio for deletion!")
    
# # # # # # # # # # # # # # # # #
# Database Manipulation Buttons #
# # # # # # # # # # # # # # # # #
add_btn = tk.Button(borderwidth=1, relief="ridge", text="Add Position", command=addTicker, bg="#DBDBDB", width=16, height=0)
add_btn.grid(row=2, column=4, columnspan=1, sticky=tk.E, padx=20, ipadx=3, ipady=3)
tip.bind_widget(add_btn, balloonmsg="Add the stock Ticker, Volume\nand Open Price to Portfolio.\n ") # Deprecated and should not be used!

ref_btn = tk.Button(borderwidth=1, relief="ridge", text="Refresh Data", command=market_data_refresh, bg="#DBDBDB", width=16, height=0)
ref_btn.grid(row=3, column=4, columnspan=1, sticky=tk.E, padx=20, ipadx=3, ipady=3)
tip.bind_widget(ref_btn, balloonmsg="Refresh the Portfolio with up to date\nprice data from Yahoo Finance\n ") # Deprecated and should not be used!

edt_btn = tk.Button(borderwidth=1, relief="ridge", text="Edit Selected", command=edit_row, bg="#DBDBDB", width=16, height=0)
edt_btn.grid(row=4, column=4, columnspan=1, sticky=tk.E, padx=20, ipadx=3, ipady=3)
tip.bind_widget(edt_btn, balloonmsg="Edit a selected row\nin the Portfolio.\n ") # Deprecated and should not be used!

del_btn = tk.Button(borderwidth=1, relief="ridge", text="Delete Selected", command=delete_row, bg="#DBDBDB", width=16, height=0)
del_btn.grid(row=2, column=5, columnspan=1, sticky=tk.E, padx=20, ipadx=3, ipady=3)
tip.bind_widget(del_btn, balloonmsg="Delete the selected row\nfrom the Portfolio.\n ") # Deprecated and should not be used!

# # # # # # # # # # # # # # # # # # # 
# Add Ticker When Enter Key Pressed #
# # # # # # # # # # # # # # # # # # #
def return_add(event):
    status_bar["text"] = "Adding Stock To Portfolio"
    addTicker()
window.bind('<Return>', return_add)

# # # # # # # # # # #  **************** WORK IN PROGRESS ************
# Portfolio Summary #
# # # # # # # # # # #
# currency_summary = "3498"
# percentage_summary = int(45)
# if percentage_summary >=0:
#     up_down_cond = "increased"
# else:
#     up_down_cond = "decreased"
# currency_summary_str = str(currency_summary)
# percentage_summary_str = str(percentage_summary)
# up_down_cond_str = str(up_down_cond)

# summary_lbl=tk.Label(text="Your portfolio has " + up_down_cond_str +  " by $" + currency_summary_str + " (" + percentage_summary_str + "%)", justify="center")
# summary_lbl.grid(row=13, column=1, rowspan=4, columnspan=4, sticky="WE")

# # # # # # # # #
# Confirm Close # Currently disabled, to enable remove rem's
# # # # # # # # #
# def on_closing():
#     if messagebox.askokcancel("Quit", "Do you want to quit?"):
#         window.destroy()
#         editor.destroy()
# window.protocol("WM_DELETE_WINDOW", on_closing)

# # # # # # # # # # # # 
# End Of Application  #
# # # # # # # # # # # # 
window.mainloop()
