# Ultimate Guitar Bulk Downloader

## About

This tool is used for downloading text tabs and chords from Ultimate Guitar (no Guitar Pro tabs)

This project uses [Playwright](https://pypi.org/project/playwright/) for scraping

> DISCLAIMER : Don't rely too much on this script... I made it in like 1 hour and I don't work on it anymore so it may be broken now

## Setup

- You will need python 3 for this script
- In your terminal, navigate to the directory and type `pip install -r requirements.txt`

## Usage

`$ python main.py [FILENAME] [ARGUMENTS]`

### Parameters

- `-b, --remove-blank-lines`: remove blank lines in tab
- `-f, --headful`: Run browser in headful mode (visible window)

> WARNING : HEADLESS MODE DIDN'T WORK WHEN I TESTED IT

### Input File Format

1 URL per line, that's it. No comments, no blank lines. Theoretically, you could input any URL but i don't know if it would work.
