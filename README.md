# demo-haust-26
verkefnadæmi fyrir nemendur

Verkefni 1.

```python
from flask import Flask, render_template

app = Flask(__name__)
```

Þessi kóði er grunnurinn að því að setja upp vefforrit í Flask. Hér er stutt útskýring á því hvað hver lína gerir:

*   **`from flask import Flask, render_template`**: Hér er verið að flytja inn (e. import) nauðsynlega íhluti úr Flask safninu. 
    *   **`Flask`** er klasinn sem er notaður til að búa til sjálft vefforritið.
    *   **`render_template`** er fall sem er notað til að sýna (e. render) HTML-skrár fyrir notandann í vafranum.
*   **`app = Flask(__name__)`**: Þessi lína býr til nýtt tilvik (e. instance) af Flask klasanum. 
    *   Breytan **`__name__`** er notuð svo Flask viti hvar það á að leita að auðlindum, eins og HTML-sniðmátum í `templates` möppunni og kyrrstæðum skrám (e. static files) eins og CSS í `static` möppunni.

Þetta er fyrsta skrefið í að búa til lágmarksvefforrit þar sem breytan `app` verður miðpunktur forritsins þíns.

---

```python
if __name__ == '__main__':
  app.run(debug=True, use_reloader=True) 
```

Þessi kóðabútur er notaður til að ræsa Flask-vefþjóninn beint úr Python-skránni þinni. Hér er stutt útskýring á því hvað hver hluti gerir:

*   **`if __name__ == '__main__':`**: Þetta er hefðbundin Python-leið til að tryggja að kóðinn keyri aðeins ef skráin er ræst beint (t.d. með skipuninni `python skráarnafn.py`). Ef skráin væri flutt inn (e. import) í aðra skrá sem eining, myndi vefþjóninn ekki ræsast sjálfkrafa.
*   **`app.run(...)`**: Þetta ræsir innbyggðan þróunarvefþjón Flask, sem er hannaður til að prófa forritið á meðan á smíði stendur.
*   **`debug=True`**: Þetta virkjar **villuleitarham** (e. debug mode). Það hefur tvo mikilvæga kosti í för með sér:
    1.  Vefþjónninn fylgist með breytingum á kóðanum þínum og **endurræsir sig sjálfkrafa** þegar þú vistar skrána.
    2.  Ef villa kemur upp í kóðanum birtist gagnvirkur villuleitari beint í vafranum sem hjálpar þér að greina vandamálið.
*   **`use_reloader=True`**: Þessi skipun stýrir því sérstaklega að vefþjóninn endurræsi sig þegar kóða er breytt. Þótt `debug=True` virki þetta yfirleitt sjálfkrafa, þá er þetta tiltekið hér til að tryggja að sú virkni sé virk.

**Mikilvæg athugasemd:** Samkvæmt heimildum ætti aldrei að nota villuleitarhaminn (`debug=True`) í raunverulegu vinnsluumhverfi (e. production) þar sem hann getur skapað öryggishættu með því að leyfa keyrslu á kóða beint úr vafra.


