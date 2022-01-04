# Light Portfolio Tracker

This is a Portfolio Tracker where users can add their stock positions. Including the Company (by Ticker), Volume of stocks and Average Price/Open Price. It features a refresh function allowing users to see up to date data on P&L.

Screenshot of Light Portfolio Tracker
![Screenshot](/snip.jpg?raw=true "Light Portfolio Tracker: Screenshot (Windows)")

Known Issues:

#1	Requires Tix (used for tool tips) which is deprecated. Causes issues when attempting to run compiled on Windows or as a script on Mac. As a result only runs as a script on Windows. RESOLVED. Replaced Tix with Pmw.

#2	Users are able to enter invalid strings in the “volume” entry field. Adding validation is a work in progress.

#3	The data is stored in an SQLite3 database and is displayed using Tkinter’s Treeview. Column headings can be used to sort on the Ticker and Company columns but doing so on the numerical data headings doesn’t sort as expected. Possibly due to integers being stored or displayed as strings.

Enjoy real good!
