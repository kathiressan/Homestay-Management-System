from Tkinter import *
import tkMessageBox
import sqlite3
import calendar
import datetime
import time

db = sqlite3.connect('homestayDatabase.db')
cursor = db.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute(''' CREATE TABLE IF NOT EXISTS USERS (	loginID text,
														loginPW text,
														userID integer PRIMARY KEY AUTOINCREMENT,
														userName text,
														userGender text,
														userContact text,
														userEmail text,
														userAddress text,
														userType text
														) ''')
cursor.execute('''	CREATE TABLE IF NOT EXISTS HOMESTAY(	homeID integer PRIMARY KEY AUTOINCREMENT,
															userID integer,
															homeAddress text,
															homeCity text,
															homeState text,
															homePrice float,
															homeDesc text,
															roomAmount integer,
															bathroomAmount integer,
															hasWindows boolean,
															FOREIGN KEY (userID) REFERENCES USERS(userID)
															) ''')

cursor.execute('''	CREATE TABLE IF NOT EXISTS BOOKING(	bookID integer PRIMARY KEY AUTOINCREMENT,
														userID integer,
														homeID integer,
														bookStart date,
														bookEnd date,
														pricePerNight float,
														FOREIGN KEY (userID) REFERENCES USERS(userID)
														FOREIGN KEY (homeID) REFERENCES HOMESTAY(homeID)
														) ''')
cursor.execute('''	CREATE TABLE IF NOT EXISTS REVIEW(	reviewID integer PRIMARY KEY AUTOINCREMENT,
														userID integer,
														bookID integer,
														review text,
														stars float,
														FOREIGN KEY (userID) REFERENCES USERS(userID)
														FOREIGN KEY (bookID) REFERENCES BOOKING(bookID)
														) ''')


root = Tk()
root.geometry("700x450")

LoginFrame = Frame(root)
LoginFrame.pack()

RegisterFrame = Frame(root)

MainInterfaceFrame = Frame(root)

HomestayEntryFrame = Frame(root)

SearchFrame = Frame(root)

SearchListFrame = Frame(root)

BookingFrame = Frame(root)

ReviewFrame = Frame(root)

ReportGenerationFrame = Frame(root)

def LoginRegisterClicked():
    LoginFrame.pack_forget()
    RegisterFrame.pack()

def RegisterClicked():
    global InfoInput_1
    global InfoInput_2
    global InfoInput_3
    GetRegistrationName = InfoInput_1.get()
    GetRegistrationPass = InfoInput_2.get()
    GetRegistrationConfirmPass = InfoInput_3.get()
    if len(GetRegistrationName) <= 1 or len(GetRegistrationPass) <= 1 or GetRegistrationPass != GetRegistrationConfirmPass:
        tkMessageBox.showerror("Error", "Invalid Credentials Entered")
    else:
        cursor.execute('''INSERT INTO USERS(loginID, loginPW) VALUES(?,?)''',(GetRegistrationName, GetRegistrationPass))
        db.commit()
        tkMessageBox.showinfo("Success", "Registration Successful")
        InfoInput_1.delete(0, END)
        InfoInput_1.insert(0, "")
        InfoInput_2.delete(0, END)
        InfoInput_2.insert(0, "")
        InfoInput_3.delete(0, END)
        InfoInput_3.insert(0, "")
        RegisterFrame.pack_forget()
        LoginFrame.pack()

def fromRegToLogPage():
    RegisterFrame.pack_forget()
    LoginFrame.pack()

def mainInterface():
    LoginFrame.pack_forget()
    MainInterfaceFrame.pack()

def LoginCredentials():
    global entry_1
    global entry_2
    global getLoginName
    global getLoginPassword
    getLoginName = entry_1.get()
    getLoginPassword = entry_2.get()
    str(getLoginName)
    str(getLoginPassword)
    test = cursor.execute(''' SELECT loginPW FROM USERS WHERE loginID = ? ''', (getLoginName, )).fetchone()
    if test:
        checkPassword = test
        if getLoginPassword == checkPassword[0]:
            tkMessageBox.showinfo("Welcome", "Login Successful")
            time.sleep(0.5)
            mainInterface()
            entry_1.delete(0, END)
            entry_1.insert(0, "")
            entry_2.delete(0, END)
            entry_2.insert(0, "")
        else:
            tkMessageBox.showerror("Error", "Wrong Password")
    else:
        tkMessageBox.showerror("Error", "User does not exist. Please register first.")


def onClickSearchHomestay():
    MainInterfaceFrame.pack_forget()
    SearchFrame.pack()

def onClickListHomestay():
    MainInterfaceFrame.pack_forget()

def bookfunc(HOMEID):
    SearchListFrame.pack_forget()
    BookingFrame.pack()
    print(HOMEID)

