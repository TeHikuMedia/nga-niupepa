# nga-niupepa
Code for extracting Māori text from the 19th century Māori language newspapers
Both scripts are only intended for python3.

## Tau
`tau` is a module containing functions that return the reo of common strings containing numbers, such as dates, time and financial figures. It is specifically catered to nzdl's niupepa archive, in that it assumes dates are between 1841 and 1933. It also only recognises typographical conventions used in the newspaper, and may be erroneous upon usage with external conventions.

## Usage
* `hiki_niupepa_kupu` collects text from the 19th century Māori language newspaper archive, splits it into its constituent paragraphs, determines how much Māori language is used, and stores it. It outputs a CSV file containing the time of extraction, newspaper name, issue name, page number, percentage of Māori language in the text, the raw, and the page's url for every paragraph it can find in every issue, including paragraphs that span multiple pages. The script can update the 'text' CSV if it is incomplete. It uses the CSV, re, time, argparse, pathlib, urllib.request, bs4, datetime and taumahi modules, which may need to be installed. Some possible formats are provided below to execute the script. If no files are specified, it will use a default name.

```
python3 hiki_niupepa_kupu -u url_file.csv -t text_file.csv
python3 hiki_niupepa_kupu
```

* `hiki_rau_ōrau` collects paragraphs from the output CSV file of `hiki_niupepa_kupu` if they are evaluated as being 100% Māori, and saves the paragraphs along with their associated information (specified below under the columns explanation) to a new CSV file. It adds a new column, bad_read, to which it writes True if there are special characters detected, indicating the newspaper scan has had problems being converted into text. The input CSV file and output CSV file can be passed to the script in the terminal using `-i` and `-o` respectively, otherwise it will use default names. Alternatively it can rewrite the input CSV file using `-r`, which takes precedence over `-i` and `-o`. Possible formats are provided below for executing the script.

```
python3 hiki_rau_ōrau -i input_file.csv -o output_file.csv
python3 hiki_rau_ōrau -r rewritable_file.csv
python3 hiki_rau_ōrau -i input_file.csv
python3 hiki_rau_ōrau -o output_file.csv
python3 hiki_rau_ōrau
```

* `whakahāngai_ōrau` updates the percentage of Māori language calculation for each row in the text file output by hiki_niupepa_kupu depending on the usage of the taumahi function in hiki_niupepa_kupu. It can overwrite the input CSV file, or keep the input CSV file and make a new output CSV file. The input CSV file and output CSV file can be passed to the script in the terminal using `-i` and `-o` respectively, otherwise it will use default names. Alternatively it can rewrite the input CSV file using `-r`, which takes precedence over `-i` and `-o` Possible formats are provided below for executing the script.

```
python3 whakahāngai_ōrau -i input_file.csv -o output_file.csv
python3 whakahāngai_ōrau -r rewritable_file.csv
python3 whakahāngai_ōrau -i input_file.csv
python3 whakahāngai_ōrau -o output_file.csv
python3 whakahāngai_ōrau
```

* `kopana_kōwae` collects rows from the output CSV file of `hiki_niupepa_kupu` and splits the text into paragraphs, which are individually analysed and saved, along with their associated information (specified below under the columns explanation), to a new CSV file. The input CSV file and output CSV file can be passed to the script in the terminal using `-i` and `-o` respectively, otherwise it will use default names. Alternatively it can rewrite the input CSV file using `-r`, which takes precedence over `-i` and `-o`. Possible formats are provided below for executing the script. This was useful for testing `hiki_niupepa_kupu`'s paragraph splitting function, from when it only saved and analysed each page's text.

```
python3 kopana_kōwae -i input_file.csv -o output_file.csv
python3 kopana_kōwae -r rewritable_file.csv
python3 kopana_kōwae -i input_file.csv
python3 kopana_kōwae -o output_file.csv
python3 kopana_kōwae
```

* `hihira_kupu_pākehā` collects all the text from the output CSV file of `hiki_niupepa_kupu` and collects a set of every word in the CSV file's text column which it determines to not be Māori. The input CSV file can be passed to the script in the terminal using `-i` otherwise it will use a default name. If an output file is passed in the terminal using `-o`, the list of pākehā words will be saved to that file, otherwise they will be printed in the terminal. Possible formats are provided below for executing the script. This was useful for determining which words were being incorrectly counted after the `taumahi` module had been updated.

```
python3 hihira_kupu_pākehā -i input_file.csv -o output_file.csv
python3 hihira_kupu_pākehā -i input_file.csv
python3 hihira_kupu_pākehā
```

### perehitanga_kuputohu.csv columns
* date_retrieved: the time at which the text was extracted and converted from NZDL's archive, useful for chronological ordering of the CSV
* newspaper: the name of the newspaper from which the text was retrieved, including the years of publication - corresponds to the categories on the archive website
* issue: the name of the issue of the newspaper from which the text in the same row was extracted, usually contains "Vol." or "No."
* page: the page number from which the text was extracted, or the page number of the beginning of the paragraph if the text spans multiple pages
* māori: the count of words that are classified as Māori
* rangirua: the count of words that could be Māori or otherwise
* pākehā: the count of words which are not classified as Māori
* tapeke: the total count of words
* ōrau: the percentage of words classified as Māori, without taking ambiguous words into account
* adapted_text: the raw paragraph extracted from the issue's page, adapted into the format required for an IRSTLM.
* url: the hyperlink to the page of the newspaper's issue from which the text was extracted, as given by the page number
* raw_text: the paragraph-split text, scraped directly from the HTML source, after cleaning whitespace.
