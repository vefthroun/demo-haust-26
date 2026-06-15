### 1. HTML form 
1. [Html Forms leiðbeiningar](https://developer.mozilla.org/en-US/docs/Learn/Forms)  
1. [HTML Forms (gagnvirkt)](https://www.w3schools.com/html/html_forms.asp) 
1. [Pico CSS: Form](https://picocss.com/docs/forms)

---

### 2. FLASK: Form 
1. [Flask: The Request Object](https://flask.palletsprojects.com/en/3.0.x/quickstart/#the-request-object)
1. [Einfalt kóðasýnidæmi (login, signup, form): Html Form & Request Object](https://github.com/vefthroun/Vefforritun1/tree/main/Verkefni3/FORM)


---

### 3. Flask-WTF og WTForms 
The [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/) extension provides your Flask application integration with WTForms. It uses Python classes to represent web forms (wrapper). `(venv) $ pip install flask-wtf`.

[WTForms](https://wtforms.readthedocs.io/en/3.0.x/) is a flexible forms validation and rendering library for Python web development. It can work with whatever web framework and template engine you choose. It supports data validation, CSRF protection etc.

1. [Flask-WTF](https://www.tutorialspoint.com/flask/flask_wtf.htm) _vefgrein_
1. Tutorial: User Login Form, [The Flask Mega-Tutorial:  Web Forms](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms) _(tutorial) redirect, flash, klasanotkun_
1. Login sýnidæmi _(youtube)_
   1. [WTForms in Flask (login)](https://www.youtube.com/watch?v=vzaXBm-ZVOQ) 
   1. [Using Validators in Flask-WTF](https://youtu.be/jR2aFKuaOBs) og _[kóðinn](https://github.com/PrettyPrinted/youtube_video_code/tree/master/2017/04/24/Using%20Validators%20in%20Flask-WTF%20(Part%202%20of%205)/wtf_validators)_
   1. ítarefni: [Creating a Macro to Reduce Code Duplication](https://youtu.be/J9O0v-iM0TE) og _[kóðinn](https://github.com/PrettyPrinted/youtube_video_code/tree/master/2017/04/28/Flask-WTF%20-%20Creating%20a%20Macro%20to%20Reduce%20Code%20Duplication%20(4%20of%205))_
1. [Forms and User Input (48 mín)](https://www.youtube.com/watch?v=UIJKdCIEXUQ) _(youtube)_ og [kóðaskrár](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog/03-Forms-and-Validation) _Leiðrétting: Nota þarf email-validator safn fyrir email validator_

#### Athugasemdir

- When the `action` is set to an empty string the form is submitted to the URL that is currently in the address bar, which is the URL that rendered the form on the page. 
- From WTForms 2.3.0 version, the email validation is handled by an external library called email-validator `pip install email-validator`

<!--
1. Signup sýnidæmi: [WTForms validation and rendering in Flask (27 mín)](https://www.youtube.com/watch?v=j5IQI4aW9ZU) _(youtube)_ 
1. [How to validate and use WTForms í Flask](https://www.digitalocean.com/community/tutorials/how-to-use-and-validate-web-forms-with-flask-wtf)
1. [Handling Forms in Flask with Flask-WTF](https://hackersandslackers.com/flask-wtforms-forms/) _(gömul og gölluð vefgrein)_
1. [FLASK CRUD From scratch, wtform + editor (gamall)](https://www.youtube.com/watch?v=zRwy8gtgJ1A&t=54s&ab_channel=TraversyMedia) _youtube_ og [kóði](https://github.com/bradtraversy/myflaskapp) 
-->


---

## CRUD

Til að búa til CRUD (Create, Read, Update, Delete) virkni í Flask er algengt að nota **Python orðasöfn (dictionaries)** sem einfaldan gagnagrunn í minni. CRUD stendur fyrir hinar fjórar grunnaraðgerðir gagnavinnslu: að búa til, lesa, uppfæra og eyða gögnum.

Hér er dæmi um hvernig má útfæra þetta í Flask:

### 1. Uppsetning og gagnaskipan
Fyrst þarf að flytja inn nauðsynleg söfn og skilgreina orðasafn til að geyma gögnin.

```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Einfaldur "gagnagrunnur" í minni
nemendur = {
    "1": {"nafn": "Jón Jónsson", "netfang": "jon@skoli.is"},
    "2": {"nafn": "Anna Önnu", "netfang": "anna@skoli.is"}
}
```

### 2. Read (Lesa)
Notað til að birta lista yfir alla nemendur eða upplýsingar um einn ákveðinn.

```python
@app.route('/')
def index():
    # Birtir alla nemendur úr orðasafninu
    return render_template('index.html', nemendur=nemendur)

@app.route('/nemandi/<id>')
def view_student(id):
    # Sækir ákveðinn nemanda með lykli (key)
    nemandi = nemendur.get(id)
    return render_template('profile.html', nemandi=nemandi)
```

### 3. Create (Búa til)
Hér er notað **POST** aðferðin til að taka á móti gögnum úr HTML-formi. Nýr hlutur er bætt við orðasafnið með því að skilgreina nýjan lykil.

```python
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Sækir gögn úr formi
        nytt_id = str(len(nemendur) + 1)
        nafn = request.form.get('nafn')
        netfang = request.form.get('netfang')
        
        # Bætir við í orðasafnið
        nemendur[nytt_id] = {"nafn": nafn, "netfang": netfang}
        return redirect(url_for('index'))
    return render_template('create_form.html')
```

### 4. Update (Uppfæra)
Til að uppfæra gögn er gildið á tilteknum lykli í orðasafninu endurskilgreint.

```python
@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        # Uppfærir gildi nemanda
        nemendur[id]['nafn'] = request.form.get('nafn')
        nemendur[id]['netfang'] = request.form.get('netfang')
        return redirect(url_for('index'))
    
    nemandi = nemendur.get(id)
    return render_template('update_form.html', nemandi=nemandi, id=id)
```

### 5. Delete (Eyða)
Nota má `pop()` aðferðina eða `del` skipunina til að fjarlægja færslu úr orðasafninu.

```python
@app.route('/delete/<id>')
def delete(id):
    # Fjarlægir nemanda með gefnu ID
    if id in nemendur:
        nemendur.pop(id)
    return redirect(url_for('index'))
```

### Lykilatriði í útfærslunni:
*   **Routing:** Notað er `@app.route` til að tengja föll við ákveðnar vefslóðir.
*   **Request Object:** Gögnum úr formum er náð í gegnum `request.form`.
*   **Dictionaries:** Orðasöfn eru notuð því þau eru **breytanleg (mutable)**, sem gerir okkur kleift að bæta við, breyta og eyða gögnum á auðveldan hátt.
*   **HTTP Methods:** Mikilvægt er að skilgreina `methods=['POST']` fyrir leiðir sem breyta gögnum.

### 4. CKEditor (WYSIWYG HTML editor)

WYSIWYG HTML editor has the ability to convert HTML text area fields or other HTML elements to editor instances. WYSIWYG is an acronym for "what you see is what you get."

1. [Flask CKEditor](https://flask-ckeditor.readthedocs.io/en/latest/)
1. [How To Add A Rich Text Editor and Basic usage](https://www.youtube.com/watch?v=5jnAnnxZGQQ&ab_channel=Codemy.com) _myndband_

<!--
1. [CKEditor](https://ckeditor.com/)
   - [Online Demo](https://ckeditor.com/ckeditor-5/demo/), [kóðasýnidæmi](https://ckeditor.com/docs/ckeditor5/latest/installation/getting-started/quick-start.html) og [Docs](https://ckeditor.com/docs/)
-->
