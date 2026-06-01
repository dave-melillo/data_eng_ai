# 🔴 PokeAPI

Practice calling REST APIs with **PokeAPI**—a free, no-authentication service
that returns detailed JSON data about every Pokémon. Because it takes a number
(the Pokédex id) and returns a consistent JSON structure, it is ideal for
learning how to build requests, parse responses, and handle errors.

---

## 🔗 URL Structure

```
https://pokeapi.co/api/v2/pokemon/<id or name>
```

- **id**: an integer Pokédex number (e.g. `42`)
- **name**: a Pokémon name (e.g. `pikachu`)

A missing id or name returns **HTTP 404**, so always check
`response.status_code` before parsing.

---

## 📌 Examples

```http
https://pokeapi.co/api/v2/pokemon/1
⇒ Bulbasaur (grass/poison)

https://pokeapi.co/api/v2/pokemon/42
⇒ Golbat (poison/flying)

https://pokeapi.co/api/v2/pokemon/pikachu
⇒ Pikachu (electric)
```

---

## 🧱 Useful Fields

| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Pokédex number |
| `name` | string | lowercase name |
| `height` / `weight` | int | decimetres / hectograms |
| `base_experience` | int | XP for defeating it |
| `types` | list | type name at `types[i]["type"]["name"]` |
| `abilities` | list | ability name at `abilities[i]["ability"]["name"]` |

---

## 📄 List & Paginate

```http
https://pokeapi.co/api/v2/pokemon?limit=20&offset=0
```

Use the optional `limit` and `offset` query parameters to page through results.

---

## 🧪 Quick Test (Python)

```python
import requests

resp = requests.get("https://pokeapi.co/api/v2/pokemon/42")
data = resp.json()
print(data["name"], "-", "/".join(t["type"]["name"] for t in data["types"]))
# golbat - poison/flying
```

No API key, no signup. Full docs: https://pokeapi.co/docs/v2
