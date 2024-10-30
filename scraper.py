# from requests import Session
# from faker import Faker
# from lxml import html
# from time import sleep
# from fuzzywuzzy import fuzz
# from deep_translator import GoogleTranslator
# from exceptions import GoogleSearchError
# import unicodedata


# class GoogleSearch:
#     def __init__(self, language='en', max_results=10):
#         self.language = language
#         self.max_results = max_results
#         self.session = Session()
#         self.fake_agent = Faker()
#         self.translator = GoogleTranslator(source='auto', target=language)
    
#     def search(self, keywords):
#         """Main method to perform the Google search."""
#         if self.language != 'en':
#             keywords = self.translate_text(keywords, 'en')
        
#         query = keywords.replace(' ', '+')
#         results = []
#         start = 0
#         increment = min(self.max_results + 5, 100)

#         while len(results) < self.max_results:
#             url = f'https://www.google.com/search?q={query}&num={increment}&hl={self.language}&start={start}&gbv=1'
#             try:
#                 global response
#                 response = self.session.get(url, timeout=10, headers={'User-Agent': self.fake_agent.user_agent()})
#                 response.raise_for_status()
#             except Exception as e:
#                 raise GoogleSearchError(f"Error fetching search results: {e}")
            
#             if response.status_code == 429:
#                 print('Captcha detected! Exiting search.')
#                 return None
            
#             tree = html.fromstring(response.text)
#             search_elements = tree.xpath("//div[./div/a//h3]")
            
#             if not search_elements:
#                 return results

#             for element in search_elements:
#                 title = element.xpath('.//h3//text()')
#                 if title:
#                     link = element.xpath('.//a/@href[1]')
#                     snippet = element.xpath("./div[2]")
#                     result = {
#                         'title': title[0],
#                         'url': link[0].lstrip('/url?q=').split('&')[0],
#                         'snippet': unicodedata.normalize("NFKD", snippet[0].text_content()) if snippet else "",
#                     }
#                     result['similarity_score'] = self.calculate_similarity(keywords, result['snippet'])
#                     results.append(result)

#                 if len(results) >= self.max_results:
#                     return results

#             start += increment
#             sleep(5)
        
#         return results

#     def translate_text(self, text, target_lang):
#         """Translate text to target language if necessary."""
#         try:
#             return GoogleTranslator(source='auto', target=target_lang).translate(text)
#         except Exception as e:
#             raise GoogleSearchError(f"Translation error: {e}")

#     def calculate_similarity(self, input_text, snippet_text):
#         """Calculate the similarity between input text and the snippet."""
#         return fuzz.token_set_ratio(input_text, snippet_text)

# # Example of usage
# if __name__ == "__main__":
#     search_tool = GoogleSearch(language='el', max_results=20)
#     results = search_tool.search("climate change")
#     print(results)

from requests import Session
from faker import Faker
from lxml import html
from time import sleep
from fuzzywuzzy import fuzz
from deep_translator import GoogleTranslator
from exceptions import GoogleSearchError
import unicodedata
import warnings

# Suppress warnings related to fuzzy matching performance
warnings.filterwarnings("ignore", category=UserWarning, message="Using slow pure-python SequenceMatcher. Install python-Levenshtein to remove this warning")

class GoogleSearch:
    def __init__(self, language='en', max_results=10, max_retries=3):
        self.language = language
        self.max_results = max_results
        self.session = Session()
        self.fake_agent = Faker()
        self.translator = GoogleTranslator(source='auto', target=language)
        self.max_retries = max_retries

    def search(self, keywords):
        """Main method to perform the Google search."""
        if self.language != 'en':
            try:
                keywords = self.translate_text(keywords, 'en')
            except GoogleSearchError as e:
                print(e)
                return None

        query = keywords.replace(' ', '+')
        increment = min(self.max_results + 5, 100)

        for attempt in range(1, self.max_retries + 1):
            results = []
            start = 0
            
            while len(results) < self.max_results:
                url = f'https://www.google.com/search?q={query}&num={increment}&hl={self.language}&start={start}&gbv=1'
                try:
                    response = self.session.get(url, timeout=10, headers={'User-Agent': self.fake_agent.user_agent()})
                    response.raise_for_status()
                except Exception as e:
                    print(f"Attempt {attempt}: Error fetching search results - {e}")
                    sleep(5)
                    continue  # Retry if there's an error fetching results

                if response.status_code == 429:
                    print(f"Attempt {attempt}: Captcha detected! Retrying after waiting...")
                    sleep(5)
                    continue

                try:
                    tree = html.fromstring(response.content)  # Use response.content for byte input
                    search_elements = tree.xpath("//div[./div/a//h3]")
                except ValueError as e:
                    print(f"Attempt {attempt}: Error parsing HTML content - {e}")
                    sleep(5)
                    continue

                if not search_elements:
                    print(f"Attempt {attempt}: No search elements found. Retrying...")
                    break

                for element in search_elements:
                    try:
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
                    except (IndexError, ValueError) as e:
                        print(f"Attempt {attempt}: Error processing search element - {e}")
                        continue

                    if len(results) >= self.max_results:
                        return results

                start += increment
                sleep(5)

            if results:
                return results
            print(f"Attempt {attempt}: Retrying as results list is empty.")
        
        print("Max retries reached. No results obtained.")
        return None

    def translate_text(self, text, target_lang):
        """Translate text to target language if necessary."""
        try:
            return GoogleTranslator(source='auto', target=target_lang).translate(text)
        except Exception as e:
            raise GoogleSearchError(f"Translation error: {e}")

    def calculate_similarity(self, input_text, snippet_text):
        """Calculate the similarity between input text and the snippet."""
        return fuzz.token_set_ratio(input_text, snippet_text)

# Example of usage
if __name__ == "__main__":
    search_tool = GoogleSearch(language='ja', max_results=100)
    results = search_tool.search("US economy recession")
    print(results)
