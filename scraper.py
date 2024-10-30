from requests import Session
from requests.exceptions import HTTPError, RequestException
from faker import Faker
from lxml import html
from time import sleep
from fuzzywuzzy import fuzz
from deep_translator import GoogleTranslator
from exceptions import GoogleSearchError
import unicodedata

class GoogleSearch:
    def __init__(self, language='en', max_results=10):
        self.language = language
        self.max_results = max_results
        self.session = Session()
        self.fake_agent = Faker()
        self.translator = GoogleTranslator(source='auto', target=language)
    
    def search(self, keywords):
        """Main method to perform the Google search."""
        if self.language != 'en':
            keywords = self.translate_text(keywords, 'en')
        
        query = keywords.replace(' ', '+')
        results = []
        start = 0
        increment = min(self.max_results + 5, 100)

        while len(results) < self.max_results:
            url = f'https://www.google.com/search?q={query}&num={increment}&hl={self.language}&start={start}&gbv=1'
            try:
                response = self.session.get(url, timeout=10, headers={'User-Agent': self.fake_agent.user_agent()})
                response.raise_for_status()
            except HTTPError as http_err:
                # Handle specific HTTP errors with status code and message
                error_message = f"HTTP error occurred: {http_err.response.status_code} - {http_err.response.reason}"
                print(error_message)
                return {"error": error_message, "status_code": http_err.response.status_code}
            except RequestException as req_err:
                # Handle other requests exceptions
                error_message = f"Request error occurred: {req_err}"
                print(error_message)
                return {"error": error_message, "status_code": None}
            except Exception as e:
                # Catch-all for any other errors
                error_message = f"An unexpected error occurred: {e}"
                print(error_message)
                return {"error": error_message, "status_code": None}
            
            if response.status_code == 429:
                error_message = "Captcha detected! Exiting search."
                print(error_message)
                return {"error": error_message, "status_code": 429}
            
            try:
                tree = html.fromstring(response.text)
                search_elements = tree.xpath("//div[./div/a//h3]")
            except Exception as parse_err:
                # Handle parsing errors
                error_message = f"Error parsing HTML content: {parse_err}"
                print(error_message)
                return {"error": error_message, "status_code": None}

            if not search_elements:
                print("No search elements found.")
                return results

            for element in search_elements:
                title = element.xpath('.//h3//text()')
                if title:
                    link = element.xpath('.//a/@href[1]')
                    snippet = element.xpath("./div[2]")
                    result = {
                        'title': title[0],
                        'url': link[0].lstrip('/url?q=').split('&')[0],
                        'snippet': unicodedata.normalize("NFKD", snippet[0].text_content()) if snippet else "",
                    }
                    result['similarity_score'] = self.calculate_similarity(keywords, result['snippet'])
                    results.append(result)

                if len(results) >= self.max_results:
                    return results

            start += increment
            sleep(5)
        
        return results

    def translate_text(self, text, target_lang):
        """Translate text to target language if necessary."""
        try:
            return GoogleTranslator(source='auto', target=target_lang).translate(text)
        except Exception as e:
            error_message = f"Translation error: {e}"
            print(error_message)
            return {"error": error_message, "status_code": None}

    def calculate_similarity(self, input_text, snippet_text):
        """Calculate the similarity between input text and the snippet."""
        return fuzz.token_set_ratio(input_text, snippet_text)
