#!/usr/bin/python3
# Collects all the text from Māori newspapers on nzdl.org

import csv
import re
import time
import argparse
from pathlib import Path
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import datetime
from taumahi import *

pae_tukutuku = 'http://www.nzdl.org'
pae_tukutuku_haurua = '{}{}'.format(
    pae_tukutuku, '/gsdlmod?gg=text&e=p-00000-00---off-0niupepa--00-0----0-10-0---0---0direct-10---4-------0-1l--11-en-50---20-about---00-0-1-00-0-0-11-1-0utfZz-8-00-0-0-11-10-0utfZz-8-00&a=d&c=niupepa&cl=CL1')

perehitanga_kōnae_ingoa = 'perehitanga_kuputohu.csv'

# Punctuation that will be searched for, and stripped respectively. The former indicates the end of a paragraph if followed by a new line character.
tohutuhi = ".!?"
tohukī = "‘’\'\") "


class Perehitanga:
    # This class takes a row from the index file it reads and attributes it to a class object for readability
    def __init__(self, rārangi, mātāmuri_rārangi=None):
        self.niupepa = rārangi[0]
        if len(rārangi) == 3:
            self.perehitanga = rārangi[1]
            self.taukaea = rārangi[2]
        else:
            self.perehitanga = ''
            self.taukaea = rārangi[1]

        if mātāmuri_rārangi:
            self.mātāmuri_niupepa = mātāmuri_rārangi[1]
            self.mātāmuri_perehitanga = mātāmuri_rārangi[2]
            self.mātāmuri_hau = mātāmuri_rārangi[3]
            self.mātāmuri_kupu = mātāmuri_rārangi[9]
            self.mātāmuri_taukaea = mātāmuri_rārangi[10]
            self.mātāmuri = True
        else:
            self.mātāmuri = False


class Rārangi:
    # This information sets up all the information that will be written to the text csv file, apart from the time of retrieval, in a class object, to prevent the need for tuples, and for improved readability.
    # The input is a Perehitanga class object, and the url of the page the text is extracted from
    # The māori, rangirua, pākehā and tapeke attributes are updated per paragraph in the rārangi_kaituhituhi function.
    def __init__(self, niupepa, taukaea):
        self.niupepa = niupepa.niupepa
        self.perehitanga = niupepa.perehitanga
        self.taukaea = taukaea
        # Extracts the soup of the issue's first page
        self.hupa = bs(urlopen(self.taukaea), 'html.parser')
        # Extracts the page number from the soup
        self.tau = self.hupa.find('b').text.split("page  ")[1]
        self.māori = 0
        self.rangirua = 0
        self.pākehā = 0
        self.tapeke = 0
        self.ōrau = 0.00
        # Extracts the text from the page's soup
        self.kupu = unu_kupu_tōkau(self.hupa, self.tau)
        self.urutau = ""
        self.mātāmuri_rārangi = niupepa.mātāmuri


class Tīmata_kōwae:
    # Sets up the 'left over paragraph' from the previous page in a class object for readability
    # The input is a Rārangi class object.
    def __init__(self, tāuru):
        self.tau = tāuru.tau
        self.kupu = tāuru.kupu
        self.taukaea = tāuru.taukaea


