import sqlite3

# Connect to database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Drop existing tables
cursor.execute('DROP TABLE IF EXISTS crop_schemes')
cursor.execute('DROP TABLE IF EXISTS crops')
cursor.execute('DROP TABLE IF EXISTS regions')
cursor.execute('DROP TABLE IF EXISTS scheme_translations')
cursor.execute('DROP TABLE IF EXISTS crop_translations')
cursor.execute('DROP TABLE IF EXISTS schemes')

# Create schemes table
cursor.execute('''
    CREATE TABLE schemes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_en TEXT NOT NULL,
        description_en TEXT NOT NULL,
        eligibility_en TEXT NOT NULL,
        category TEXT NOT NULL,
        website_url TEXT,
        document_url TEXT       
               
    )
''')

# Create scheme_translations table
cursor.execute('''
    CREATE TABLE scheme_translations (
        scheme_id INTEGER,
        language TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        eligibility TEXT NOT NULL,
        FOREIGN KEY (scheme_id) REFERENCES schemes(id),
        PRIMARY KEY (scheme_id, language)
    )
''')

# Create regions table
cursor.execute('''
    CREATE TABLE regions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_en TEXT NOT NULL
    )
''')

# Create crops table
cursor.execute('''
    CREATE TABLE crops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_en TEXT NOT NULL,
        image_path TEXT NOT NULL,
        region_id INTEGER,
        FOREIGN KEY (region_id) REFERENCES regions(id)
    )
''')

cursor.execute('''
    CREATE TABLE crop_translations (
        crop_id INTEGER,
        language TEXT NOT NULL,
        name TEXT NOT NULL,
        image_path TEXT NOT NULL,
        region_id INTEGER,
        
        FOREIGN KEY (crop_id) REFERENCES schemes(id),
        PRIMARY KEY (crop_id, language)
    )
''')

###
# Drop existing region_translations table
cursor.execute('DROP TABLE IF EXISTS region_translations')
# Create region_translations table
cursor.execute('''
    CREATE TABLE region_translations (
        region_id INTEGER,
        language TEXT NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (region_id) REFERENCES regions(id),
        PRIMARY KEY (region_id, language)
    )
''')

# Create crop_schemes table (many-to-many)
cursor.execute('''
    CREATE TABLE crop_schemes (
        crop_id INTEGER,
        scheme_id INTEGER,
        FOREIGN KEY (crop_id) REFERENCES crops(id),
        FOREIGN KEY (scheme_id) REFERENCES schemes(id),
        PRIMARY KEY (crop_id, scheme_id)
    )
''')

# Insert regions
regions = [
    ('Dodballapura',),
    ('Chikkamagaluru',),
    ('Raichur',)
]
cursor.executemany('INSERT INTO regions (name_en) VALUES (?)', regions)
###
# Insert region translations
region_translations = [
    (1, 'hi', 'दोडबल्लापुर'),  # Dodballapura in Hindi
    (1, 'kn', 'ದೊಡ್ಡಬಳ್ಳಾಪುರ'),  # Dodballapura in Kannada
    (2, 'hi', 'चिक्कमगलुरु'),  # Chikkamagaluru in Hindi
    (2, 'kn', 'ಚಿಕ್ಕಮಗಳೂರು'),  # Chikkamagaluru in Kannada
    (3, 'hi', 'रायचूर'),  # Raichur in Hindi
    (3, 'kn', 'ರಾಯಚೂರು')  # Raichur in Kannada
]
cursor.executemany('''
    INSERT INTO region_translations (region_id, language, name)
    VALUES (?, ?, ?)
''', region_translations)


