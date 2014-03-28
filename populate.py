import os
import csv
import sqlite3
import datetime

conn = sqlite3.connect('subscriptions.db')
c = conn.cursor()

# CSVs containing addresses + subscription information.
address_tables = ('Vidalia.csv', 'Lyons.csv', 'Out304.csv', 'Outco.csv')
# Containing PO Box No., City Code, Select Code, Walk Seq, Tag.
po_tables = ('LPOBoxes.csv', 'VPOBoxes.csv')
# Containing Address, Sort Code, and City RTE.
code_tables = ('Soperton.csv', 'VC12345.csv')
# Containing Addresses, Walk Seq, and City Code.
lc12 = 'LC12.csv'

def mk_int(s):
    """int() function that returns a 0 if given an empty string instead of throwing an exception."""
    s = s.strip()
    return int(s) if s else 0

"""Takes a CSV table, starts the primary keys at n, and populates the database from it."""
def populate_starting_at(table, n=1):
        with open(table, 'rb') as f:
            plotlist = csv.reader(f, delimiter=',')
            plotlist.next()
            plotlist.next()
            for i, line in enumerate(plotlist):
                if i % 2 == 0:
                    id = i + n
                    first = line[0]
                    last = line[1]
                    address = line[2]
                    po_box = line[3]
                    rural_box = line[4]
                    city = line[5]
                    state = line[6]
                    zip = line[7]
                    phone = line[10]
                    email = ''
            
            # Handling dates.
                    if line[16] == '':
                        start_date = datetime.date(1950, 1, 1) 
                    else:
                        try:
                            start_date = datetime.datetime.strptime(line[16], "%m/%d/%Y").date()
                        except ValueError:
                            start_date = datetime.date(1950, 1, 1) 
                            
                    if line[9] == '':
                        end_date = datetime.date(1950, 1, 1) 
                    else:
                        try:
                            end_date = datetime.datetime.strptime(line[9], "%y-%m-%d").date()
                        except ValueError:
                            end_date = datetime.date(1950, 1, 1) 

                    sort_code = mk_int(line[11])
                    walk_sequence = mk_int(line[12])
                    city_code = line[13]
                    zone = line[14]
                    level = line[15]
                    # renewal_date = line[16]
                    advance = True
                    clipper = False
            
                    record = (id, first, last, address, po_box, rural_box, city, state, zip, start_date, end_date, phone, email, sort_code, walk_sequence, city_code, zone, level, advance, clipper)
                    
                    print record
                    c.execute("INSERT INTO subscriptions (id, First_Name, Last_Name, Address, PO_Box, Rural_Box, City, State, ZIP, Start_Date, End_Date, Phone, Email, Sort_Code, Walk_Sequence, City_Code, Zone, Level, Advance, Clipper) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", record)

# Each n value is the number of entries already in the database + 1.
populate_starting_at('Vidalia.csv', 1)
populate_starting_at('Lyons.csv', 1777)
populate_starting_at('Out304.csv', 2282)
populate_starting_at('Outco.csv', 2625)

                    
conn.commit()
conn.close()
