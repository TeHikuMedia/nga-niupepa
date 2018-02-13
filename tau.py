from taumahi import clean_whitespace
import re
import csv

# This module is designed to replace forms of numbers, specifically those appear in nzdl's archive of Māori newspapers with appropriate te reo text.
# Numbers from other sources may incur errors, or have the function break early.

def hōputu_tau(tau):
    # Converts numerals into Māori words for numbers up to 100 billion.
    # The input is a string of numerals, periods and commas
    # The output is a string of Māori words

    # Dictionary for each numeral and its associated number, aside from 0 which is usually omitted except for when it is the only numeral
    tau_kupu = {'1': 'kotahi', '2': 'rua', '3': 'toru', '4': 'whā',
                '5': 'rima', '6': 'ono', '7': 'whitu', '8': 'waru',
                '9': 'iwa', '10': 'tekau', '100': 'rau'}

    # Sets up the string where the numerals' text will be stored
    reo = ""
    # Sets up the 10s carryover variable
    mā = False

    # Removes any commas or periods, with the intention of being left with a string of numbers
    kupu = re.sub(r'[ \./,\'‘’\"]', '', tau)

    # If there are any other characters in the string apart from those mentioned in the function's beginning,
    if re.search(r'[^0-9]', kupu):
        # the function will break.
        return kupu
    # Retrieves the length of the string, which is important in determining which 'place' (100s, 10s or 1s) each digit is in.
    hauroa = len(kupu)
    # Loops through each index in the numeral string
    for i in range(hauroa):
        # The numeral '0' is never written, and is treated very differently from other digits. The tests for the digit 0 are hence separated.
        if kupu[i] == '0':
            # If there was a non-zero digit in the previous position, which would be a 10s position if this test is activated,
            if mā:
                # then nothing needs to be written, as the current digit is 0. So it is reverted back to False.
                mā = False
            # If the last thing written was in the number dictionary (i.e. not an order of magnitude from kaha_kaituhituhi), and it is in the 1s position,
            if reo and reo.split()[-1] in tau_kupu.values() and (hauroa - i) % 3 == 1:
                # then an order of magnitude needs to be written
                reo += kaha_kaituhituhi(hauroa, i)
        # If the digit is non-zero,
        else:
            # This will be activated when the current digit is in the 1s position, after a non-zero 10s digit.
            if mā:
                # Since there is also a non-zero digit in the 1s position, it will write "mā", which is used to connect 10s and 1s.
                reo += "mā "
                # The variable is then reverted to False, so that it is only activated in the 1s position after it has been set to True.
                mā = False

            # If there is a 1 in the 10s position, nothing will be written
            if kupu[i] == '1' and (hauroa - i) % 3 == 2:
                pass
            # If there is a 1 in the last position, 'tahi' will be written. Otherwise, 1 is 'kotahi' as in the dictionary.
            elif kupu[i] == '1' and i == (hauroa - 1):
                reo += "tahi"
            # If the previous conditions are not satisfied, then the corresponding word for the digit (stored in the dictionary) is written
            else:
                reo += tau_kupu[kupu[i]]

            # The 100s, 10s and 1s positions loop in cycles of 3.
            # The function determines which position it is by taking the modulo of the difference between the index and string length upon division by 3.
            # 0 = 100s, 1 = 10s, 2 = 1s.

            # If there is a non-zero digit in the 100s position, the word for 'hundred' is written.
            if (hauroa - i) % 3 == 0:
                reo += " rau "
            # If there is a non-zero digit in the 10s position, the word for 'ten' is written. Multiples of 10 are written as the digit multiplier followed by 10.
            elif (hauroa - i) % 3 == 2:
                reo += " tekau "
                # The 10 carryover variable is activated if a 10 is written
                mā = True
            # If there is a non-zero digit in the 1s position, it is passed to the order of magnitude function to determine whether a placeholder needs to be written
            elif (hauroa - i) % 3 == 1:
                reo += kaha_kaituhituhi(hauroa, i)

    # If all the digits were 0, nothing would be written, and the empty string would evaluate as False.
    if reo:
        # Fixes excess whitespace and commas on the end, returns the number's words.
        return clean_whitespace(reo).strip(',')
    else:
        # If all digits were 0, it returns the word for 0.
        return 'kore'