def hātepe_perehitanga(niupepa, kaituhituhi):
    # This function extracts the text from every page of the newspaper issue it
    # Has been passed, and gives it to the text csv writing function. The input
    # Is a Perehitanga class object with the newspaper name, issue name and
    # Issue url as attributes, the csv writer, and a variable to determine if it
    # Should write the text from the first page of the issue it extracts.

    print("Collecting pages of " +
          niupepa.perehitanga + " in " + niupepa.niupepa + ":\n")

    # Passes the issue's information (Perehitanga class object) to the Rāringa class, as well as specifying which page it should start from, as the process may have ended
    tāuru = Rārangi(
        niupepa, niupepa.mātāmuri_taukaea if niupepa.mātāmuri else niupepa.taukaea)

    tīmata_kōwae = None

    # If it hasn't been told to ignore the first page, it passes the information to the writing function
    if not niupepa.mātāmuri:
        print("Extracted page " + tāuru.tau)
        rāringa_kaituhituhi(tāuru, kaituhituhi, tīmata_kōwae)
    else:
        tāuru.kupu = mātītori_kupu(tāuru.kupu)[-1]
        tīmata_kōwae = kupu_moroki(tāuru, tīmata_kōwae)
        # Loops, trying to find a next page. If it can't, the loop breaks.
    while True:
        # Simplifies the soup to where the next page link will be located
        taukaea_pinetohu = tāuru.hupa.select('div.navarrowsbottom')[
            0].find('td', align='right', valign='top')

        # If there is no next page button, the process ends and the list is returned
        if taukaea_pinetohu.a == None:
            print("\nFinished with " + niupepa.perehitanga +
                  " in " + niupepa.niupepa + "\n\n----------\n")
            return

        # If there is a link, its page number, soup and url are made into a tuple to be written to the csv
        elif taukaea_pinetohu.a['href']:

            tāuru = Rārangi(niupepa, pae_tukutuku +
                            taukaea_pinetohu.a['href'])

            print("Extracted page " + tāuru.tau)

            # Passes the tuple and csv writer to the csv writing function
            tīmata_kōwae = rāringa_kaituhituhi(
                tāuru, kaituhituhi, tīmata_kōwae)

        # If there is some other option, the function ends, to prevent an infinite loop.
        else:
            print("\nError collecting all pages\n")
            print("Finished with " + niupepa.perehitanga +
                  " in " + niupepa.niupepa + "\n\n----------\n")
            return


def kupu_moroki(tāuru, tīmata_kōwae):

    # It strips the text of any unnecessary trailing characters that could follow the end of the sentence, such as quotation marks
    mahuru_kupu = tāuru.kupu.strip(tohukī)
    # If there is anything left after these characters have been stripped (so as not to cause an error)
    if mahuru_kupu:
        # If the last character of the string is an acceptable "end of paragraph" character, and there are preceeding pages (i.e. it is not the last page of the issue since a paragraph will not continue over consecutive issues)
        if (mahuru_kupu[-1] not in tohutuhi) and (tāuru.hupa.select('div.navarrowsbottom')[0].find('td', align='right', valign='top').a):
            # Then this paragraph will be carried over to the next page (the next time this function is called) by using the global tīmata_kōwae variable

            # If there isn't already a paragraph being carried over, it stores the start of the paragraph's text, page number and url
            if not tīmata_kōwae:
                tīmata_kōwae = Tīmata_kōwae(tāuru)
            # Otherwise if there is a paragraph being carried over, it just adds the text to the rest of the paragraph, without changing the original page number and url
            else:
                tīmata_kōwae.kupu += tāuru.kupu
            # It then breaks, exiting out of the function, so the carried paragraph is not written until all the text in the paragraph has been collected

    return tīmata_kōwae


def mātītori_kupu(kupu):
    return re.findall(r'[\w\W]*?[{}][{}]*\n|[\w\W]+$'.format(tohutuhi, tohukī), kupu)


