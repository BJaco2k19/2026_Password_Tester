# Password Strength Tester, Inspired in and primarily written by Me, with some extra eyes-on from Copilot

[![CI](https://github.com/BJaco2k19/password-strength/actions/workflows/ci.yml/badge.svg)](https://github.com/BJaco2k19/password-strength/actions/workflows/ci.yml)

Repository layout:

- [cli.py](cli.py)
- [password_strength/core.py](password_strength/core.py)
- [web/app.py](web/app.py)
- [web/templates/index.html](web/templates/index.html)
- [tests/test_core.py](tests/test_core.py)
- [pyproject.toml](pyproject.toml)
- [.github/workflows/ci.yml](.github/workflows/ci.yml)
- [.gitignore](.gitignore)
- [LICENSE](LICENSE)

Minimal Python package that provides a simple password strength scoring function, a CLI, and suggestions.

Usage:

- Run CLI interactively:

```bash
python cli.py
```

- Pass password on CLI (note: not secure on shared terminals):

```bash
python cli.py -p "MyP@ssw0rd"
```

- Get JSON output:

```bash
python cli.py -p "MyP@ssw0rd" --json
```

The JSON output includes per-component ratings for `length` and `complexity`:

```json
{
	"score": 72,
	"classification": "Strong",
	"breakdown": {
		"length_score": 36.0,
		"charset_score": 22.5,
		"bonus": 12.0,
		"repeat_penalty": 0,
		"sequence_penalty": 0,
		"length": 16,
		"charsets": 3
	},
	"components": {
		"length": {"score": 80, "classification": "Strong"},
		"complexity": {"score": 64, "classification": "Medium"}
	},
	"suggestions": [
		"Include a mix of lowercase, uppercase, digits, and symbols."
	]
}
```


Library:

```py
from password_strength import score_password, classify_score, suggest_improvements
```

Run tests (requires `pytest`):

```bash
pip install -r requirements.txt
pytest -q
```