# Insert schemes (from previous + new from document)
schemes = [
    # Existing schemes from previous setup
    ('Paramparagat Krishi Vikas Yojana (PKVY)', 'Promotes organic farming through cluster-based approach; financial assistance for organic inputs and certification.', 'All farmers willing to adopt organic farming practices; preference to small and marginal farmers.', 'Crop Production and Productivity',"https://drive.google.com/file/d/10JTpPwnPdkcei5cB5aGvRAEmI1EhiTGV/view?usp=drive_link","https://www.pgsindia-ncof.gov.in/ "),
    ('National Food Security Mission (NFSM)', 'Increases production of rice, wheat, pulses, and coarse cereals through improved technology and input support.', 'Farmers in identified districts with potential for yield improvement; implementation by State Governments.', 'Crop Production and Productivity',"https://drive.google.com/file/d/1LZpf1ieIoD8NfRi7Y1v0JYr7guqsdgVl/view?usp=drive_link","https://www.nfsm.gov.in/"),
    ('Soil Health Card Scheme', 'Provides detailed soil health report with nutrient recommendations every 2 years.', 'All farmers across the country; implemented by State Departments of Agriculture.', 'Crop Production and Productivity',"https://drive.google.com/file/d/15UTKL1chT3nHD0K9YBZbP1IF8n4hCLkp/view?usp=drive_link","https://soilhealth.dac.gov.in/home"),
    ('Sub-Mission on Seeds and Planting Material (SMSP)', 'Promotes production and distribution of quality seeds with financial assistance for infrastructure and certification.', 'Seed producing agencies, farmers, and private sector entities involved in seed production.', 'Crop Production and Productivity',"https://drive.google.com/file/d/1ygTQdxgW6jIsqPMplnGCUF7VO3vAZ3kD/view?usp=drive_link","https://agriwelfare.gov.in/en/SeedsDiv"),
    ('Mission for Integrated Development of Horticulture (MIDH)', 'Supports development of horticulture crops and cold chain infrastructure.', 'Farmers, SHGs, cooperatives, and private entrepreneurs in horticulture.', 'Crop Production and Productivity',"https://drive.google.com/file/d/1FZbraH_tM015U6-8p_z81SqltptgwiTG/view?usp=drive_link","https://midh.gov.in/"),
    ('Pradhan Mantri Krishi Sinchai Yojana (PMKSY)', 'Ensures irrigation coverage and water-use efficiency; includes micro-irrigation, watershed, and canal projects.', 'All farmers; implemented through states with convergence of resources from related schemes.', 'Irrigation and Water Management',None,"https://pmksy.gov.in/"),
    ('Per Drop More Crop (PDMC)', 'Focused on micro-irrigation (drip and sprinkler) to save water and increase yield.', 'Farmers adopting micro-irrigation technologies; financial assistance provided by government.', 'Irrigation and Water Management',None,"https://pdmc.da.gov.in/"),
    ('Command Area Development and Water Management (CADWM)', 'Improves water use efficiency in irrigation commands through field channels and water users associations.', 'Farmers in command areas of major and medium irrigation projects.', 'Irrigation and Water Management',None,"https://cadwm.gov.in/"),
    ('Watershed Development Component (WDC-PMKSY)', 'Promotes rainwater harvesting, soil and moisture conservation in rainfed areas.', 'Farmers in watershed development areas, especially in hilly and dry regions.', 'Irrigation and Water Management',None,"https://wdcpmksy.dolr.gov.in/"),
    ('Accelerated Irrigation Benefit Programme (AIBP)', 'Provides central assistance for faster completion of irrigation projects.', 'State governments implementing major/medium irrigation projects.', 'Irrigation and Water Management',None,"https://pmksy-mowr.nic.in/aibp-mis/"),
    ('Kisan Credit Card (KCC)', 'Provides affordable credit to farmers for agricultural and allied activities.', 'Farmers, tenant farmers, and sharecroppers with valid land documents.', 'Credit and Insurance',None,"https://fasalrin.gov.in/"),
    ('Agricultural Marketing Infrastructure (AMI)', 'Supports development of market infrastructure like warehouses and cold storages.', 'Farmers, cooperatives, and private entities involved in agricultural marketing.', 'Agricultural Marketing and Value Chain Development',None,"https://dmi.gov.in/Schemeamigs.aspx"),
    ('National Livestock Mission', 'Supports livestock, poultry, and fodder development to enhance farmer income.', 'Farmers engaged in livestock, poultry, or fodder production.', 'Allied Sectors (Livestock, Fisheries, etc.)',None,"https://nlm.udyamimitra.in/"),
    ('Krishi Vigyan Kendra (KVK)', 'Offers training, demonstrations, and extension services to promote modern farming practices.', 'Farmers, rural youth, and extension workers.', 'Research, Education, and Extension',None,"https://icar.org.in/en/krishi-vigyan-kendras"),
    ('Rural Infrastructure Development Fund (RIDF)', 'Provides loans for rural infrastructure like warehouses and cold storage to support agriculture.', 'State governments and eligible institutions; benefits farmers indirectly.', 'Infrastructure Development',None,"https://www.nabard.org/content1.aspx?id=573&catid=8&mid=8"),
    ('PM-KISAN', 'Provides ₹6,000 per year in three installments to support farmers’ income.', 'Indian farmers owning up to 2 hectares of land with a bank account and Aadhaar.', 'Welfare and Direct Benefit Transfer (DBT)',None,"https://pmkisan.gov.in/homenew.aspx?aspxerrorpath=/BeneficiaryStatus_New.aspx"),
    # New schemes from document
    ('PM Fasal Bima Yojana', 'Crop insurance against losses due to natural calamities, pests, or diseases.', 'Farmers growing notified crops in notified areas; premium shared with government.', 'Credit and Insurance',None,"https://pmfby.gov.in/"),
    ('Rashtriya Krishi Vikas Yojana (RKVY)', 'Supports general crop development and diversification through state-specific agricultural strategies.', 'Farmers and state governments implementing agricultural projects.', 'Crop Production and Productivity',"https://drive.google.com/file/d/1maotq9LUUJDOcsHzqjzO6MO8cFwuqWSQ/view?usp=drive_link","https://rkvy.da.gov.in/"),
    ('State Millet Mission', 'Promotes ragi production and processing through financial and technical support.', 'Farmers growing millets, especially in Karnataka.', 'Crop Production and Productivity',"https://drive.google.com/file/d/1j1fh0YjdROo1J4RRrE95maLHU_FGEjzx/view?usp=drive_link","https://raitamitra.karnataka.gov.in/info-2/Organic+Farming+and+Millet+Promotional+Programs/en"),
    ('Coffee Development Programme', 'Supports coffee growers with financial aid, training, and infrastructure development.', 'Coffee farmers and cooperatives in coffee-growing regions.', 'Crop Production and Productivity',"https://drive.google.com/file/d/11up88gB412d7wPp2wJ67WHk0rK_2EuwJ/view?usp=drive_link","https://coffeeboard.gov.in/index.aspx"),
    ('Spice Board Initiatives', 'Promotes production and export of spices like pepper and cardamom with subsidies and training.', 'Farmers growing spices, especially in hilly regions.', 'Crop Production and Productivity',"https://drive.google.com/file/d/1515xy58t1g_AcH0ILzgeeVGjiVw5Bh1_/view?usp=drive_link","https://www.indianspices.com/box5_programmes_schemes.html"),
    ('e-NAM (National Agriculture Market)', 'Facilitates online trading for better price discovery for crops like cotton and pulses.', 'Farmers and traders registered on the e-NAM platform.', 'Agricultural Marketing and Value Chain Development',None,"https://www.enam.gov.in/web/")
]

# Insert schemes
cursor.executemany('INSERT INTO schemes (name_en, description_en, eligibility_en, category,document_url, website_url) VALUES (?, ?, ?, ?, ?, ?)', schemes)

