import requests
from bs4 import BeautifulSoup
import argparse

def get_webpage_content(url):
    """
    Fetch the content of the web page.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

def extract_sentences_with_phrase(text, phrase):
    """
    Extract sentences containing the specified phrase from the text.
    Assume that each sentence is already divided by newlines.
    """
    # Split the text by newline characters
    sentences = text.splitlines()
    
    # Filter sentences that contain the phrase (case insensitive)
    matching_sentences = [sentence for sentence in sentences if phrase.lower() in sentence.lower()]
    
    return matching_sentences

def save_sentences_to_markdown(sentences, phrase):
    """
    Save the sentences to a markdown file, with extra newlines between each matching sentence.
    """
    # File name based on the phrase
    filename = f"extracted_sentences_{phrase.replace(' ', '_')}.md"
    
    with open(filename, 'w') as f:
        f.write(f"# Sentences containing '{phrase}'\n\n")
        for sentence in sentences:
            f.write(sentence.strip() + "\n\n")  # Write each sentence followed by two newlines
    
    print(f"Sentences saved to {filename}")

def get_sentences_from_webpage(url, phrase):
    """
    Extract sentences containing the specified phrase from the webpage content.
    """
    webpage_content = get_webpage_content(url)
    
    if not webpage_content:
        return []
    
    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(webpage_content, 'html.parser')
    
    # Extract all text from the page
    page_text = soup.get_text(separator="\n", strip=True)  # Ensure text is split by newlines
    
    # Extract sentences with the specified phrase
    sentences = extract_sentences_with_phrase(page_text, phrase)
    
    return sentences

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Extract sentences with a specific phrase from a web page and save to a markdown file.")
    parser.add_argument("url", help="The URL of the webpage to fetch content from")
    parser.add_argument("phrase", help="The phrase to search for in the webpage content")
    
    args = parser.parse_args()
    
    # Get sentences from the webpage containing the phrase
    sentences = get_sentences_from_webpage(args.url, args.phrase)
    
    if sentences:
        print(f"Sentences containing '{args.phrase}' found. Saving to markdown file...")
        save_sentences_to_markdown(sentences, args.phrase)
    else:
        print(f"No sentences found containing the phrase '{args.phrase}'.")

if __name__ == "__main__":
    main()