def onClickSearch():
    SearchFrame.pack_forget()
    SearchListFrame.pack()
    global SearchStateEntry
    global SearchCityEntry
    global SearchPriceMinEntry
    global SearchPriceMaxEntry
    global state
    global city
    global minPrice
    global maxPrice

    state = SearchStateEntry.get()
    city = SearchCityEntry.get()
    Label(SearchListFrame, text="Number").grid(row=0, column=0)
    Label(SearchListFrame, text="Address").grid(row=0, column=1)
    Label(SearchListFrame, text="City").grid(row=0, column=2)
    Label(SearchListFrame, text="State").grid(row=0, column=3)
    Label(SearchListFrame, text="Price").grid(row=0, column=4)
    Label(SearchListFrame, text="Description").grid(row=0, column=5)
    Label(SearchListFrame, text="Number of rooms").grid(row=0, column=6)
    Label(SearchListFrame, text="Number of bathrooms").grid(row=0, column=7)
    Label(SearchListFrame, text="Windows Available").grid(row=0, column=8)
    Label(SearchListFrame, text="Click to book").grid(row=0, column=9)

    minPrice = float(SearchPriceMinEntry.get())
    maxPrice = float(SearchPriceMaxEntry.get())
    cursor.execute(''' SELECT * FROM HOMESTAY ''')
    row = cursor.fetchall()
    rowC = 1
    columnC = 0
    for rows in row:
        isTrue = True
        if (state != rows[4] or city != rows[3]):
            if(state != ""):
                if(state != rows[4]):
                    isTrue = False
            if(city != ""):
                if(city != rows[3]):
                    isTrue = False
        elif(minPrice != 0):
            if(rows[5] < minPrice):
                isTrue = False
            elif(rows[5] > maxPrice):
                isTrue = False
        if(isTrue == True):
            loopcounter = 0
            Label(SearchListFrame, text=rowC).grid(row=rowC, column=columnC)
            columnC = columnC + 1
            Label(SearchListFrame, text=rows[2]).grid(row=rowC, column=columnC)
            columnC = columnC + 1
            Label(SearchListFrame, text=rows[3]).grid(row=rowC, column=columnC)
            columnC = columnC + 1
            Label(SearchListFrame, text=rows[4]).grid(row=rowC, column=columnC)
            columnC = columnC + 1
            Label(SearchListFrame, text=rows[5]).grid(row=rowC, column=columnC)
            columnC = columnC + 1
            Label(SearchListFrame, text=rows[6]).grid(row=rowC, column=columnC)
            columnC = columnC + 1
            Label(SearchListFrame, text=rows[7]).grid(row=rowC, column=columnC)
            columnC = columnC + 1
            Label(SearchListFrame, text=rows[8]).grid(row=rowC, column=columnC)
            columnC = columnC + 1
            Label(SearchListFrame, text=rows[9]).grid(row=rowC, column=columnC)
            columnC = columnC + 1
            Button(SearchListFrame, text="Book", fg="blue", command=lambda: bookfunc(rows[0])).grid(row=rowC, column=columnC)
            columnC = columnC + 1
            rowC = rowC + 1

        columnC = 0


'''
LOGIN FRAME
'''
label_1 = Label(LoginFrame, text="Event Name: ")
label_2 = Label(LoginFrame, text="Date: ")
label_3 = Label(LoginFrame, text="Time: ").grid(row=4, column=0, sticky=E)
label_4 = Label(LoginFrame, text="Venue: ").grid(row=5, column=0, sticky=E)
label_3 = Label(LoginFrame, text="Occupancy: ").grid(row=6, column=0, sticky=E)
label_3 = Label(LoginFrame, text="Description: ").grid(row=7, column=0, sticky=E)
entry_1 = Entry(LoginFrame)
entry_2 = Entry(LoginFrame)
entry_1.focus_set()
entry_2.focus_set()
entry_3 = Entry(LoginFrame).grid(row=4, column=1)
entry_4 = Entry(LoginFrame).grid(row=5, column=1)
entry_5 = Entry(LoginFrame).grid(row=6, column=1)
entry_6 = Entry(LoginFrame).grid(row=7, column=1)
label_1.grid(row=1, column=0, sticky=E)
label_2.grid(row=2, column=0, sticky=E)

entry_1.grid(row=1, column=1)
entry_2.grid(row=2, column=1)

LoginButton = Button(LoginFrame, text="Create Event", fg="blue", command=LoginCredentials)
LoginButton.grid(row=8,columnspan=2)

RegisterButton = Button(LoginFrame, text="Back", fg="blue", command=LoginRegisterClicked)
RegisterButton.grid(row=9,columnspan=2)


'''
END LOGIN FRAME
'''

'''
Register Frame
'''
Info_1 = Label(RegisterFrame, text="Username")
Info_2 = Label(RegisterFrame, text="Password")
Info_3 = Label(RegisterFrame, text="Confirm Password")
dasd = Label(RegisterFrame, text="Account Type: ").grid(row=3, column=0, sticky=E)
TextRegister = Button(RegisterFrame, text="Register", fg="blue", command=RegisterClicked)
TextRegister.grid(row=4, columnspan=2)
RegFrameBackLogin = Button(RegisterFrame,text="Go back to login", fg="blue", command=fromRegToLogPage)
RegFrameBackLogin.grid(row=5, columnspan=2)
entry_3 = Entry(RegisterFrame).grid(row=3, column=1)
InfoInput_1 = Entry(RegisterFrame)
InfoInput_2 = Entry(RegisterFrame)
InfoInput_3 = Entry(RegisterFrame)
InfoInput_2.config(show='*')
InfoInput_3.config(show='*')
InfoInput_1.focus_set()
InfoInput_2.focus_set()
InfoInput_3.focus_set()