# Insert crops
crops = [
    ('Ragi (Finger Millet)', 'images/crops/ragi.jpg', 1),  # Dodballapura
    ('Groundnut', 'images/crops/groundnut.jpg', 1),
    ('Maize', 'images/crops/maize.jpg', 1),
    ('Paddy (Rice)', 'images/crops/paddy.jpg', 1),
    ('Tomato', 'images/crops/tomato.jpg', 1),
    ('Beans', 'images/crops/beans.jpg', 1),
    ('Coffee', 'images/crops/coffee.jpg', 2),  # Chikkamagaluru
    ('Arecanut', 'images/crops/arecanut.jpg', 2),
    ('Pepper', 'images/crops/pepper.jpg', 2),
    ('Cardamom', 'images/crops/cardamom.jpg', 2),
    ('Paddy (Rice)', 'images/crops/paddy.jpg', 2),
    ('Cotton', 'images/crops/cotton.jpg', 3),  # Raichur
    ('Paddy (Rice)', 'images/crops/paddy.jpg', 3),
    ('Red Gram (Tur)', 'images/crops/red_gram.jpg', 3),
    ('Jowar (Sorghum)', 'images/crops/jowar.jpg', 3),
    ('Groundnut', 'images/crops/groundnut.jpg', 3)
]


cursor.executemany('INSERT INTO crops (name_en, image_path, region_id) VALUES (?, ?, ?)', crops)

# Insert crop-schemes mappings
crop_schemes = [
    # Dodballapura: Ragi
    (1, 17),  # PM Fasal Bima Yojana
    (1, 2),   # NFSM
    (1, 19),  # State Millet Mission
    (1, 18),  # RKVY
    # Dodballapura: Groundnut
    (2, 17),  # PM Fasal Bima Yojana
    (2, 18),  # RKVY
    # Dodballapura: Maize
    (3, 17),  # PM Fasal Bima Yojana
    (3, 2),   # NFSM
    (3, 18),  # RKVY
    # Dodballapura: Paddy
    (4, 17),  # PM Fasal Bima Yojana
    (4, 2),   # NFSM
    (4, 18),  # RKVY
    # Dodballapura: Tomato
    (5, 1),   # PKVY
    (5, 17),  # PM Fasal Bima Yojana
    (5, 18),  # RKVY
    # Dodballapura: Beans
    (6, 1),   # PKVY
    (6, 17),  # PM Fasal Bima Yojana
    (6, 18),  # RKVY
    # Chikkamagaluru: Coffee
    (7, 20),  # Coffee Development Programme
    (7, 17),  # PM Fasal Bima Yojana
    (7, 5),   # MIDH
    # Chikkamagaluru: Arecanut
    (8, 5),   # MIDH
    (8, 17),  # PM Fasal Bima Yojana
    # Chikkamagaluru: Pepper
    (9, 21),  # Spice Board Initiatives
    (9, 5),   # MIDH
    (9, 17),  # PM Fasal Bima Yojana
    # Chikkamagaluru: Cardamom
    (10, 21), # Spice Board Initiatives
    (10, 5),  # MIDH
    (10, 17), # PM Fasal Bima Yojana
    # Chikkamagaluru: Paddy
    (11, 17), # PM Fasal Bima Yojana
    (11, 6),  # PMKSY
    (11, 2),  # NFSM
    # Raichur: Cotton
    (12, 17), # PM Fasal Bima Yojana
    (12, 18), # RKVY
    (12, 22), # e-NAM
    # Raichur: Paddy
    (13, 17), # PM Fasal Bima Yojana
    (13, 2),  # NFSM
    (13, 18), # RKVY
    # Raichur: Red Gram
    (14, 17), # PM Fasal Bima Yojana
    (14, 2),  # NFSM
    (14, 22), # e-NAM
    # Raichur: Jowar
    (15, 17), # PM Fasal Bima Yojana
    (15, 2),  # NFSM
    (15, 18), # RKVY
    # Raichur: Groundnut
    (16, 17), # PM Fasal Bima Yojana
    (16, 18)  # RKVY
]
cursor.executemany('INSERT INTO crop_schemes (crop_id, scheme_id) VALUES (?, ?)', crop_schemes)

