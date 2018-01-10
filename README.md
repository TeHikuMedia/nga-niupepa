# nga-niupepa
Code for extracting Māori text from the 19th century Māori language newspapers

Both scripts are only intended for python3.

`hiki_niupepa_kupu` collects text from the 19th century Māori language newspaper archive, determines how much Māori language is used, and stores it in a csv. It uses a 'url' csv file containing the urls of all the newspapers' issues and their urls, and a 'text' csv file containing the time of extraction, newspaper name, issue name, page number, percentage of Māori language in the text, the page's text, and the page's url. If it doesn't have these csvs, it will create them. When tested, the process took about 2 hours, so the script may be stopped and continued later, i.e. the script can update the 'text' csv if it is incomplete. It uses the csv, re, time, argparse, pathlib, urllib.request, bs4, datetime and taumahi modules, which may need to be installed. Some possible formats are provided below to execute the script. If no files are specified, it will use a default name.

`python3 hiki_niupepa_kupu -u url_file.csv -t text_file.csv` \n
`python3 hiki_niupepa_kupu`

`whakahāngai_ōrau` updates the percentage of Māori language calculation for each page in the text file output by hiki_niupepa_kupu depending on the usage of the taumahi function in hiki_niupepa_kupu. It can overwrite the input file, or keep the input file and make a new output file. All of the user input options are optional, if no file names are specified it will use default names. However, `-i` and `-o` will be useless if used as well as `-u`. Some possible formats are provided below to execute the script.

`python3 whakahāngai_ōrau -i input_file.csv -o output_file.csv` \n
`python3 whakahāngai_ōrau -u updateable_file.csv` \n
`python3 whakahāngai_ōrau`

# hiki_niupepa_kupu To-Do List

- Revise script
- Split up text entries that are evaluated as being under a certain percentage of Māori (like 95%) and evaluate them by paragraph
- Implement 'classes' for global variables with William
- Make a script that will split text into paragraphs from the text csv file output by hiki_niupepa_kupu