def rāringa_kaituhituhi(tāuru, kaituhituhi, tīmata_kōwae):
    # This function splits the text from a given page into its constituent
    # Paragraphs, and writes them along with the page's information (date
    # Retrieved, newspaper name, issue name, page number, Māori word count,
    # Ambiguous word count, other word count, total word count, Māori word
    # Percentage, the raw text, and the url of the page). If it determines that
    # The paragraph carries on to the next page, and it is not the last page of
    # An issue, it carries the information that changes from page to page (text,
    # Page number, url) to the next time the function is called, i.e. the next
    # Page. It tries to find where the paragraph continues, and then writes it
    # To the text csv with the information of the page where it was first found.
    # If it can't, it will continue to loop this information forward until the
    # Last page of the issue. It takes a Rārangi class object, and a csv writer.

    if tāuru.kupu:  # Only writes the information if text was able to be extracted

        # Splits the text up into paragraphs
        kupu_tūtira = mātītori_kupu(tāuru.kupu)

        # Loops through the paragraphs
        for kupu in kupu_tūtira:

            # Strips leading and trailing white space
            tāuru.kupu = kupu.strip()

            # If the paragraph is the last paragraph on the page
            if kupu == kupu_tūtira[-1]:
                tīmata_kōwae = kupu_moroki(tāuru, tīmata_kōwae)

            # If there is leftover text from the previous page, Find the first paragraph that isn't in caps, i.e. isn't a title
            if tīmata_kōwae and not kupu.isupper():

                # Add the leftover text to the first paragraph that isn't entirely uppercase
                tāuru.kupu = tīmata_kōwae.kupu + tāuru.kupu
                # The page number and url that are to be written with the paragraph are from the original paragraph, so they are taken from the global variable and assigned to the variables that will be written
                whārangi_tau = tīmata_kōwae.tau
                whārangi_taukaea = tīmata_kōwae.taukaea
                # Then the global variable is cleared, because it is being written, so nothing is being carried over to the next call of the function
                tīmata_kōwae = None

            else:
                # If nothing is being added from a previous page, the page number and url that are to be written come from the current page, and are assigned to the variables which will be written
                whārangi_tau = tāuru.tau
                whārangi_taukaea = tāuru.taukaea

            # Replaces all white space with a space
            tāuru.kupu = clean_whitespace(tāuru.kupu)
            # If there is no text left after it has been stripped, there is no point writing it, so the function continues onto the next paragraph
            if not tāuru.kupu:
                continue

            tāuru.urutau = whakarauiri(tāuru.kupu)
            tāuru.urutau = tohutau(tāuru.urutau)
            # Gets the percentage of the text that is Māori
            tāuru.māori, tāuru.rangirua, tāuru.pākehā, tāuru.tapeke, tāuru.ōrau = tiki_ōrau(
                tāuru.urutau)
            # Prepares the row that is to be written to the csv
            rārangi = [datetime.now(), tāuru.niupepa, tāuru.perehitanga, whārangi_tau,
                       tāuru.māori, tāuru.rangirua, tāuru.pākehā, tāuru.tapeke, tāuru.ōrau, tāuru.urutau, whārangi_taukaea, tāuru.kupu]
            # Writes the date retrieved, newspaper name, issue name, page number, Māori percentage, extracted text and page url to the file
            kaituhituhi.writerow(rārangi)

    return tīmata_kōwae


def rīwhi_tauriterite(kimikimi, taumahi_ingoa, kōwae):
    # Finds all matches to the input regex, in the input text, using the input string to determine what to replace the match with
    # The first argument is a regex expression, the second is a string containing a function name from the tau module, the third is the text that is to be modified
    ngā_whakataki_tūtira = re.compile(kimikimi).findall(kōwae)
    for ngā_whakataki in ngā_whakataki_tūtira:
        whakataki = ngā_whakataki[0].strip()
        kupu = " "
        if taumahi_ingoa == "rā_kupu":
            kupu += "<date>"
        elif taumahi_ingoa == "tāima_kupu":
            kupu += "<time>"
        else:
            kupu += "<number>"
        kupu += " "
        kōwae = kōwae.replace(whakataki, kupu)
    return kōwae