# Insert scheme translations
hindi_translations = [
    (1, 'hi', 'परंपरागत कृषि विकास योजना (PKVY)', 'क्लस्टर-आधारित दृष्टिकोण के माध्यम से जैविक खेती को बढ़ावा देता है; जैविक इनपुट और प्रमाणन के लिए वित्तीय सहायता।', 'जैविक खेती अपनाने के इच्छुक सभी किसान; छोटे और सीमांत किसानों को प्राथमिकता।'),
    (2, 'hi', 'राष्ट्रीय खाद्य सुरक्षा मिशन (NFSM)', 'बलुशाली तकनीक और इनपुट समर्थन के माध्यम से चावल, गेहूं, दालों, और मोटे अनाजों का उत्पादन बढ़ाता है।', 'उपज सुधार की संभावना वाले पहचाने गए जिलों में किसान; राज्य सरकारों द्वारा कार्यान्वयन।'),
    (3, 'hi', 'मृदा स्वास्थ्य कार्ड योजना', 'हर 2 साल में पोषक तत्व सिफारिशों के साथ विस्तृत मिट्टी स्वास्थ्य रिपोर्ट प्रदान करता है।', 'देश भर के सभी किसान; राज्य कृषि विभागों द्वारा लागू।'),
    (4, 'hi', 'बीज और रोपण सामग्री पर उप-मिशन (SMSP)', 'बुनियादी ढांचे और प्रमाणन के लिए वित्तीय सहायता के साथ गुणवत्ता वाले बीजों के उत्पादन और वितरण को बढ़ावा देता है।', 'बीज उत्पादन में शामिल बीज उत्पादन एजेंसियां, किसान, और निजी क्षेत्र की संस्थाएं।'),
    (5, 'hi', 'बागवानी के एकीकृत विकास मिशन (MIDH)', 'बागवानी फसलों और कोल्ड चेन बुनियादी ढांचे के विकास का समर्थन करता है।', 'बागवानी में किसान, स्वयं सहायता समूह, सहकारी समितियां, और निजी उद्यमी।'),
    (6, 'hi', 'प्रधानमंत्री कृषि सिंचाई योजना (PMKSY)', 'सिंचाई कवरेज और जल-उपयोग दक्षता सुनिश्चित करता है; इसमें सूक्ष्म-सिंचाई, वाटरशेड, और नहर परियोजनाएं शामिल हैं।', 'सभी किसान; संबंधित योजनाओं से संसाधनों के अभिसरण के साथ राज्यों के माध्यम से लागू।'),
    (7, 'hi', 'प्रति बूंद अधिक फसल (PDMC)', 'पानी बचाने और उपज बढ़ाने के लिए सूक्ष्म-सिंचाई (ड्रिप और स्प्रिंकलर) पर केंद्रित।', 'सूक्ष्म-सिंचाई तकनीकों को अपनाने वाले किसान; सरकार द्वारा वित्तीय सहायता प्रदान की जाती है।'),
    (8, 'hi', 'कमांड क्षेत्र विकास और जल प्रबंधन (CADWM)', 'क्षेत्रीय चैनलों और जल उपयोगकर्ता संघों के माध्यम से सिंचाई कमांड में जल उपयोग दक्षता में सुधार करता है।', 'प्रमुख और मध्यम सिंचाई परियोजनाओं के कमांड क्षेत्रों में किसान।'),
    (9, 'hi', 'वाटरशेड विकास घटक (WDC-PMKSY)', 'वर्षा जल संचयन, मिट्टी और नमी संरक्षण को वर्षा आधारित क्षेत्रों में बढ़ावा देता है।', 'वाटरशेड विकास क्षेत्रों में किसान, विशेष रूप से पहाड़ी और शुष्क क्षेत्रों में।'),
    (10, 'hi', 'त्वरित सिंचाई लाभ कार्यक्रम (AIBP)', 'सिंचाई परियोजनाओं को तेजी से पूरा करने के लिए केंद्रीय सहायता प्रदान करता है।', 'प्रमुख/मध्यम सिंचाई परियोजनाओं को लागू करने वाली राज्य सरकारें।'),
    (11, 'hi', 'किसान क्रेडिट कार्ड (KCC)', 'कृषि और संबद्ध गतिविधियों के लिए किसानों को सस्ता ऋण प्रदान करता है।', 'वैध भूमि दस्तावेजों वाले किसान, किरायेदार किसान, और बटाईदार।'),
    (12, 'hi', 'कृषि विपणन बुनियादी ढांचा (AMI)', 'गोदामों और कोल्ड स्टोरेज जैसे बाजार बुनियादी ढांचे के विकास का समर्थन करता है।', 'कृषि विपणन में शामिल किसान, सहकारी समितियां, और निजी संस्थाएं।'),
    (13, 'hi', 'राष्ट्रीय पशुधन मिशन', 'किसानों की आय बढ़ाने के लिए पशुधन, कुक्कुट, और चारा विकास का समर्थन करता है।', 'पशुधन, कुक्कुट, या चारा उत्पादन में लगे किसान।'),
    (14, 'hi', 'कृषि विज्ञान केंद्र (KVK)', 'आधुनिक कृषि पद्धतियों को बढ़ावा देने के लिए प्रशिक्षण, प्रदर्शन, और विस्तार सेवाएं प्रदान करता है।', 'किसान, ग्रामीण युवा, और विस्तार कार्यकर्ता।'),
    (15, 'hi', 'ग्रामीण बुनियादी ढांचा विकास निधि (RIDF)', 'कृषि का समर्थन करने के लिए गोदामों और कोल्ड स्टोरेज जैसे ग्रामीण बुनियादी ढांचे के लिए ऋण प्रदान करता है।', 'राज्य सरकारें और पात्र संस्थान; किसानों को अप्रत्यक्ष लाभ।'),
    (16, 'hi', 'PM-KISAN', 'किसानों की आय का समर्थन करने के लिए प्रति वर्ष ₹6,000 तीन किश्तों में प्रदान करता है।', '2 हेक्टेयर तक की भूमि वाले भारतीय किसान, जिनके पास बैंक खाता और आधार हो।'),
    (17, 'hi', 'PM Fasal Bima Yojana', 'प्राकृतिक आपदाओं, कीटों या रोगों के कारण फसल नुकसान के खिलाफ बीमा।', 'अधिसूचित क्षेत्रों में अधिसूचित फसलों को उगाने वाले किसान; प्रीमियम सरकार के साथ साझा।'),
    (18, 'hi', 'राष्ट्रीय कृषि विकास योजना (RKVY)', 'राज्य-विशिष्ट कृषि रणनीतियों के माध्यम से सामान्य फसल विकास और विविधीकरण का समर्थन करता है।', 'कृषि परियोजनाओं को लागू करने वाले किसान और राज्य सरकारें।'),
    (19, 'hi', 'राज्य बाजरा मिशन', 'वित्तीय और तकनीकी समर्थन के माध्यम से रागी उत्पादन और प्रसंस्करण को बढ़ावा देता है।', 'कर्नाटक में विशेष रूप से बाजरा उगाने वाले किसान।'),
    (20, 'hi', 'कॉफी विकास कार्यक्रम', 'कॉफी उत्पादकों को वित्तीय सहायता, प्रशिक्षण, और बुनियादी ढांचे के विकास के साथ समर्थन करता है।', 'कॉफी उगाने वाले क्षेत्रों में कॉफी किसान और सहकारी समितियां।'),
    (21, 'hi', 'मसाला बोर्ड पहल', 'काली मिर्च और इलायची जैसे मसालों के उत्पादन और निर्यात को सब्सिडी और प्रशिक्षण के साथ बढ़ावा देता है।', 'पहाड़ी क्षेत्रों में मसाले उगाने वाले किसान।'),
    (22, 'hi', 'ई-नाम (राष्ट्रीय कृषि बाजार)', 'कपास और दालों जैसे फसलों के लिए बेहतर मूल्य खोज के लिए ऑनलाइन व्यापार की सुविधा प्रदान करता है।', 'ई-नाम मंच पर पंजीकृत किसान और व्यापारी।')
]

