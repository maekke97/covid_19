#!/usr/bin/env python3

import scrape_common as sc

print('NE')
d = sc.download('https://www.ne.ch/autorites/DFS/SCSP/medecin-cantonal/maladies-vaccinations/Pages/Coronavirus.aspx')
sc.timestamp()
d = sc.filter('Nombre de cas confirmés', d)

# 2020-03-25
"""
</p><p style="text-align&#58;justify;">&#160;&#160;<br></p><p style="text-align&#58;justify;">Le coronavirus COVID-19 (2019-nCoV) est un nouveau coronavirus découvert en décembre 2019 dans la ville de Wuhan dans la province de Hubei au centre de la Chine et responsable d'une large épidémie&#160;de pneumonies. Ce virus est apparenté aux coronavirus responsables du SARS et du MERS.</p><p style="text-align&#58;justify;">Le virus provient probablement d'animaux sauvages, a été transmis à l'être humain et se transmet désormais de personne à personne.</p><h3>Quelle est la situation actuelle ?</h3><p style="text-align&#58;justify;">Au niveau mondial, la situation évolue rapidement depuis début janvier (<a title="Lien vers la page web de Johns Hopkins" href="https&#58;//gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6" target="_blank">carte de la situation mondiale</a>). Après la Chine, l'épidémie de maladie de coronavirus COVID-19 atteint désormais&#160;tous les continents (Asie, Europe, Amérique du Nord, Amérique du Sud, Australie, Afrique). L'Organisation mondiale de la santé (OMS)&#160;parle désormais de pandémie.</p><p style="text-align&#58;justify;">En Suisse, des&#160;&#160;cas ont&#160;été signalés dans&#160;24 cantons &#58;&#160;Appenzell Rhodes-Extérieures, Argovie, Bâle-Campagne, Bâle-Ville, Berne, Fribourg, Genève, Glaris, Grisons, Jura, Lucerne, Neuchâtel,&#160;Nidwald, Obwald, Saint-Gall, Schaffouse, Schwyz, Soleure,&#160;Tessin, Turgovie, Vaud, Valais, Zug et Zürich. </p><p style="text-align&#58;justify;"><strong><br><span class="ms-rteThemeForeColor-5-0">Suisse&#160;&#160; 25.03.2020, 08h15</span><br><strong><strong>Nombre de tests positifs &#58; 9'765<br>Nombre de décès &#58; 103<br><strong><strong><strong><strong><strong><strong><br><span class="ms-rteThemeForeColor-5-0">Neuchâtel&#160;&#160; 25.03.2020, 14h00</span><br>Nombre de cas confirmés &#58;&#160;256 personnes<br>Nombre de décès &#58; 2</strong></strong></strong></strong></strong></strong></strong></strong></strong></p><p style="text-align&#58;justify;">&#160;</p><div class="well"><h3>Pour en savoir plus...<br></h3><p style="text-align&#58;justify;">Étant donné que la situation change très rapidement, veuillez consulter la page web de l'Office fédéral de la santé publique (OFSP) pour obtenir les dernières informations sur le nouveau coronavirus COVID-19, ainsi que la liste des questions fréquemment posées &#58;</p><p style="text-align&#58;justify;">
"""

# 2020-03-25, smaller part:
"""
... <strong><strong><br><span class="ms-rteThemeForeColor-5-0">Neuchâtel&#160;&#160; 25.03.2020, 14h00</span><br>Nombre de cas confirmés &#58;&#160;256 personnes<br>Nombre de décès &#58; 2</strong></strong> ...
"""

print('Date and time:', sc.find(r'>Neuchâtel(&#160;)* +([^<]+)<\/span>', d, group=2))
# d2 = d.replace('<br>', '\n')
# Use non-greed matching in few places.
print('Confirmed cases:', sc.find(r'>Neuchâtel.+?Nombre de.*? confirmés (&#58;|&#160;| )*([0-9]+) pers', d, group=2))
print('Deaths:', sc.find(r'>Neuchâtel.+?Nombre.*? décès (&#58;|&#160;| )*([0-9]+)( pers|<)', d, group=2))

d = sc.pdfdownload('https://www.ne.ch/autorites/DFS/SCSP/medecin-cantonal/maladies-vaccinations/Documents/Covid-19-Statistiques/COVID19_PublicationInternet.pdf', layout=True)
sc.timestamp()

import re

if d:
    # Magic column fix (don't know if this is stable).
    d = d.replace('avr\n   il', 'avril')
    # d = d.replace('avr\n il', 'avril')
    # Find the start of the table on page 5.
    res = re.search('1mars2020', d)
    d = d[res.span()[0]:]
    # Replace spans of spaces by colon to indicate columns.
    d = d.replace('2020                      ', '2020:')
    d = d.replace('                    ', ':')
    d = d.replace('              ', ':')
    # Split all lines into rows and columns.
    data = [[dat.strip() for dat in line.split(':')] for line in d.split('\n')]
    for line in data:
        if len(line) < 3 or line[2] == '':
            continue
        last_row = line
        
    COLUMNS = [
        'date',
        'ncases_per_day',
        'ncumul_cases',
        'n_hospital_non_icu',
        'n_hospital_icu',
        'n_hospital_icu_non_tube',
        'n_hospital_icu_tube',
        'n_hospital_total',
        'n_icu_covid',
        'n_icu_non_tube',
        'n_icu_tube',
        'n_icu_non_covid',
        'n_icu_total',
        'n_deceased',
        'ncumul_deceased'
    ]

    print('Date and time:', last_row[COLUMNS.index('date')])
    print('Confirmed cases:', last_row[COLUMNS.index('ncumul_cases')] or 'None')
    print('Deaths:', last_row[COLUMNS.index('ncumul_deceased')] or 'None')
    print('Hospitalized:', last_row[COLUMNS.index('n_hospital_total')] or 'None')
    print('ICU:', last_row[COLUMNS.index('n_icu_total')] or 'None')
    # Intubated.
    print('Vent:', last_row[COLUMNS.index('n_hospital_icu_tube')] or 'None')
