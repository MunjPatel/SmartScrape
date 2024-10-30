from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from scraper import GoogleSearch  # Assume GoogleSearch class is imported
import json
import pandas as pd
import os

# Load supported languages from JSON file
with open("languages.json", 'r') as languages_file:
    LANGUAGES = json.load(languages_file)

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flashing messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        language = request.form.get('language', 'en')  # Default to English
        num_results = request.form.get('num_results', 5)  # Default to 5 results
        download_format = request.form.get('download_format', 'none')  # Default to None

        # Basic form validation
        if not search_query:
            flash("Search query is required!", "error")
            return redirect(url_for('index'))
        
        try:
            num_results = int(num_results)
            if num_results < 1 or num_results > 100:
                flash("Please enter a number of results between 1 and 100.", "error")
                return redirect(url_for('index'))
        except ValueError:
            flash("Number of results must be an integer.", "error")
            return redirect(url_for('index'))

        # Perform the search
        search_tool = GoogleSearch(language=language, max_results=num_results)
        results = search_tool.search(search_query)

        # Check if results contain an error
        if isinstance(results, dict) and "error" in results:
            # If an error occurred, pass the error message and code to the template
            return render_template('results.html', error=results["error"], status_code=results.get("status_code"))

        # If no error, proceed with normal sorting and rendering
        results = sorted(results, key=lambda x: x['similarity_score'], reverse=True)
        file_path = save_results(results, download_format) if download_format != 'none' else None
        return render_template('results.html', results=results, search_query=search_query, download_format=download_format, file_path=file_path)

    return render_template('index.html', languages=LANGUAGES)

def save_results(results, format):
    """Saves the search results in the specified format and returns the file path."""
    if format == 'json':
        file_path = "search_results.json"
        with open(file_path, 'w') as f:
            json.dump(results, f)
    elif format == 'csv':
        file_path = "search_results.csv"
        df = pd.DataFrame(results)
        df.to_csv(file_path, index=False)
    elif format == 'excel':
        file_path = "search_results.xlsx"
        df = pd.DataFrame(results)
        df.to_excel(file_path, index=False, engine='xlsxwriter')
    return file_path

@app.route('/download/<format>', methods=['GET'])
def download_file(format):
    """Route to download the file in the requested format."""
    file_path = f"search_results.{format}"
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        flash(f"Error downloading file: {e}", "error")
        return redirect(url_for('index'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
