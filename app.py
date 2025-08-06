from flask import Flask, render_template, request
import sqlite3
import json
import os


app = Flask(__name__)


# Enable Jinja2 'do' extension
app.jinja_env.add_extension('jinja2.ext.do')

# Register custom filter for translation
def translate_filter(text, translations_dict):
    key = text.lower().replace(' ', '_')
    return translations_dict.get(key, text)

app.jinja_env.filters['translate'] = translate_filter


def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn


def load_translations(lang):
    try:
        with open(f'translations/{lang}.json', 'r', encoding='utf-8') as f:
            translations = json.load(f)
        print(f"Loaded translations for {lang}: {translations.keys()}")  # Debug line
        required_keys = [
            'category_crop_production_and_productivity',
            'category_irrigation_and_water_management',
            'category_credit_and_insurance',
            'category_agricultural_marketing_and_value_chain_development',
            'category_allied_sectors_livestock_fisheries_etc',
            'category_research_education_and_extension',
            'category_infrastructure_development',
            'category_welfare_and_direct_benefit_transfer_dbt',
            'nav_crops',
            'crops_title',
            'select_region',
            'crop_schemes_title',
            'download_document',
            'select_language'
        ]
        for key in required_keys:
            if key not in translations:
                print(f"Warning: Missing translation key {key} in {lang}.json")
        return translations
    except FileNotFoundError:
        print(f"Error: {lang}.json not found, falling back to en.json")
        with open('translations/en.json', 'r', encoding='utf-8') as f:
            return json.load(f)


@app.route('/')
def index():
    lang = request.args.get('lang', 'en')
    translations = load_translations(lang)
    return render_template('index.html', translations=translations, lang=lang)


@app.route('/schemes')
def schemes():
    lang = request.args.get('lang', 'en')
    translations = load_translations(lang)
    conn = get_db_connection()
    cursor = conn.cursor()
   
    categories = [
        'Crop Production and Productivity',
        'Irrigation and Water Management',
        'Credit and Insurance',
        'Agricultural Marketing and Value Chain Development',
        'Allied Sectors (Livestock, Fisheries, etc.)',
        'Research, Education, and Extension',
        'Infrastructure Development',
        'Welfare and Direct Benefit Transfer (DBT)'
    ]
   
    categorized_schemes = {}
    for category in categories:
        if lang == 'en':
            cursor.execute('''
                SELECT name_en AS name, description_en AS description,
                       eligibility_en AS eligibility, category , website_url, document_url
                FROM schemes
                WHERE category = ?
            ''', (category,))
        else:
            cursor.execute('''
                SELECT COALESCE(st.name, s.name_en) AS name,
                       COALESCE(st.description, s.description_en) AS description,
                       COALESCE(st.eligibility, s.eligibility_en) AS eligibility,
                       s.category , s.website_url, s.document_url
                FROM schemes s
                LEFT JOIN scheme_translations st ON s.id = st.scheme_id AND st.language = ?
                WHERE s.category = ?
                GROUP BY s.id
            ''', (lang, category))
        schemes = cursor.fetchall()
        categorized_schemes[category] = schemes
   
    conn.close()
    return render_template('schemes.html', translations=translations,
                          categorized_schemes=categorized_schemes, lang=lang)


@app.route('/crops', methods=['GET', 'POST'])
def crops():
    lang = request.args.get('lang', 'en')
    translations = load_translations(lang)
    conn = get_db_connection()
    cursor = conn.cursor()
   
    # Get regions
    if lang == 'en':
        cursor.execute('SELECT id, name_en AS name FROM regions')
    else:
        cursor.execute('''
            SELECT r.id, COALESCE(rt.name, r.name_en) AS name
            FROM regions r
            LEFT JOIN region_translations rt ON r.id = rt.region_id AND rt.language = ?
        ''', (lang,))
    regions = cursor.fetchall()
   
    # Get selected region
    region_id = request.form.get('region_id') if request.method == 'POST' else None
    crops = []
    if region_id:
        if lang == 'en':
            cursor.execute('''
                SELECT c.id, c.name_en AS name, c.image_path
                FROM crops c
                WHERE c.region_id = ?
            ''', (region_id,))
        else:
            cursor.execute('''
                SELECT c.id, COALESCE(ct.name, c.name_en) AS name, c.image_path
                FROM crops c
                LEFT JOIN crop_translations ct ON c.id = ct.crop_id AND ct.language = ?
                WHERE c.region_id = ?
            ''', (lang, region_id))
        crops = cursor.fetchall()
        for crop in crops:
            if not crop['id']:
                print(f"Warning: Crop with name={crop['name']} has no ID")
                print(f"Crops fetched: {[dict(c) for c in crops]}")

    conn.close()
    return render_template('crops.html', translations=translations, regions=regions,
                          crops=crops, selected_region=region_id, lang=lang)


@app.route('/crop_schemes/<int:crop_id>')
def crop_schemes(crop_id):
    lang = request.args.get('lang', 'en')
    print(f"Received crop_id: {crop_id}, lang: {lang}")
    translations = load_translations(lang)
    conn = get_db_connection()
    cursor = conn.cursor()
   
    # Get crop name
    cursor.execute('SELECT name_en FROM crops WHERE id = ?', (crop_id,))
    crop = cursor.fetchone()
    crop_name = crop['name_en'] if crop else 'Unknown Crop'
   
# Get schemes for the crop
    if lang == 'en':
        cursor.execute('''
            SELECT s.name_en AS name, s.description_en AS description,
                   s.eligibility_en AS eligibility, s.category, s.document_url
            FROM schemes s
            JOIN crop_schemes cs ON s.id = cs.scheme_id
            WHERE cs.crop_id = ?
        ''', (crop_id,))
    else:
        cursor.execute('''
            SELECT COALESCE(st.name, s.name_en) AS name,
                   COALESCE(st.description, s.description_en) AS description,
                   COALESCE(st.eligibility, s.eligibility_en) AS eligibility,
                   s.category, s.document_url
            FROM schemes s
            JOIN crop_schemes cs ON s.id = cs.scheme_id
            LEFT JOIN scheme_translations st ON s.id = st.scheme_id AND st.language = ?
            WHERE cs.crop_id = ?
        ''', (lang, crop_id))
   
    schemes = cursor.fetchall()
    conn.close()
    return render_template('crop_schemes.html', translations=translations,
                          schemes=schemes, crop_name=crop_name, lang=lang, crop_id=crop_id)




@app.route('/helplines')
def helplines():
    lang = request.args.get('lang', 'en')
    translations = load_translations(lang)
    return render_template('helplines.html', translations=translations, lang=lang)




@app.route('/banks')
def banks():
    lang = request.args.get('lang', 'en')
    translations = load_translations(lang)
    return render_template('banks.html', translations=translations, lang=lang)




if __name__ == '__main__':
    app.run(debug=True)






