.PHONY: reproduce robustness figures paper all
reproduce:   ## recompute every number and check pre-registration fingerprints (standard library only)
	python3 reproduce.py
robustness:  ## confidence intervals and alternative scoring rules
	python3 robustness.py
figures:     ## redraw every figure from data/ (needs matplotlib)
	python3 figures/make_figures.py
paper:       ## rebuild the PDF (needs a LaTeX installation)
	cd paper && pdflatex -interaction=nonstopmode main && bibtex main && pdflatex -interaction=nonstopmode main && pdflatex -interaction=nonstopmode main && cp main.pdf Sharma_JCrew_Blockers_2026.pdf
all: reproduce robustness figures
