
# 📊 Numbers API

Bring meaning to your metrics and stories to your dates with the Numbers API—an interface for fetching interesting facts about numbers, dates, years, and math.

---

## 🔗 URL Structure

```
http://numbersapi.com/<number>/<type>
```

- **number**:  
  - An integer (e.g., `42`)  
  - `"random"` for a random fact  
  - A date in `month/day` format (e.g., `2/29`) for `type=date`  
  - A range or comma-separated list (e.g., `1..3,10` for batch requests)

- **type** (optional):  
  - `trivia` (default)  
  - `math`  
  - `date`  
  - `year`

---

## 📌 Examples

```http
http://numbersapi.com/42
⇒ 42 is the result given by Google and Bing for the query "the answer to life the universe and everything".

http://numbersapi.com/2/29/date
⇒ February 29 is the day in 1504 that Columbus used a lunar eclipse to gain supplies from Native Americans.

http://numbersapi.com/random/year
⇒ 2013 is the year China attempted its first unmanned Moon landing.
```

---

## ⚙️ Usage Options

### ➕ `fragment`
Returns a sentence fragment instead of a full sentence.

```http
http://numbersapi.com/23/trivia?fragment
⇒ the number of times Julius Caesar was stabbed
```

---

### ➕ `notfound`
Controls behavior when no fact is found:
- `default` (returns fallback message)
- `floor` (rounds down to nearest fact)
- `ceil` (rounds up to nearest fact)

```http
http://numbersapi.com/314159265358979
⇒ 314159265358979 is a boring number.

http://numbersapi.com/35353?notfound=floor
⇒ 35000 is the number of genes in a human being.
```

---

### ➕ `default`
Supply a custom fallback message.

```http
http://numbersapi.com/1234567890987654321/year?default=Boring+number+is+boring.
⇒ Boring number is boring.
```

---

### ➕ `callback` (JSONP)
Wraps the response in a function for use with JSONP.

```http
http://numbersapi.com/42/math?callback=showNumber
⇒ showNumber("42 is the 5th Catalan number.");
```

---

### ➕ `write`
Wraps response in `document.write()` for direct HTML embedding.

```html
<script src="http://numbersapi.com/2012/year?write&fragment"></script>
```

---

### ➕ `min` & `max`
Restrict range for `random` queries.

```http
http://numbersapi.com/random?min=10&max=20
⇒ 13 is the number of provinces and territories in Canada.
```

---

### ➕ `json`
Returns metadata with the fact.

```http
http://numbersapi.com/random/year?json

⇒ {
  "text": "2012 is the year that the century's second and last solar transit of Venus occurs on June 6.",
  "found": true,
  "number": 2012,
  "type": "year",
  "date": "June 6"
}
```

---

## 🧮 Batch Requests

Fetch facts for multiple numbers:

```http
http://numbersapi.com/1..3,10

⇒ {
  "1": "1 is the number of dimensions of a line.",
  "2": "2 is the number of polynucleotide strands in a DNA double helix.",
  "3": "3 is the number of sets needed to win a volleyball match.",
  "10": "10 is the highest score in Olympic gymnastics competitions."
}
```

Use `json` to control the format of each returned fact.

---

## 💻 Code Samples

### jQuery Example

```javascript
$.get('http://numbersapi.com/1337/trivia?notfound=floor&fragment', function(data) {
  $('#number').text(data);
});
```

---

### JSONP Example

```html
<span id="number-fact"></span>

<script>
  function showNumber(str) {
    document.getElementById('number-fact').innerText = str;
  }

  (function() {
    var scriptTag = document.createElement('script');
    scriptTag.async = true;
    scriptTag.src = "http://numbersapi.com/42/math?callback=showNumber";
    document.body.appendChild(scriptTag);
  })();
</script>
```

---

## 📝 Notes

- Responses are plain text by default.
- Supports CORS for cross-origin requests.
- Batch responses limited to 100 entries.


