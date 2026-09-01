# 权衡司南 build pipeline.
# One command publishes everything locally into _site/. Each step is a small
# program that reads files and writes files; this Makefile only connects them.
#
# make build   full build: PDF, HTML, feed, index, assembled into _site/
# make html    per-entry HTML only (pandoc)
# make pdf      per-entry PDF only (LaTeX)
# make serve    build, then serve _site/ at http://localhost:8000
# make clean    remove _site/ and LaTeX aux files
#
# LATEX defaults to xelatex because entries are Mandarin and pdfLaTeX cannot
# set CJK body text. Override on the command line if needed: make build LATEX=lualatex

PY        := python3
LATEX     ?= xelatex
LATEXFLAGS ?= -interaction=nonstopmode -halt-on-error -shell-escape
SITE      := _site
TEMPLATES := templates

# Published entry directories, e.g. "entries/001-rope-derived".
PUBLISHED := $(shell $(PY) scripts/list_published.py)

.PHONY: build pdf html site rss index serve clean

build: pdf html site rss index
	@echo "build complete -> $(SITE)/"

# PDF is best-effort. A failed compile (e.g. a GIF-only entry that xelatex
# cannot embed) prints a warning and continues, so it never blocks the HTML
# build or the deploy. HTML is the published artifact; the PDF is a bonus.
pdf:
	@if ! command -v $(LATEX) >/dev/null 2>&1; then \
		echo "$(LATEX) not found; skipping PDF step"; \
	else \
		for dir in $(PUBLISHED); do \
			echo "$(LATEX) $$dir"; \
			if ! ( cd $$dir && $(LATEX) $(LATEXFLAGS) main.tex >/dev/null ); then \
				echo "  warning: PDF failed for $$dir; HTML still built, deploy continues"; \
			fi; \
		done; \
	fi

html:
	@command -v pandoc >/dev/null 2>&1 || { echo "pandoc not found; cannot build HTML"; exit 1; }
	@for dir in $(PUBLISHED); do \
		echo "pandoc $$dir"; \
		( cd $$dir && pandoc main.tex \
			--from latex --to html5 --standalone \
			--shift-heading-level-by=1 \
			--template ../../$(TEMPLATES)/page.html \
			--css ../../$(TEMPLATES)/style.css \
			--mathjax \
			-o index.html ); \
	done

site:
	@mkdir -p $(SITE)/entries $(SITE)/$(TEMPLATES)
	@cp $(TEMPLATES)/style.css $(SITE)/$(TEMPLATES)/style.css
	@for dir in $(PUBLISHED); do \
		name=$$(basename $$dir); \
		mkdir -p $(SITE)/entries/$$name; \
		cp $$dir/index.html $(SITE)/entries/$$name/ 2>/dev/null || true; \
		[ -f $$dir/main.pdf ] && cp $$dir/main.pdf $(SITE)/entries/$$name/ || true; \
		[ -d $$dir/figures ] && cp -r $$dir/figures $(SITE)/entries/$$name/ || true; \
	done

rss:
	@$(PY) scripts/build_rss.py

index:
	@$(PY) scripts/build_index.py

serve: build
	@echo "serving $(SITE)/ at http://localhost:8000 (Ctrl-C to stop)"
	@cd $(SITE) && $(PY) -m http.server 8000

clean:
	rm -rf $(SITE)
	@find entries -type f \( -name '*.aux' -o -name '*.log' -o -name '*.out' \
		-o -name '*.toc' -o -name '*.fls' -o -name '*.fdb_latexmk' \
		-o -name '*.synctex.gz' \) -delete 2>/dev/null || true
