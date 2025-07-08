# Ultimate Guitar Bulk Downloader

## About

This tool is used for downloading text tabs and chords from Ultimate Guitar (no Guitar Pro tabs)

> DISCLAIMER : Don't rely too much on this script... I made it in like 1 hour and I don't work on it anymore so it may be broken now

## Usage

`$ python main.py [FILENAME] [ARGUMENTS]`

### Parameters

- `-b, --remove-blank-lines`: remove blank lines in tab
- `-f, --headful`: Run browser in headful mode (visible window)

> WARNING : HEADLESS MODE DIDN'T WORK WHEN I TESTED IT

### Input File Format

1 URL per line, that's it. No comments, no blank lines. Theoretically, you could input any URL but i don't know if it would work.