kannada_translations = [
    (1, 'kn', 'ಪರಂಪರಾಗತ ಕೃಷಿ ವಿಕಾಸ ಯೋಜನೆ (PKVY)', 'ಕ್ಲಸ್ಟರ್-ಆಧಾರಿತ ವಿಧಾನದ ಮೂಲಕ ಸಾವಯವ ಕೃಷಿಯನ್ನು ಉತ್ತೇಜಿಸುತ್ತದೆ; ಸಾವಯವ ಒಳಹರಿವು ಮತ್ತು ಪ್ರಮಾಣೀಕರಣಕ್ಕೆ ಆರ್ಥಿಕ ಸಹಾಯ.', 'ಸಾವಯವ ಕೃಷಿಯನ್ನು ಅಳವಡಿಸಿಕೊಳ್ಳಲು ಇಚ್ಛಿಸುವ ಎಲ್ಲಾ ರೈತರು; ಸಣ್ಣ ಮತ್ತು ಅಂಚಿನ ರೈತರಿಗೆ ಆದ್ಯತೆ.'),
    (2, 'kn', 'ರಾಷ್ಟ್ರೀಯ ಆಹಾರ ಭದ್ರತಾ ಮಿಷನ್ (NFSM)', 'ಉನ್ನತ ತಂತ್ರಜ್ಞಾನ ಮತ್ತು ಒಳಹರಿವು ಸಮರ್ಥನೆಯ ಮೂಲಕ ಅಕ್ಕಿ, ಗೋಧಿ, ದ್ವಿದಳ ಧಾನ್ಯಗಳು, ಮತ್ತು ಒರಟು ಧಾನ್ಯಗಳ ಉತ್ಪಾದನೆಯನ್ನು ಹೆಚ್ಚಿಸುತ್ತದೆ.', 'ಉತ್ಪಾದನೆ ಸುಧಾರಣೆಯ ಸಾಮರ್ಥ್ಯವಿರುವ ಗುರುತಿಸಲಾದ ಜಿಲ್ಲೆಗಳಲ್ಲಿ ರೈತರು; ರಾಜ್ಯ ಸರ್ಕಾರಗಳಿಂದ ಜಾರಿಗೊಳಿಸಲಾಗುತ್ತದೆ.'),
    (3, 'kn', 'ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಕಾರ್ಡ್ ಯೋಜನೆ', 'ಪ್ರತಿ 2 ವರ್ಷಗಳಿಗೊಮ್ಮೆ ಪೋಷಕಾಂಶ ಶಿಫಾರಸುಗಳೊಂದಿಗೆ ವಿವರವಾದ ಮಣ್ಣಿನ ಆರೋಗ್ಯ ವರದಿಯನ್ನು ಒದಗಿಸುತ್ತದೆ.', 'ದೇಶಾದ್ಯಂತ ಎಲ್ಲಾ ರೈತರು; ರಾಜ್ಯ ಕೃಷಿ ಇಲಾಖೆಗಳಿಂದ ಜಾರಿಗೊಳಿಸಲಾಗುತ್ತದೆ.'),
    (4, 'kn', 'ಬೀಜ ಮತ್ತು ನಾಟಿ ಸಾಮಗ್ರಿ ಉಪ-ಮಿಷನ್ (SMSP)', 'ಬುನಿಯಾದಿ ಸೌಕರ್ಯ ಮತ್ತು ಪ್ರಮಾಣೀಕರಣಕ್ಕೆ ಆರ್ಥಿಕ ಸಹಾಯದೊಂದಿಗೆ ಗುಣಮಟ್ಟದ ಬೀಜಗಳ ಉತ್ಪಾದನೆ ಮತ್ತು ವಿತರಣೆಯನ್ನು ಉತ್ತೇಜಿಸುತ್ತದೆ.', 'ಬೀಜ ಉತ್ಪಾದನೆಯಲ್ಲಿ ತೊಡಗಿರುವ ಬೀಜ ಉತ್ಪಾದನಾ ಸಂಸ್ಥೆಗಳು, ರೈತರು, ಮತ್ತು ಖಾಸಗಿ ವಲಯದ ಸಂಸ್ಥೆಗಳು.'),
    (5, 'kn', 'ಬಾಗವಾನಿಕೆಯ ಏಕೀಕೃತ ಅಭಿವೃದ್ಧಿ ಮಿಷನ್ (MIDH)', 'ಬಾಗವಾನಿಕೆ ಬೆಳೆಗಳು ಮತ್ತು ಕೋಲ್ಡ್ ಚೇನ್ ಬುನಿಯಾದಿ ಸೌಕರ್ಯದ ಅಭಿವೃದ್ಧಿಯನ್ನು ಬೆಂಬಲಿಸುತ್ತದೆ.', 'ಬಾಗವಾನಿಕೆಯಲ್ಲಿ ರೈತರು, ಸ್ವಯಂ ಸಹಾಯ ಗುಂಪುಗಳು, ಸಹಕಾರಿ ಸಂಸ್ಥೆಗಳು, ಮತ್ತು ಖಾಸಗಿ ಉದ್ಯಮಿಗಳು.'),
    (6, 'kn', 'ಪ್ರಧಾನಮಂತ್ರಿ ಕೃಷಿ ಸಿಂಚಾಯಿ ಯೋಜನೆ (PMKSY)', 'ನೀರಾವರಿ ವ್ಯಾಪ್ತಿ ಮತ್ತು ನೀರಿನ ಬಳಕೆ ದಕ್ಷತೆಯನ್ನು ಖಾತರಿಪಡಿಸುತ್ತದೆ; ಸೂಕ್ಷ್ಮ-ನೀರಾವರಿ, ಜಲಾನಯನ, ಮತ್ತು ಕಾಲುವೆ ಯೋಜನೆಗಳನ್ನು ಒಳಗೊಂಡಿದೆ.', 'ಎಲ್ಲಾ ರೈತರು; ಸಂಬಂಧಿತ ಯೋಜನೆಗಳಿಂದ ಸಂಪನ್ಮೂಲಗಳ ಸಂಗಮದೊಂದಿಗೆ ರಾಜ್ಯಗಳ ಮೂಲಕ ಜಾರಿಗೊಳಿಸಲಾಗುತ್ತದೆ.'),
    (7, 'kn', 'ಪ್ರತಿ ಹನಿ ಹೆಚ್ಚು ಬೆಳೆ (PDMC)', 'ನೀರನ್ನು ಉಳಿಸಲು ಮತ್ತು ಇಳುವರಿಯನ್ನು ಹೆಚ್ಚಿಸಲು ಸೂಕ್ಷ್ಮ-ನೀರಾವರಿ (ಡ್ರಿಪ್ ಮತ್ತು ಸ್ಪ್ರಿಂಕ್ಲರ್) ಮೇಲೆ ಕೇಂದ್ರೀಕರಿಸಿದೆ.', 'ಸೂಕ್ಷ್ಮ-ನೀರಾವರಿ ತಂತ್ರಜ್ಞಾನಗಳನ್ನು ಅಳವಡಿಸಿಕೊಂಡ ರೈತರು; ಸರ್ಕಾರದಿಂದ ಆರ್ಥಿಕ ಸಹಾಯ ಒದಗಿಸಲಾಗುತ್ತದೆ.'),
    (8, 'kn', 'ಕಮಾಂಡ್ ಏರಿಯಾ ಡೆವಲಪ್‌ಮೆಂಟ್ ಮತ್ತು ವಾಟರ್ ಮ್ಯಾನೇಜ್‌ಮೆಂಟ್ (CADWM)', 'ಕ್ಷೇತ್ರ ಕಾಲುವೆಗಳು ಮತ್ತು ನೀರಿನ ಬಳಕೆದಾರರ ಸಂಘಗಳ ಮೂಲಕ ನೀರಾವರಿ ಕಮಾಂಡ್‌ಗಳಲ್ಲಿ ನೀರಿನ ಬಳಕೆ ದಕ್ಷತೆಯನ್ನು ಸುಧಾರಿಸುತ್ತದೆ.', 'ಪ್ರಮುಖ ಮತ್ತು ಮಧ್ಯಮ ನೀರಾವರಿ ಯೋಜನೆಗಳ ಕಮಾಂಡ್ ಪ್ರದೇಶಗಳಲ್ಲಿ ರೈತರು.'),
    (9, 'kn', 'ಜಲಾನಯನ ಅಭಿವೃದ್ಧಿ ಘಟಕ (WDC-PMKSY)', 'ವರ್ಷಾಧಾರಿತ ಪ್ರದೇಶಗಳಲ್ಲಿ ವರ್ಷದ ನೀರಿನ ಕೊಯ್ಲು, ಮಣ್ಣು ಮತ್ತು ತೇವಾಂಶ ಸಂರಕ್ಷಣೆಯನ್ನು ಉತ್ತೇಜಿಸುತ್ತದೆ.', 'ಜಲಾನಯನ ಅಭಿವೃದ್ಧಿ ಪ್ರದೇಶಗಳಲ್ಲಿ ರೈತರು, ವಿಶೇಷವಾಗಿ ಬೆಟ್ಟದ ಮತ್ತು ಒಣ ಪ್ರದೇಶಗಳಲ್ಲಿ.'),
    (10, 'kn', 'ತ್ವರಿತ ನೀರಾವರಿ ಲಾಭ ಕಾರ್ಯಕ್ರಮ (AIBP)', 'ನೀರಾವರಿ ಯೋಜನೆಗಳನ್ನು ಶೀಘ್ರವಾಗಿ ಪೂರ್ಣಗೊಳಿಸಲು ಕೇಂದ್ರೀಯ ಸಹಾಯವನ್ನು ಒದಗಿಸುತ್ತದೆ.', 'ಪ್ರಮುಖ/ಮಧ್ಯಮ ನೀರಾವರಿ ಯೋಜನೆಗಳನ್ನು ಜಾರಿಗೊಳಿಸುವ ರಾಜ್ಯ ಸರ್ಕಾರಗಳು.'),
    (11, 'kn', 'ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ (KCC)', 'ಕೃಷಿ ಮತ್ತು ಸಂಬಂಧಿತ ಚಟುವಟಿಕೆಗಳಿಗೆ ರೈತರಿಗೆ ಕೈಗೆಟುಕುವ ಸಾಲವನ್ನು ಒದಗಿಸುತ್ತದೆ.', 'ಮಾನ್ಯ ಭೂಮಿ ದಾಖಲೆಗಳನ್ನು ಹೊಂದಿರುವ ರೈತರು, ಗುತ್ತಿಗೆ ರೈತರು, ಮತ್ತು ಬಾಡಿಗೆದಾರರು.'),
    (12, 'kn', 'ಕೃಷಿ ಮಾರ್ಕೆಟಿಂಗ್ ಇನ್‌ಫ್ರಾಸ್ಟ್ರಕ್ಚರ್ (AMI)', 'ಗೋದಾಮುಗಳು ಮತ್ತು ಕೋಲ್ಡ್ ಸ್ಟೋರೇಜ್‌ನಂತಹ ಮಾರುಕಟ್ಟೆ ಬುನಿಯಾದಿ ಸೌಕರ್ಯದ ಅಭಿವೃದ್ಧಿಯನ್ನು ಬೆಂಬಲಿಸುತ್ತದೆ.', 'ಕೃಷಿ ಮಾರ್ಕೆಟಿಂಗ್‌ನಲ್ಲಿ ತೊಡಗಿರುವ ರೈತರು, ಸಹಕಾರಿ ಸಂಸ್ಥೆಗಳು, ಮತ್ತು ಖಾಸಗಿ ಸಂಸ್ಥೆಗಳು.'),
    (13, 'kn', 'ರಾಷ್ಟ್ರೀಯ ಪಶುಸಂಗೋಪನೆ ಮಿಷನ್', 'ರೈತರ ಆದಾಯವನ್ನು ಹೆಚ್ಚಿಸಲು ಪಶುಸಂಗೋಪನೆ, ಕೋಳಿ, ಮತ್ತು ಮೇವಿನ ಅಭಿವೃದ್ಧಿಯನ್ನು ಬೆಂಬಲಿಸುತ್ತದೆ.', 'ಪಶುಸಂಗೋಪನೆ, ಕೋಳಿ, ಅಥವಾ ಮೇವು ಉತ್ಪಾದನೆಯಲ್ಲಿ ತೊಡಗಿರುವ ರೈತರು.'),
    (14, 'kn', 'ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರ (KVK)', 'ಆಧುನಿಕ ಕೃಷಿ ಪದ್ಧತಿಗಳನ್ನು ಉತ್ತೇಜಿಸಲು ತರಬೇತಿ, ಪ್ರದರ್ಶನಗಳು, ಮತ್ತು ವಿಸ್ತರಣೆ ಸೇವೆಗಳನ್ನು ನೀಡುತ್ತದೆ.', 'ರೈತರು, ಗ್ರಾಮೀಣ ಯುವಕರು, ಮತ್ತು ವಿಸ್ತರಣೆ ಕಾರ್ಯಕರ್ತರು.'),
    (15, 'kn', 'ಗ್ರಾಮೀಣ ಮೂಲಭೂತ ಸೌಕರ್ಯ ಅಭಿವೃದ್ಧಿ ನಿಧಿ (RIDF)', 'ಕೃಷಿಯನ್ನು ಬೆಂಬಲಿಸಲು ಗೋದಾಮುಗಳು ಮತ್ತು ಕೋಲ್ಡ್ ಸ್ಟೋರೇಜ್‌ನಂತಹ ಗ್ರಾಮೀಣ ಮೂಲಭೂತ ಸೌಕರ್ಯಕ್ಕೆ ಸಾಲಗಳನ್ನು ಒದಗಿಸುತ್ತದೆ.', 'ರಾಜ್ಯ ಸರ್ಕಾರಗಳು ಮತ್ತು ಯೋಗ್ಯ ಸಂಸ್ಥೆಗಳು; ರೈತರಿಗೆ ಪರೋಕ್ಷವಾಗಿ ಲಾಭ.'),
    (16, 'kn', 'PM-KISAN', 'ರೈತರ ಆದಾಯವನ್ನು ಬೆಂಬಲಿಸಲು ವರ್ಷಕ್ಕೆ ₹6,000 ಮೂರು ಕಂತುಗಳಲ್ಲಿ ನೀಡುತ್ತದೆ.', '2 ಹೆಕ್ಟೇರ್‌ವರೆಗಿನ ಭೂಮಿ ಹೊಂದಿರುವ ಭಾರತೀಯ ರೈತರು, ಬ್ಯಾಂಕ್ ಖಾತೆ ಮತ್ತು ಆಧಾರ್ ಹೊಂದಿರಬೇಕು.'),
    (17, 'kn', 'PM Fasal Bima Yojana', 'ನೈಸರ್ಗಿಕ ವಿಪತ್ತುಗಳು, ಕೀಟಗಳು ಅಥವಾ ರೋಗಗಳಿಂದ ಬೆಳೆ ನಷ್ಟಕ್ಕೆ ವಿಮೆ.', 'ಅಧಿಸೂಚಿತ ಪ್ರದೇಶಗಳಲ್ಲಿ ಅಧಿಸೂಚಿತ ಬೆಳೆಗಳನ್ನು ಬೆಳೆಯುವ ರೈತರು; ಪ್ರೀಮಿಯಂ ಸರ್ಕಾರದೊಂದಿಗೆ ಹಂಚಿಕೆ.'),
    (18, 'kn', 'ರಾಷ್ಟ್ರೀಯ ಕೃಷಿ ವಿಕಾಸ ಯೋಜನೆ (RKVY)', 'ರಾಜ್ಯ-ನಿರ್ದಿಷ್ಟ ಕೃಷಿ ಕಾರ್ಯತಂತ್ರಗಳ ಮೂಲಕ ಸಾಮಾನ್ಯ ಬೆಳೆ ಅಭಿವೃದ್ಧಿ ಮತ್ತು ವೈವಿಧ್ಯೀಕರಣವನ್ನು ಬೆಂಬಲಿಸುತ್ತದೆ.', 'ಕೃಷಿ ಯೋಜನೆಗಳನ್ನು ಜಾರಿಗೊಳಿಸುವ ರೈತರು ಮತ್ತು ರಾಜ್ಯ ಸರ್ಕಾರಗಳು.'),
    (19, 'kn', 'ರಾಜ್ಯ ರಾಗಿ ಮಿಷನ್', 'ಆರ್ಥಿಕ ಮತ್ತು ತಾಂತ್ರಿಕ ಬೆಂಬಲದ ಮೂಲಕ ರಾಗಿ ಉತ್ಪಾದನೆ ಮತ್ತು ಸಂಸ್ಕರಣೆಯನ್ನು ಉತ್ತೇಜಿಸುತ್ತದೆ.', 'ಕರ್ನಾಟಕದಲ್ಲಿ ವಿಶೇಷವಾಗಿ ರಾಗಿ ಬೆಳೆಯುವ ರೈತರು.'),
    (20, 'kn', 'ಕಾಫಿ ಅಭಿವೃದ್ಧಿ ಕಾರ್ಯಕ್ರಮ', 'ಕಾಫಿ ಉತ್ಪಾದಕರಿಗೆ ಆರ್ಥಿಕ ಸಹಾಯ, ತರಬೇತಿ, ಮತ್ತು ಬುನಿಯಾದಿ ಸೌಕರ್ಯ ಅಭಿವೃದ್ಧಿಯೊಂದಿಗೆ ಬೆಂಬಲ ನೀಡುತ್ತದೆ.', 'ಕಾಫಿ ಬೆಳೆಯುವ ಪ್ರದೇಶಗಳಲ್ಲಿ ಕಾಫಿ ರೈತರು ಮತ್ತು ಸಹಕಾರಿ ಸಂಸ್ಥೆಗಳು.'),
    (21, 'kn', 'ಮಸಾಲೆ ಬೋರ್ಡ್ ಉಪಕ್ರಮಗಳು', 'ಕಾಳುಮೆಣಸು ಮತ್ತು ಏಲಕ್ಕಿ ರೀತಿಯ ಮಸಾಲೆಗಳ ಉತ್ಪಾದನೆ ಮತ್ತು ರಫ್ತನ್ನು ಸಹಾಯಧನ ಮತ್ತು ತರಬೇತಿಯೊಂದಿಗೆ ಉತ್ತೇಜಿಸುತ್ತದೆ.', 'ಬೆಟ್ಟದ ಪ್ರದೇಶಗಳಲ್ಲಿ ಮಸಾಲೆ ಬೆಳೆಯುವ ರೈತರು.'),
    (22, 'kn', 'ಇ-ನಾಮ್ (ರಾಷ್ಟ್ರೀಯ ಕೃಷಿ ಮಾರುಕಟ್ಟೆ)', 'ಕಪಾಸು ಮತ್ತು ದ್ವಿದಳ ಧಾನ್ಯಗಳಂತಹ ಬೆಳೆಗಳಿಗೆ ಉತ್ತಮ ಬೆಲೆ ಕಂಡುಕೊಳ್ಳಲು ಆನ್‌ಲೈನ್ ವ್ಯಾಪಾರವನ್ನು ಸುಗಮಗೊಳಿಸುತ್ತದೆ.', 'ಇ-ನಾಮ್ ವೇದಿಕೆಯಲ್ಲಿ ನೋಂದಾಯಿತ ರೈತರು ಮತ್ತು ವ್ಯಾಪಾರಿಗಳು.')
]