def tiki_niupepa(kōnae_ingoa, mātāmuri_rārangi=None):
    # Collects the urls and names of all the newspapers
    # Opens the archive page and fetches the soup

    kōnae = open(kōnae_ingoa, 'a')
    kaituhituhi = csv.writer(kōnae)

    if not mātāmuri_rārangi:  # If this evaluates as False, it means to start writing the file from scratch
        # Writes the column names since the file did not exist
        kaituhituhi.writerow(
            ['date_retrieved', 'newspaper', 'issue', 'page', 'māori_words', 'ambiguous_words', 'other_words', 'total_words', 'percent_māori', 'adapted_text', 'url', 'raw_text'])

    hupa = bs(urlopen(pae_tukutuku_haurua), 'html.parser')

    # Gets a list of all tags where newspaper links are stored
    for tr in hupa.select('div.top')[0].find_all('tr', {'valign': 'top'}):
        for td in tr.find_all('td', {'valign': 'top'}):
            if td.a:
                taukaea = pae_tukutuku + td.a['href']
            elif td.text:
                ingoa = td.text[:td.text.index(" (")].strip()

        if mātāmuri_rārangi:
            if ingoa != mātāmuri_rārangi[1]:
                continue
        niupepa = Perehitanga([ingoa, taukaea], mātāmuri_rārangi)
        if mātāmuri_rārangi:
            mātāmuri_rārangi = None
        tiki_perehitanga(niupepa, kaituhituhi)

    kōnae.close()


def tiki_perehitanga(niupepa, kaituhituhi):
    # Collects the names and urls of each issue of a particular newspaper
    hupa = bs(urlopen(niupepa.taukaea), 'html.parser')
    print("\n\nCollecting issues of " +
          niupepa.niupepa + "\n\n\n----------------------------------------\n\n")

    # Finds all tags that contain links and issue names
    for tr in hupa.select('#group_top')[0].find_all('tr', {"valign": "top"}):
        for td in tr.find_all('td', {"valign": "top"}):
            if td.a:
                # If there is a link, adds it to the link list. names and urls have the same index in their respective lists
                niupepa.taukaea = pae_tukutuku + td.a['href']
            elif "No." in td.text or "Volume" in td.text or " " in td.text:
                # Makes sure text meets criteria, as there is some unwanted text. the second bracket is a specific case that doesn't get picked up by the first bracket
                niupepa.perehitanga = td.text.strip()
            else:
                pass

        # If commentary is in the tile, we don't want to extract this title or link
        if "commentary" in niupepa.perehitanga.lower():
            continue

        # If there is a carryover row from where the process stopped,
        if niupepa.mātāmuri:
            # And the current issue is not in the previously written row, then skip it until it is found
            if niupepa.perehitanga != niupepa.mātāmuri_perehitanga:
                continue
            # If it is the same issue, it takes down the 'carryover row' flag, so it can go on to process the issue
            else:
                niupepa.mātāmuri = False

        # Then processes the issue
        hātepe_perehitanga(niupepa, kaituhituhi)


def tohutau(kupu):
    # Formats text in a way suitable for the irstlm language model
    kupu = re.sub(r'w[”“"\'`‘’´]', 'wh', kupu.lower())
    kupu = re.sub(r'[—–]', '-', kupu)
    kupu = re.sub(r'([^A-Za-zĀĒĪŌŪāēīōū\s])', r' \1 ', kupu)
    kupu = re.sub(r'< (date|number|time) >', r'<\1>', kupu)
    kupu = re.sub(r'-', r'@-@', kupu)
    return "<s> " + clean_whitespace(kupu) + " </s>"


def unu_kupu_tōkau(hupa, tau):
    # Extracts the text for all pages of the issue it has been passed.
    # It takes a tuple and a list. The tuple has the newspaper name, issue name
    # And issue link. The list is of tuples containing each page of the issue's
    # Number, soup and url. It outputs a list of tuples, which contain each page
    # Of an issue's number, text and url.

    # Simplify the soup to the area we are interested in
    kupu_tōkau = hupa.select('div.documenttext')[0].find('td')

    # Must determine there is a div.documenttext, because .text will raise an error if it kupu_tōkau is None
    if kupu_tōkau != None:
        if kupu_tōkau.text:
            # If it can find text, it returns it
            return kupu_tōkau.text
        else:
            # If there is no text found, print an error
            print("Failed to extract text from page " + tau)
    else:
        print("Failed to extract text from page " + tau)

    return


