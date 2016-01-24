# -*- coding: utf-8 -*-
import pickle
from BeautifulSoup import BeautifulSoup
import codecs

with open("raw.pkl", "rb") as f:
    result = pickle.load(f)

with codecs.open("data.txt", "w", "utf-8") as o:
    with codecs.open("data_det.txt", "w","utf-8") as od:
        for url, html in result.iteritems():
            soup = BeautifulSoup(html)
            key = list(url.replace('http://www.kunigunde.ch/', '').replace('.htm',''))

            if key[0] != 'H':
                for line in soup.findAll('tr'):
                    tmp = [key[0]]
                    for entry in line.findAll('td'):
                        text = entry.text
                        text = text.replace('Variante von', '')
                        tmp.append(text)
                    if len(tmp) == 3 and sum([len(x) for x in tmp]) < 60:
                        print >>o, '\t'.join(tmp)
            else:
                for table in soup.findAll('table', attrs={"class":"text", "width": "100%"}):
                    rows = table.findAll('tr')

                    if rows[0].find('td', attrs={'colspan': "2"}):
                        name = rows[0].find('td', attrs={'colspan': "2"}).text
                        gender = "-"
                        origin = "-"
                        words = "-"
                        language = "-"
                        meaning = "-"
                        for x in rows[1:]:
                            col1 = x.findAll('td')[0].text
                            col2 = x.findAll('td')[1].text

                            if "Herkunftssprache" in col1:
                                language = col2
                            elif "Herkunft" in col1:
                                origin = col2
                            elif "rter:" in col1:
                                words = col2
                            elif "Geschlecht" in col1:
                                gender = col2
                            elif "Bedeutung" in col1:
                                meaning = col2
                        print >>od, '\t'.join((name, origin, gender, meaning, words, language))
