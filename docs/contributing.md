# Contributing

Contributions are welcome. This fork maintains the Python API and documentation; changes should avoid altering runtime behavior unless required.

## Development setup
```bash
git clone https://github.com/neoralab/pdbfixer.git
cd pdbfixer
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\\Scripts\\activate
pip install -e ".[tests]"
```

## Running tests
```bash
pytest
```

Use `pytest -m "not slow"` to skip slow or network-heavy tests.

## Documentation
```bash
pip install -e ".[docs]"
mkdocs serve  # live preview
mkdocs build  # validate build
```

## Pull requests
- Keep changes narrowly scoped and avoid refactoring production code unless necessary for documentation accuracy.
- Update or add examples when API-facing changes are made.
- Ensure new files carry the MIT license header or are clearly covered by the repository LICENSE.