def whakarauiri(kupu):
    # The calls to these functions in tau don't need to be made for the irstlm language model, however replacements make the model more effective. Hence we use a string with the function of the tau module's name to represent the kind of object it is replacing.
    marama = '(Hanuere|Pepuere|Maehe|Apereira|Mei|Hune|Hurae|Akuhata|Hepetema|Oketopa|Noema|Nowema|Tihema)'
    # Comma separated pound values, ending with common representations for shillings and pounds
    kupu = rīwhi_tauriterite('((£?([1-9]\d{0,2}[,\/‘`´’\'\".][ ]?)(\d{3}[,\/‘`´’\'\".][ ]?)*\d{3}([.,]{2}\d{1,2}){1,2}))', "pakaru_moni", kupu)
    kupu = rīwhi_tauriterite('(?i)(£?[1-9]\d{0,2}[,\/‘`´’\'\".][ ]?(\d{3}[,\/‘`´’\'\".]?[ ]?)+ ?l\.? ?( ?\d+ ?[ds]\.? ?){0,2})', "pakaru_moni", kupu)
    # Non-comma separated pound values, with the same endings
    kupu = rīwhi_tauriterite('(£?([1-9]\d*([.,]{2}\d{1,2}){1,2}))', "pakaru_moni", kupu)
    kupu = rīwhi_tauriterite('(?i)((£?[1-9]\d*( ?\d+ ?[lsd]\.? ?){1,3}))', "pakaru_moni", kupu)
    # Typical date format xx/xx/xx
    kupu = rīwhi_tauriterite('((\d{1,2}\/){1,2}\d{2})', "rā_kupu", kupu)
    # Other common date formats that involve words - e.g. the (day) of (month), (year); or (month) (day) (year)
    kupu = rīwhi_tauriterite('(?i)((\b|\W|\s|^)(te )\d{1,2}( [,o])? ' + marama + ',? \d{4}(\b|\W|\s|\s|$|\W))', "rā_kupu", kupu)
    kupu = rīwhi_tauriterite('(?i)((\b|\W|\s|^)\d{1,2}( [,o])? ' + marama + ',? \d{4}(\b|\W|\s|\s|$|\W))', "rā_kupu", kupu)
    kupu = rīwhi_tauriterite('(?i)(' + marama + ',? \d{1,2},? \d{4}(\b|\W|\s|$))', "rā_kupu", kupu)
    kupu = rīwhi_tauriterite('(?i)((\b|\W|\s|^)\d{4},? ' + marama + ')', "rā_kupu", kupu)
    kupu = rīwhi_tauriterite('(?i)(' + marama + ',? \d{4}(\b|\W|\s|$))', "rā_kupu", kupu)
    kupu = rīwhi_tauriterite('(?i)((\b|\W|\s|^)(te )\d{1,2}( [,o])? ' + marama + '(\b|\W|\s|$))', "rā_kupu", kupu)
    kupu = rīwhi_tauriterite('(?i)((\b|\W|\s|^)\d{1,2}( [,o])? ' + marama + '(\b|\W|\s|$))', "rā_kupu", kupu)
    kupu = rīwhi_tauriterite('(?i)(' + marama + ',? \d{1,2}(\b|\W|\s|$))', "rā_kupu", kupu)
    # Comma separated pound values with no suffixes
    kupu = rīwhi_tauriterite('(£([1-9]\d{0,2}[,‘`´’\'\".][ ]?)(\d{3}[,\/‘`´’\'\".][ ]?)*\d{3})', "pakaru_moni", kupu)
    # Other comma separated values, not financial
    kupu = rīwhi_tauriterite('(([1-9]\d{0,2}[,‘`´’\'\".][ ]?)(\d{3}[,\/‘`´’\'\".][ ]?)*\d{3})', "hōputu_tau", kupu)
    # Finds times separated by punctuation (with or without a space), optionally followed by am/pm
    kupu = rīwhi_tauriterite('(?i)((\d{1,2}\. ){1,2}(\d{1,2}) ?[ap]\.?m\.?)', "tāima_kupu", kupu)
    kupu = rīwhi_tauriterite('(?i)((\d{1,2}[,.:]){0,2}(\d{1,2}) ?[ap]\.?m\.?)', "tāima_kupu", kupu)
    kupu = rīwhi_tauriterite('((\d{1,2}\. ?){1,2}\d{1,2})', "tāima_kupu", kupu)
    # Deals with any leftover slash-separated values that weren't accepted by "tāima_kupu" by replacing the slashes with words
    kupu = rīwhi_tauriterite('((\d{1,6}( \/ | \/|\/ |\/|\.)){1,5}\d{1,5})', "hautau_rānei_ira", kupu)
    # Finds all other monetary values
    kupu = rīwhi_tauriterite('(£(\d)+)', "pakaru_moni", kupu)
    # Finds all other numbers
    kupu = rīwhi_tauriterite('((\d)+)', "hōputu_tau", kupu)
    # Removes characters that aren't letters or spaces.
    kupu = re.sub(r'[^A-Za-zĀĒĪŌŪāēīōū!"#$%&\'()*+,./:;<=>?[\\]^_`‘’{|}-£´\s]', '', kupu)
    # Clears excess spaces
    return clean_whitespace(kupu)



