# QOSMOS
Qosmos is an open project for learning through small simulations. It includes AI helpers for setup and analysis, plus examples and tests so results are easy to repeat.
# Qosmos

Plain-language, open-source simulations with a little AI help.
Qosmos makes it easy to run small physics-style experiments, see what
happens, and share repeatable results—complete with examples, docs,
and automatic tests.

## Features
- Simple simulations you can read and tweak
- AI helpers for setup notes and result summaries
- Clear docs and examples to learn by doing
- Built-in tests and CI so results are easy to repeat

## Quick start
    pip install -e ".[dev]"
    python scripts/extract_knowledge.py
    pytest -q

## Project layout
- `src/qosmos/` — library code  
- `docs/` — short guides and examples  
- `assets/` — zipped knowledge packs (tracked with Git LFS)  
- `knowledge/` — auto-extracted data for local use  
- `tests/` — quick checks to keep things honest  

## Notes
- Everything here is for learning and exploration.  
- No claims about real-world effects—these are simulations.
