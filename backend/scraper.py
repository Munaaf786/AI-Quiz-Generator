import requests
from bs4 import BeautifulSoup, Comment
from urllib.parse import urlparse
from typing import Dict
import re

def scrape_wikipedia(url: str) -> Dict:
    """
    Fetches, parses, and cleans a Wikipedia article to extract
    the main text and title for quiz generation.
    """
    try:
        # Checks if the URL is from Wikipedia
        parsed_url = urlparse(url)
        if not (parsed_url.scheme in ['http', 'https'] and 'wikipedia.org' in parsed_url.netloc):
            raise ValueError("Only Wikipedia URLs are supported.")

        # Sets a User-Agent header to mimic a browser and avoid 403 errors
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an error for bad HTTP responses

        # Parses the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracts the article title from the main heading
        title_tag = soup.find('h1', id='firstHeading')
        title = title_tag.get_text(separator=' ', strip=True) if title_tag else "No Title Found"

        # Finds the main content area of the Wikipedia page
        # Tries standard classes/IDs used in Wikipedia articles
        content_div = soup.find('div', class_='mw-content-ltr')
        if not content_div:
            content_div = soup.find('div', id='mw-content-text')
        if not content_div:
            content_div = soup.find('div', class_='mw-parser-output')

        if not content_div:
            raise RuntimeError("Could not find main content div on Wikipedia page.")

        # modifiable copy of the content div for cleaning
        cleaned_content_soup = BeautifulSoup(str(content_div), 'html.parser')

        # Removes script, style tags, and HTML comments
        for element in cleaned_content_soup(['script', 'style', Comment]):
            element.decompose()

        # Removes various boilerplate and non-article elements by class
        unwanted_classes = [
            'infobox', 'sidebar', 'navbox', 'vertical-navbox', 'hatnote',
            'ambox', 'metadata', 'thumb', 'reference-text', 'rellink',
            'box-Multiple_issues', 'citation-needed', 'portal', 'printfooter',
            'mw-jump-link', 'mw-indicators'
        ]
        unwanted_tags = ['table', 'dl'] # Also removes description lists and general tables

        for cls in unwanted_classes:
            for element in cleaned_content_soup.find_all(class_=cls):
                element.decompose()

        for tag in unwanted_tags:
            for element in cleaned_content_soup.find_all(tag):
                element.decompose()

        # Removes common sections like "See also", "References", etc.
        sections_to_remove = [
            "See also", "References", "External links", "Further reading",
            "Notes", "Bibliography", "Citations", "Footnotes", "Publications",
            "Sources", "Awards and honours"
        ]
        for h2_tag in cleaned_content_soup.find_all('h2'):
            span_headline = h2_tag.find('span', class_='mw-headline')
            if span_headline and span_headline.get_text(strip=True) in sections_to_remove:
                # Removes the heading and all its following content until the next heading
                current_element = h2_tag
                while current_element:
                    next_element = current_element.next_sibling
                    current_element.decompose()
                    current_element = next_element
                    if next_element and next_element.name == 'h2':
                        break

        # Removes superscript reference numbers like [1], [2]
        for sup in cleaned_content_soup.find_all('sup', class_='reference'):
            sup.decompose()

        # Removes phonetic spellings and pronunciation guides
        for span_ipa in cleaned_content_soup.find_all('span', class_='IPA'):
            span_ipa.decompose()
        for small_tag in cleaned_content_soup.find_all('small'):
            small_tag.decompose()
        for span_pron in cleaned_content_soup.find_all('span', class_=['nowrap', 'unicode', 'latinx', 'respell']):
            span_pron.decompose()

        # Extracts text and perform final string cleanup
        clean_text = cleaned_content_soup.get_text(separator=' ', strip=True)

        # Removes multiple spaces
        clean_text = ' '.join(clean_text.split())

        # Removes common Wikipedia introductory boilerplate phrases
        clean_text = clean_text.replace("From Wikipedia, the free encyclopedia", "").strip()
        clean_text = clean_text.replace("Jump to navigation Jump to search", "").strip()
        clean_text = clean_text.replace("This article is about the British mathematician. For other uses, see Alan Turing (disambiguation).", "").strip()

        # Uses regex to remove any remaining phonetic transcription patterns
        clean_text = re.sub(r'\(\s*/.*?/\s*\)', '', clean_text)
        clean_text = re.sub(r'\[\s*/.*?/\s*\]', '', clean_text)
        clean_text = re.sub(r'[\(\[\{][ˈˌ].*?[\)\]\}]', '', clean_text)

        # Standardizes newlines and spacing
        clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)
        clean_text = re.sub(r'([.!?])\s*\n', r'\1 ', clean_text)
        clean_text = re.sub(r'\s*\n\s*', '\n', clean_text).strip()

        return {
            "title": title,
            "clean_text": clean_text,
            "raw_html": response.text
        }

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network or request error: {e}")
    except ValueError as e:
        raise ValueError(f"URL validation error: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during scraping: {e}")

# Example usage (for testing)
if __name__ == "__main__":
    test_url = "https://en.wikipedia.org/wiki/Alan_Turing"

    try:
        scraped_data = scrape_wikipedia(test_url)
        print(f"Title: {scraped_data['title']}")
        print("\n--- Cleaned Text Sample (first 500 chars) ---")
        print(scraped_data['clean_text'][:500])
        print("\n--- Raw HTML Sample (first 500 chars) ---")
        print(scraped_data['raw_html'][:500])
    except (RuntimeError, ValueError) as e:
        print(f"Error: {e}")