# Springer Downloader
Springer offers a selection of textbooks [for free](https://link.springer.com/search?facet-content-type=%22Book%22&package=mat-covid19_textbooks) during the Covid-19 crisis.

This little tool allows to download all free books into a folder or all books of the disciplines: Engineering, Computer Science, Mathematics, Physics, Psychology.

## How to use
### Download all free books into one folder
```
python3 app.py
```

### Command line options
Download only books of one discipline into a separate folder
```
python3 app.py -d *option*
```
Possible options are: `engineering`, `computer_science`, `mathematics`, `physics`, `psychology`

## Requirements
Python 3