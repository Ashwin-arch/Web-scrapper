import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Function to check if the website exists by verifying the HTTP status
def check_website_exists(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False

# Function to extract HTML, CSS, JavaScript, and images
def scrape_website(url):
    try:
        # Request the webpage content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get the domain name to create a folder
        domain = urlparse(url).netloc
        folder_name = domain.replace(".", "_")
        
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Save the HTML content
        with open(f"{folder_name}/index.html", "w", encoding='utf-8') as f:
            f.write(soup.prettify())

        # Extract and save all linked CSS files
        css_links = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
        for i, css_link in enumerate(css_links):
            css_url = css_link if css_link.startswith('http') else urljoin(url, css_link)
            css_response = requests.get(css_url)
            with open(f"{folder_name}/style_{i+1}.css", "w", encoding='utf-8') as f:
                f.write(css_response.text)

        # Extract and save JavaScript files
        js_links = [script['src'] for script in soup.find_all('script') if script.get('src')]
        for i, js_link in enumerate(js_links):
            js_url = js_link if js_link.startswith('http') else urljoin(url, js_link)
            js_response = requests.get(js_url)
            with open(f"{folder_name}/script_{i+1}.js", "w", encoding='utf-8') as f:
                f.write(js_response.text)

        # Extract and save image files
        image_links = [img['src'] for img in soup.find_all('img') if img.get('src')]
        for i, img_link in enumerate(image_links):
            img_url = img_link if img_link.startswith('http') else urljoin(url, img_link)
            img_response = requests.get(img_url, stream=True)

            # Save the image
            img_name = os.path.join(folder_name, f"image_{i+1}{os.path.splitext(img_url)[1]}")
            with open(img_name, 'wb') as f:
                for chunk in img_response.iter_content(1024):
                    f.write(chunk)

        print(f"HTML, CSS, JavaScript, and Images saved in folder: {folder_name}")

    except Exception as e:
        print(f"An error occurred while scraping: {e}")

# Main function to run the script
def main():
    url = input("Enter the website URL: ")

    if not url.startswith('http'):
        url = 'http://' + url

    # Check if the website exists
    if check_website_exists(url):
        print(f"Website {url} exists. Starting to scrape...")
        scrape_website(url)
    else:
        print(f"Website {url} does not exist or is unreachable.")

if __name__ == "__main__":
    main()
