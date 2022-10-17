from datetime import datetime

today = datetime( datetime.now().year, datetime.now().month, datetime.now().day)
birthday = datetime( 2013, 4, 3 ) 
birthday = datetime( 1986, 1, 15 ) 
birthday = datetime( 2016, 7, 27 ) 
birthday = datetime( 1983, 3, 30 ) 
this_year_bday = datetime( today.year, birthday.month, birthday.day)
next_year_bday = datetime( today.year + 1, birthday.month, birthday.day)
if today > this_year_bday:
    thebday = next_year_bday
else:
    thebday = this_year_bday

age_int = int((thebday - birthday).days / 365.2425)
age_round = round((thebday - birthday).days / 365.2425)
age_days = (thebday - birthday).days / 365.2425
#calculate days to bday
days_to_birthday = (thebday - today).days

print(today)
print(birthday)
print(thebday)
print(days_to_birthday)
print(age_int)
print(age_round)
print(age_days)

def calc_easter(year):
        #find easter for 'year'
        y = year
        a = y // 100
        b = y % 100
        c = (3 * (a + 25)) // 4
        d = (3 * (a + 25)) % 4
        e = (8 * (a + 11)) // 25
        f = (5 * a + b) % 19
        g = (19 * f + c - e) % 30
        h = (f + 11 * g) // 319
        j = (60 * (5 - d) + b) // 4
        k = (60 * (5 - d) + b) % 4
        m = (2 * j - k - g + h) % 7
        n = (g - h + m + 114) // 31
        p = (g - h + m + 114) % 31
        dy = p + 1
        mth = n
        easter = datetime(y, mth, dy)
        return easter

next_easter = calc_easter(2022)
print(next_easter)
