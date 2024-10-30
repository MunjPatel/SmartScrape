# SmartScrape

SmartScrape is a Flask-based web scraping tool that extracts Google search results in real-time, providing an alternative to using Google's official search API. Designed to offer flexibility, customization, and performance, SmartScrape can be deployed as a web application or used locally for various data retrieval and search-related tasks.

## Why SmartScrape?

The traditional Google Search API has several limitations in terms of quotas, response formats, and customization. SmartScrape aims to overcome these limitations by directly scraping Google search results, making it a versatile tool for retrieving data directly from the web.

## Special Notes and Considerations

1. **Ethics and Compliance**: Web scraping should always respect website terms of service. Scraping Google may violate their terms, so use responsibly and consider using it for educational purposes only.
2. **Bot Detection**: Since SmartScrape scrapes live Google search pages, it may occasionally encounter CAPTCHAs or be rate-limited. Adjusting request frequency and headers may reduce these occurrences.
3. **IP Rotation**: Consider using proxies or IP rotation for larger-scale scraping tasks to avoid detection and throttling.

## Example Use Cases

- **Market Research**: Retrieve live search data on competitors, products, or topics.
- **SEO Analysis**: Extract top results to understand keyword rankings and trends.
- **Academic Research**: Collect data for studies or projects requiring public information.

## Google Search API and Its Limitations

The official Google Search API:
- Enforces strict usage quotas and costs per query.
- Has limited control over the search interface and customization.
- Returns data in a structured format without the flexibility of direct HTML scraping.

## How SmartScrape Overcomes These Limitations

SmartScrape directly scrapes Google’s search pages, allowing:
- **Unlimited Customization**: Full control over what data to extract.
- **Real-Time Data**: Access the latest search results.
- **Flexible Output Formats**: Export data as JSON, CSV, or Excel.

## Why Use SmartScrape?

- **Real-Time Results**: Get the latest information as shown on Google’s search page.
- **Full HTML Parsing**: Extract elements directly from the HTML structure, including titles, URLs, snippets, and more.
- **High Customizability**: Configure the tool to retrieve specific parts of the results, customize request headers, and export formats.

## Advantages

- Bypasses limitations of the Google Search API.
- Flexible and customizable scraping options.
- Supports multiple languages for diverse use cases.
- Output formats include JSON, CSV, and Excel.

## Disadvantages

- May encounter CAPTCHAs or rate limits.
- Risk of IP blocking if used aggressively.
- Potential legal or ethical implications when scraping certain data.

## Features

- **Custom Search Query**: Enter any keyword or phrase to search.
- **Language Support**: Choose from a variety of languages.
- **Result Count**: Specify the number of results (up to 100).
- **Download Formats**: Export search results as JSON, CSV, or Excel.
- **Built-In Captcha Handling**: Retries when encountering CAPTCHA blocks.
- **Similarity Scoring**: Calculates similarity between query and snippets.

## Usage

### 1. Try in Production

SmartScrape is deployed on Render. You can test it here: [SmartScrape Production](https://smartscrape.onrender.com).

### 2. Clone the Repository

To use SmartScrape locally, follow these steps:

#### Prerequisites
- Python 3.7+
- Flask
- Required dependencies listed in `requirements.txt`

#### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/SmartScrape.git
    cd SmartScrape
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    flask run
    ```

4. Open your browser and go to `http://127.0.0.1:5000`.

### Performance Optimization

To optimize scraping performance:
- **Rate Limiting**: Add delays between requests to avoid IP blocks.
- **Proxies**: Use proxies to distribute requests across multiple IP addresses.
- **User-Agent Rotation**: Change user-agents frequently to avoid detection.

## License

SmartScrape is licensed under the MIT License. See the `LICENSE` file for more details.