def kaha_kaituhituhi(hauroa, i):
    # This function takes the string length and index position from the hōputu_tau function.
    # It determines whether an order of magnitude needs to be written, as the cycles of 100s, 10s and 1s positions enters into thousands, millions, etc.
    # The output is a string to be appended to the string from hōputu_tau

    # The quotient of the division between the string length and the index number in the 1s position (when (hauroa - i) % 3 == 1)
    # Tells us whether it is in the thousands group, millions, or billions, if it is 1, 2 or 3 respectively. If it is 0, it is below the thousands group, and nothing needs to be written
    if (hauroa - i) // 3 == 1:
        kupu = " mano, "
    elif (hauroa - i) // 3 == 2:
        kupu = " miriona, "
    elif (hauroa - i) // 3 == 3:
        kupu = " piriona, "
    else:
        kupu = ""

    return kupu


def pakaru_moni(tui):
    # This function takes numeral strings with commas in them, whether monetary values or otherwise, and returns the appropriate words.
    # The characters in the string must only be numerals, commas, full stops and the pound symbol as the first character or otherwise not present,
    # or else the function will break. If there are any more than 2 instances of ',,', the 'pene' variable will be erroneous

    # Sets up the variable that determines whether the figure is in pounds or not
    moni = False
    # Sets up the variables where pounds, shillings and pence will be stored, if they exist.
    pāuna, herengi, pene = "", "", ""

    # Remove commas or anything that might have been used as commas
    tau = re.sub(r'[\'‘’"/\.,] ?', '', re.sub(r'[.,]{2}', 'p', tui))

    # If there is a pound symbol, 'pāuna moni' needs to be written.
    if tau[0] == '£' or 'l' in tau:
        # £ variable activated
        moni = True

        # The £ symbol is removed so the string may be processed by the hōputu_kupu function
        if tau[0] == '£':
            tau = tau[1:]

        # Replace the shorthand for pound with a common separator, or otherwise the first space, to show that it is separate from other number values
        if 'l' in tau:
            tau = re.sub(r'(?i) ?l ?', ',,', tau)

    if ',,' not in tau:
        tau = re.sub(r' ', ',,', tau, 1)

    tau = re.sub(r'(?i)p', ',,', tau)




    if re.search(r'(?i) ?d ?', tau) and not re.search(r'(?i) ?s ?', tau):
        tau = re.sub(r',,', ',,,,', tau, 1)
    whakareri = re.compile('(?i) ?[sd] ?')
    if whakareri.search(tau):
        tau = whakareri.sub(',,', tau)

    # If there are any symbols that cannot be processed, the function breaks
    if re.search(r'[^\d\., ]', tau):
        return tui

    # Splits the string into pounds, shillings and pence components, if they exist.
    tau_pakaru = tau.split(',,')

    # Processes the 'pounds', i.e. the digits before the first ',,' split.
    # If the hōputu_tau function returns 'kore', indicating no non-zero digits, the variable is replaced with an empty string for Boolean operation purposes
    pāuna = hōputu_tau(tau_pakaru[0])
    pāuna = pāuna if pāuna != 'kore' else ''
    # If there was a second part to the split, hōputu_tau processes the digits.
    if len(tau_pakaru) > 1 and tau_pakaru[1]:
        herengi = hōputu_tau(tau_pakaru[1])
        herengi = herengi if herengi != 'kore' else ''
    # If there was a third part to the split, hōputu_tau processes the digits.
    if len(tau_pakaru) > 2 and tau_pakaru[2]:
        pene = hōputu_tau(tau_pakaru[2])
        pene = pene if pene != 'kore' else ''

    # If there were non-zero digits in the string before the first instance of ',,'
    if pāuna:
        # It adds a pound signifier if the pound variable was activated
        if moni:
            pāuna = "pāuna moni " + pāuna
        # If there was more than one non-zero segment separated by ',,', it adds a comma and space for syntactical reasons.
        if (herengi or pene):
            pāuna += ", "

    # If there was a second segment with non-zero digits
    if herengi:
        # And a first non-zero segment
        if pāuna:
            # The second segment is preceeded by 'ngā' if there was more than one pound in the first segment, otherwise 'te'
            if herengi != 'tahi':
                herengi = "ngā " + herengi
            else:
                herengi = "te " + herengi
            # Then preceeded by 'me', as the syntax for non-zero shillings or pence is 'me ngā' or 'me te'
            herengi = "me " + herengi
        # Regardless of whether the first segment was non-zero or otherwise, the word for shillings must be added.
        herengi += " herengi "

    # If there is a third segment with non-zero digits
    if pene:
        # If there were non-zero preceeding segments
        if (pāuna or herengi):
            # Apply the same 'me te' or 'me ngā' format as in the 'herengi' if statement.
            if pene != 'tahi':
                pene = "ngā " + pene
            else:
                pene = "te " + pene
            pene = "me " + pene
        # Add the word for pence regardless
        pene += " pene"

    # If there were any non-zero digits, return the money format, without excess spaces
    if (pāuna or herengi or pene):
        return clean_whitespace(pāuna + herengi + pene)
    # Otherwise, return the word for 'none' in regards to money.
    else:
        return 'utukore'