def matua():

    # Starts recording the time to detail how long the entire process took
    tāti_wā = time.time()

    whakatukai = argparse.ArgumentParser()
    whakatukai.add_argument(
        '--textfile', '-t', help="Output csv file where the date retrieved, newspaper names, issue names, page numbers, word counts, Māori percentage, page text and page urls are stored")
    kōwhiri = whakatukai.parse_args()

    kōnae_ingoa = kōwhiri.textfile if kōwhiri.textfile else perehitanga_kōnae_ingoa

    # Checks whether there is a csv of the text
    if Path(kōnae_ingoa).exists():
        with open(kōnae_ingoa, 'r') as kōnae:

            kupuhou_kōnae = csv.reader(kōnae)
            # Reads all the rows to a list
            rārangi_tūtira = [rārangi for rārangi in kupuhou_kōnae]
            kōnae.close()

            # If the last row contains a valid url, this is the row we want to continue from. Else we continue from the second to last row.
            if 'http://' and '=CL1' in rārangi_tūtira[-1][10]:
                mātāmuri_rārangi = rārangi_tūtira[-1]
            elif len(rārangi_tūtira) > 2:
                mātāmuri_rārangi = rārangi_tūtira[-2]
            else:
                mātāmuri_rārangi = None

            # Gets the newspaper name, issue and page number of the last entry recorded. If the last one is as below, the file is up to date.
            if mātāmuri_rārangi:
                if mātāmuri_rārangi[1:4] == ['Te Toa Takitini 1921-1932', 'Volume 1, No. 7', '96']:
                    print("\nThere is nothing to read, data is already up to date.\n")
                else:
                    # Otherwise, it passes where it was last up to to the text csv writer so it may continue from there
                    print(
                        "\nThe current text corpus is insufficient, rewriting file...")
                    tiki_niupepa(kōnae_ingoa, mātāmuri_rārangi)
            else:
                # Otherwise, it passes where it was last up to to the text csv writer so it may continue from there
                print("\nThe current text corpus is insufficient, rewriting file...")
                tiki_niupepa(kōnae_ingoa)

    else:
        print("\nThere is no current text corpus, collecting text...\n")
        # If there is no text csv file, it begins to write one from scratch
        tiki_niupepa(kōnae_ingoa)

    print(
        "\n\n----------\n\nAll text has been collected and analysed. The process took {:0.2f} seconds.\n".format(time.time() - tāti_wā))  # Prints out how long the process took in a user friendly format

    return


if __name__ == '__main__':
    matua()