Info_1.grid(row=0, column=0, sticky=E)
Info_2.grid(row=1, column=0, sticky=E)
Info_3.grid(row=2, column=0, sticky=E)

InfoInput_1.grid(row=0, column=1)
InfoInput_2.grid(row=1, column=1)
InfoInput_3.grid(row=2, column=1)
'''
END REGISTER FRAME
'''

'''
MAIN INTERFACE FRAME
'''
searchHomestayButton = Button(MainInterfaceFrame, text="Search Homestay", command=onClickSearchHomestay, bg="blue", fg="white", activebackground="white", activeforeground="blue", font=('Verdana',15))
searchHomestayButton.pack(ipadx=9999, ipady=10)

listHomestayButton = Button(MainInterfaceFrame, text="List Homestay", command=onClickListHomestay, bg="red", fg="white", activebackground="white", activeforeground="red", font=('Verdana',15))
listHomestayButton.pack(ipadx=9999, ipady=10)

'''
END MAIN INTERFACE FRAME
'''

'''
HOMESTAY ENTRY FRAME
'''
HomestayLocation = Label(HomestayEntryFrame, text="Location: ")
HomestayPrice = Label(HomestayEntryFrame, text="Price per night: ")
HomestayDescription = Label(HomestayEntryFrame, text="Description: ")

LocationEntry = Entry(HomestayEntryFrame)
LocationEntry.focus_set()
PriceEntry = Entry(HomestayEntryFrame)
PriceEntry.focus_set()
DescriptionEntry = Entry(HomestayEntryFrame)
DescriptionEntry.focus_set()

HomestayLocation.grid(row=0, column=0, sticky=E)
HomestayPrice.grid(row=1, column=0, sticky=E)
HomestayDescription.grid(row=2, column=0, sticky=E)

LocationEntry.grid(row=0, column=1)
PriceEntry.grid(row=1, column=1)
DescriptionEntry.grid(row=2, column=1)

EntryButton = Button(HomestayEntryFrame,text="Publish Homestay", fg="blue")
EntryButton.grid(row=3, columnspan=2)


'''
END HOMESTAY ENTRY FRAME
'''



'''
SEARCH FRAME
'''

Search = Label(SearchFrame, text="Search for your desired homestay", font=('Verdana',20))

SearchState = Label(SearchFrame, text="Enter State: ")
SearchCity = Label(SearchFrame, text="Enter City: ")
SearchPriceMin = Label(SearchFrame, text="Minimum Price: ")
SearchPriceMax = Label(SearchFrame, text="Maximum Price: ")

stateV = StringVar()
cityV = StringVar()

SearchStateEntry = Entry(SearchFrame, textvariable=stateV)
SearchStateEntry.focus_set()
SearchCityEntry = Entry(SearchFrame, textvariable=cityV)
SearchCityEntry.focus_set()
minV = IntVar()
maxV = IntVar()
SearchPriceMinEntry = Entry(SearchFrame, textvariable=minV)
SearchPriceMinEntry.focus_set()
SearchPriceMaxEntry = Entry(SearchFrame, textvariable=maxV)
SearchPriceMaxEntry.focus_set()

Search.grid(row=0, columnspan=2)

SearchState.grid(row=1, column=0, sticky=E)
SearchCity.grid(row=2, column=0, sticky=E)
SearchPriceMin.grid(row=3, column=0, sticky=E)
SearchPriceMax.grid(row=4, column=0, sticky=E)

SearchStateEntry.grid(row=1, column=1, sticky=W)
SearchCityEntry.grid(row=2, column=1, sticky=W)
SearchPriceMinEntry.grid(row=3, column=1, sticky=W)
SearchPriceMaxEntry.grid(row=4, column=1, sticky=W)

SearchButton = Button(SearchFrame, text="Search", fg="blue", command=onClickSearch)
SearchButton.grid(row=5, columnspan=2)


'''
END SEARCH FRAME
'''


'''
BOOKING FRAME
'''
BookingDescriptionText = Label(BookingFrame, text="Booking Description: ")
BookingDescription = Label(BookingFrame, text="Description of Homestay goes here")
BookingPayment = Label(BookingFrame, text="Choose payment method: ")

BookingDescriptionText.grid(row=1, column=0, sticky=E)
BookingPayment.grid(row=2, column=0, sticky=E)

x = IntVar()
y = IntVar()

Radiobutton(BookingFrame, text="Debit/Credit", variable=x, value=1).grid(row=2, column=1)
Radiobutton(BookingFrame, text="Online Banking", variable=y, value=1).grid(row=2, column=2)

BookingDescription.grid(row=1, column=1, sticky=W)

BookNow = Button(BookingFrame, text="Book", fg="blue")
BookNow.grid(row=3, columnspan=3)
'''
END BOOKING FRAME
'''
root.mainloop()