def tāima_kupu(tau):
    # Takes a string of digits and letters and returns a string of words for the time the input represents.
    # The input string must be up to 3 instances of 1 or 2 digits, separated by periods, commas or colons, optionally followed by an 'am' or 'pm' which may have its own periods

    # Sets up the variable that determines whether the time should be expressed as '(minutes) past (hour)' or '(minutes) to (hour)'.
    # It will be set to True if the latter format is required.
    āpānoa = False

    # Replace all punctuation with a single variation
    ngā_tau = re.sub(r'[:,]', '.', tau)
    # Search for am/pm
    whakataki = re.search(r' ?[ap]\.?m\.?', ngā_tau)
    # If found,
    if whakataki:
        whakataki = whakataki.group(0)
        # Set the time of day variable to True if there is an 'a' in the second component, signifying the presence of 'am', else False, signifying 'pm'
        rā = True if ('a' in whakataki) else False
        # Remove am/pm from the string
        ngā_tau = ngā_tau.replace(whakataki, '')
    else:
        # Set it to be None, since there is no time of day information
        rā = None
    # Split the string up into components by periods
    ngā_tau = [nama.strip() for nama in ngā_tau.split('.')]

    # The i is an index variable to extract the hours from the list, depending on how many entries
    # If there are 3, the first component of the '.' is not relevant, the second contains the hours, and the third contains the minutes.
    # Otherwise, the hours will be the first component. 3 is the maximum amount of components.
    hāora = ngā_tau[1 if (len(ngā_tau) > 2) else 0]
    hāora = eval(hāora.lstrip('0')) if hāora.lstrip('0') else 12
    # If there is more than one component, the last component will represent the minutes. If there are no minutes, we assume there are no minutes past the hour
    if len(ngā_tau) > 1:
        miniti = eval(ngā_tau[-1].lstrip('0')) if ngā_tau[-1].lstrip('0') else 0
    else:
        miniti = 0

    # If the minutes evaluate as greater than 'half past'
    if miniti > 30:
        # Changing the minutes since the past hour, to the minutes until the next hour
        miniti = 60 - miniti
        # Activate the 'until' variable, so that it is expressed as '(minutes) to (hour)' as opposed to '(minutes) past (hour)'
        āpānoa = True

    # If the minutes past/to the hour are 15, it is more conventional to say 'quarter past/to'
    if miniti == 15:
        miniti = 'hauwhā'
    # If the minutes past the hour are 30, it is more conventional to say 'half past'
    elif miniti == 30:
        miniti = 'haurua'
    # If none of these conventional methods apply, convert the minutes' numerals to words
    else:
        miniti = hōputu_tau(str(miniti))

    # Hours are expressed as 'tahi' rather than 'kotahi' when in the 'until' format.
    # So the hour is made to be 'tahi' if the current hour is '12' and it needs to be in 'until' format
    if āpānoa and hāora == 12:
        hāora = 'tahi'
    # Otherwise, if in 'until' format, the hour becomes the succeeding hour, and is then converted into words
    # If the current hour is '11' and a time of day is specified, the time of day is swapped when the hour changes to '12'.
    elif āpānoa:
        if hāora == 11 and rā != None:
            rā = not rā
        hāora = hōputu_tau(str(hāora + 1))
    # Otherwise, if not in 'until' format, the hour is converted to words
    else:
        hāora = hōputu_tau(str(hāora))

    # Set up the variable where the expression of time will be stored
    reo = ""
    # If there are non-zero minutes, write the minutes. Depending if the time is in 'until' format, it will write the equivalent for "to" or "past" the hour.
    if miniti != 'kore':
        reo += miniti
        if āpānoa:
            reo += " ki"
        else:
            reo += " mai i"
        reo += " te "
    # Writes the hour, followed by 'te wā' as per the convention.
    reo += hāora + " te wā"
    # If there is a time of day specified, it sets it up with 'i te', and then writes the equivalent of 'morning' or 'evening' depending
    if rā != None:
        reo += " i te "
        if rā:
            reo += "ata"
        else:
            reo += "ahiahitanga"

    # Returns the string of words representing the time
    return reo


