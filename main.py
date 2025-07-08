from argparse import ArgumentParser
import os
from playwright.sync_api import sync_playwright

def get_parser() -> ArgumentParser:
    """
    Get parser
    Parser provides script argument descriptions and help messaging
    """
    parser = ArgumentParser(description='Download tabs')
    parser.add_argument('input', nargs=1, type=str)
    parser.add_argument('-b', '--remove-blank-lines', action='store_true', help='Remove blank lines from the downloaded tabs')
    parser.add_argument('-f', '--headful', action='store_true', help='Run browser in headful mode (visible window)')
    return parser

def get_urls(inf: str) -> list[str]:
    """
    Get urls from input file (inf). Accepts txt files
    """
    files = []
    with open(inf, 'r') as f:
        for line in f:
            files.append(line)
    return files

def write_file(filename: str, content: str) -> None:
    """
    Write content to a file with the given filename.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def is_blank_line(line: str) -> bool:
    """
    Check if a line is blank or contains only whitespace.
    """
    if "".join(line.split()) == "": return True
    return False

if __name__ == '__main__':
    args = get_parser().parse_args()

    if not os.path.exists('output'):
        os.makedirs('output')

    file = args.input[0]    # argparse returns single element list for input

    # Check for '-b' argument for removing blank lines
    if args.remove_blank_lines or args.b:
        remove_blank_lines = True
        print("Blank lines WILL BE removed from the downloaded tabs.")
    else:
        remove_blank_lines = False
        print("Blank lines will NOT be removed from the downloaded tabs.")

    # Check for '-f' argument for headful mode
    if args.headful:
        print("Running browser in headful mode (visible window).")
        headless = False
    else:
        print("Running browser in headless mode (invisible window).")
        headless = True

    urls = get_urls(file)
    success = []

    # Browser pre-initialization to gain time and resources
    with sync_playwright() as pw:
        print("Launching browser...")
        browser_obj = pw.chromium.launch(headless=headless)

        for url in urls:
            try:
                context = browser_obj.new_context(
                    viewport={"width": 1920, "height": 1080}
                )
                # <===== Data scraping =====>
                rendered_text = ""
                page = context.new_page()
                page.goto(url)
                print(f"Downloading tab from {url}")

                # Wait for the page to load and the network to be idle
                # This is important to ensure all elements are rendered
                page.wait_for_load_state('domcontentloaded')

                if page.get_by_text('AGREE').is_visible():
                    print("Found 'AGREE' button. Clicking to accept cookies.")
                    page.get_by_text('AGREE').click()

                # Sometimes, there are 2 'Dismiss' buttons for the tab rating popup... That causes problems for
                # playwright, so we check the CSS class
                dismiss_button = page.locator('button.H2hsN.vDzLP[aria-label="Dismiss"]')
                if dismiss_button.is_visible():
                    print("Found 'Dismiss' button for tab rating popup. Clicking to dismiss.")
                    dismiss_button.click()

                print("Searching for tab element with class 'lVIJS'... Selecting tab content.")
                tab_element = page.query_selector('.lVIJS')
                if tab_element:
                    rendered_text = tab_element.inner_text()

                clean_text = ""

                if remove_blank_lines:
                    print("Processing rendered text to remove blank lines...")
                    for line in rendered_text.split('\n'):
                        if not is_blank_line(line):
                            # Makes sure the title is separated from the capo
                            if not line.startswith('Capo:') and not line.startswith('Tuning:') \
                            and not line.startswith('Key:'):
                                if line.endswith('fret') or line.endswith('no capo'):
                                    clean_text += line + '\n'
                                else:
                                    clean_text += line
                            else:
                                clean_text += '\n' + line
                else:
                    clean_text = rendered_text
                print("Closing page.")
                page.close()
                context.close()


                # <===== Writing to file + error handling =====>
                if rendered_text == "":
                    print(f"Empty tab downloaded: {url}")
                else:
                    success.append(url)
                    print(f"Sucessfully downloaded {url}. Saving to output directory.")
                    filename = os.path.join('output', url.split('/')[-1].strip() + '.txt')
                    write_file(filename, clean_text)


            except KeyError:
                print(f"Missed expected header downloading: {url}")
            except Exception as e:
                print(f"Failed to download: {url}\n Reason: {str(e)}")
        
        browser_obj.close()