# Insert translations
cursor.executemany('''
    INSERT INTO scheme_translations (scheme_id, language, name, description, eligibility)
    VALUES (?, ?, ?, ?, ?)
''', hindi_translations + kannada_translations)

#crop translations
hi_tran=[
    (1,'hi','नाचनी', 'images/crops/ragi.jpg', 1),  # Dodballapura
    (2,'hi','मूंगफली', 'images/crops/groundnut.jpg', 1),
    (3,'hi','मक्का', 'images/crops/maize.jpg', 1),
    (4,'hi','चावल (धान)', 'images/crops/paddy.jpg', 1),
    (5,'hi','टमाटर', 'images/crops/tomato.jpg', 1),
    (6,'hi','बीन्स', 'images/crops/beans.jpg', 1),
    (7,'hi','कॉफी', 'images/crops/coffee.jpg', 2),  # Chikkamagaluru
    (8,'hi','सुपारी', 'images/crops/arecanut.jpg', 2),
    (9,'hi','काली मिर्च', 'images/crops/pepper.jpg', 2),
    (10,'hi','इलायची', 'images/crops/cardamom.jpg', 2),
    (11,'hi','चावल (धान)', 'images/crops/paddy.jpg', 2),
    (12,'hi','कपास', 'images/crops/cotton.jpg', 3),  # Raichur
    (13,'hi','चावल (धान)', 'images/crops/paddy.jpg', 3),
    (14,'hi','अरहर (तूर)', 'images/crops/red_gram.jpg', 3),
    (15,'hi','ज्वार', 'images/crops/jowar.jpg', 3),
    (16,'hi','मूंगफली', 'images/crops/groundnut.jpg', 3)
]
kn_tran=[
    (1,'kn','ರಾಗಿ', 'images/crops/ragi.jpg', 1),  # Dodballapura
    (2,'kn','ಕಡಲೆಕಾಯಿ', 'images/crops/groundnut.jpg', 1),
    (3,'kn','ಜೋಳ', 'images/crops/maize.jpg', 1),
    (4,'kn','ಅಕ್ಕಿ (ಬತ್ತ)', 'images/crops/paddy.jpg', 1),
    (5,'kn','ಟೊಮೆಟೊ', 'images/crops/tomato.jpg', 1),
    (6,'kn','ಹುರಿಕಾಳು', 'images/crops/beans.jpg', 1),
    (7,'kn','ಕಾಫಿ', 'images/crops/coffee.jpg', 2),  # Chikkamagaluru
    (8,'kn','ಅಡಿಕೆ', 'images/crops/arecanut.jpg', 2),
    (9,'kn','ಕಪ್ಪು ಮೆಣಸು', 'images/crops/pepper.jpg', 2),
    (10,'kn','ಏಲಕ್ಕಿ', 'images/crops/cardamom.jpg', 2),
    (11,'kn','ಅಕ್ಕಿ (ಬತ್ತ)', 'images/crops/paddy.jpg', 2),
    (12,'kn','ಬತ್ತೆ', 'images/crops/cotton.jpg', 3),  # Raichur
    (13,'kn','ಅಕ್ಕಿ (ಬತ್ತ)', 'images/crops/paddy.jpg', 3),
    (14,'kn','ತೊಗರಿ ಬೆಳೆ', 'images/crops/red_gram.jpg', 3),
    (15,'kn','ಜೋಳ', 'images/crops/jowar.jpg', 3),
    (16,'kn','ಕಡಲೆಕಾಯಿ', 'images/crops/groundnut.jpg', 3)
]
# Insert translations
cursor.executemany('''
    INSERT INTO crop_translations (crop_id, language, name, image_path, region_id)
    VALUES (?, ?, ?, ?, ?)
''', hi_tran + kn_tran)

# Commit and close
conn.commit()
conn.close()

print("Database initialized successfully!")