def rā_kupu(nama):
    # Returns the words representing the date, in a string
    # The input is a string. It can contain 2 or 3 sets of 1 or 2 digits separated by '/', or a quasi-verbal date format.
    # This date format will definitely contain the name of the month in te reo. It will contain the day of the month, or the year, in numerals. If it has both, the day of the month will preceed the year.
    # If it is in a day, month, year format - the words "te" and "o" may be on the left and right side of the day respectively. Both can be present, or just one. Any of the day, month and year can be separated by commas, but will definitely be separed by spaces.
    # The second set must be less than 12 or the function will break. If there is a third set, it must be less than 100 or else the output will be erroneous

    # Sets up the dictionary containing the names of the months
    ngā_marama = {1: 'Hānuere', 2: 'Pēpuere', 3: 'Māehe', 4: 'Āpereira', 5: 'Mei', 6: 'Hune',
                  7: 'Hūrae', 8: 'Ākuhata', 9: 'Hepetema', 10: 'Oketopa', 11: 'Noema', 12: 'Tīhema'}

    # If the function cannot find any letters, it must be in the purely numeric format, e.g. xx/xx/xx.
    if not re.search(r'(?i)[a-z]', nama):
        # Removes whitespace
        nama = re.sub(r'\s', '', nama)
        # Splits the input string into either 2 or 3 components.
        # The components are then evaluated as the integers they contain, unless the component solely contains 0s, then 0 is manually assigned.
        ngā_nama = [int(tau) if tau.lstrip('0') else 0 for tau in nama.split('/')]
        # Assigns each element of the string to a variable for ease of readability
        rā, marama, tau = ngā_nama + [None] if len(ngā_nama) == 2 else ngā_nama

        # Block of if statements that determine the order of the day, month and year.
        # If ngā_nama's second component is greater than 12, it does not represent a month.
        # If ngā_nama's second component is less than the 31 days represented in the 1st, 3rd, 5th etc months, or the 30 days in the 4th, 6th, 9th etc, or the maximum of 29 in the 2nd month
        if marama > 12 and ((31 >= marama and rā in [1, 3, 5, 7, 8, 10, 12]) or (30 >= marama and rā in [4, 6, 9, 11]) or (29 >= marama and rā == 2)):
            # Then the month is actually ngā_nama's first component, and day is the second.
            rā, marama = marama, rā
        # Otherwise, if the number in ngā_nama's second component is greater than the amount of days in the month represented by the first component
        elif (marama > 31 and rā in [1, 3, 5, 7, 8, 10, 12]) or (marama > 30 and rā in [4, 6, 9, 11]) or (marama > 29 and rā == 2):
            # Then there is no day, the month is the list's first component, and the year is the second.
            rā, marama, tau = None, rā, marama
        # Otherwise, if there is an unacceptable format (ngā_nama's first component being greater than the number of days in the month represented by the second component)
        elif ((rā > 31 and marama in [1, 3, 5, 7, 8, 10, 12]) or (rā > 30 and marama in [4, 6, 9, 11]) or (rā > 29 and marama == 2)) or marama > 12 or marama == 0 or rā == 0:
            # It returns the input string with its whitespace removed.
            return nama

    # Otherwise, if a letter was found, it is assumed to be in the quasi-verbal format.
    else:
        # Finds the month. If it cannot be found, it returns the original text. Extracts the words for the month in the match.
        marama = re.search(r'(?i)[a-z]{3,}', nama)
        if not marama:
            return nama
        marama = marama.group(0)
        # Removes useless characters/sequences from the string, including the month since that is already stored in a variable, and excess spaces.
        tau = re.compile(marama).sub('', nama)
        tau = re.sub('(?i)([^\w ]|te|o|)','', tau)
        # All that should remain in the string is numbers. Either the day and year (in that order) separated by a space, or just one of them alone.
        # The string is split by its spaces, which are cleaned first so that there are no useless components.
        ngā_nama = clean_whitespace(tau).split()
        # The components are then evaluated as the integers they contain, unless the component solely contains 0s, then 0 is manually assigned.
        ngā_nama = [int(tau) if tau.lstrip('0') else 0 for tau in ngā_nama]

        # If there are more or less components than expected, the function returns early
        if len(ngā_nama) > 2 or len(ngā_nama) == 0:
            return nama
        # If there are two components, we know they are in the order day then year, and they are assigned thusly.
        elif len(ngā_nama) == 2:
            rā, tau = ngā_nama
        # Otherwise, if there is only one component, the only variable in the list is assigned to a variable so it can be processed as a string
        else:
            te_nama = ngā_nama[0]
            # If this numeral has 4 digits, it could represents a year. As there is only one number, there must be no day.
            if len(str(te_nama)) == 4:
                tau, rā = te_nama, None
            # If this numeral has 1 or 2 digits, it could a day. As there is only one number, there must be no year.
            elif len(str(te_nama)):
                rā, tau = te_nama, None
            # If the number is not assigned, the input string is returned.
            else:
                return nama

    # If there is an illegitimate day, month, or year, the input string is returned.
    # The month is only evaluated if the input string did not contain words.
    # Therefore it is possible to get some illegitimate dates, like the 31st of February of April if the input string was in the quasi-verbal format.
    if (rā and not 0 < rā < 32) or (isinstance(marama, int) and marama > 12) or (tau and ((len(str(tau)) not in [2,4]) or (33 < int(str(tau)[-2:]) < 41) or (len(str(tau)) == 4 and str(tau)[:2] not in ['18', '19']))):
        return nama

    # Sets up the output string of words
    reo = ""
    if rā:
        reo += "te "
        # If there is only one digit in the first component, convert it into an ordinal number by adding "tua" to the front
        if rā < 10:
            reo += "tua"
        # Add to the string by converting the day into words, adding context, and converting the second component, the month, into words using the month dictionary.
        # Excess 0s must be stripped for this dictionary, unlike calls to hōputu_nama.
        reo += hōputu_tau(str(rā)) + " o ngā rā o "
    else:
        reo += "te marama o "

    # If the month variable is a number, the corresponding month is found from the dictionary. Otherwise it will already be a string in te reo, and can be added to the output
    reo += ngā_marama[marama] if isinstance(marama, int) else marama

    # If there is no third component, return the string as is, otherwise keep adding to it by prefacing the year.
    if tau == None:
        return reo

    reo += " i te tau o tō tātou Ariki "

    # All years from ngā niupepa are either in the 1900s or 1800s, between approximately 1840 and 1930.
    # The century can then be determined by the third component of the input date, representing the decade and year.
    # i.e. if the decade is before 35, it will be in the 1900s, and if it is after 35, it will be in the 1800s.
    # The decade and year are converted to numbers, and the string is returned.

    if tau < 35:
        reo += hōputu_tau('19' + str(tau))
    else:
        reo += hōputu_tau('18' + str(tau))

    return reo



def hautau_rānei_ira(tau):
    # Picks up numbers in strings separated by slashes or periods, and returns the numbers joined by the word "mā".
    kati = re.search(r'( ?/ ?|\.)', tau).group(0)
    return " mā ".join(tau.split(kati))
