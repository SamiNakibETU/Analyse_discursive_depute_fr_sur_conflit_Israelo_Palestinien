# Analyse discursive AN - Makefile
# Usage: make <target>

.PHONY: data install clean notebooks analyses analyses_extended figures ml help

help:
	@echo "Targets:"
	@echo "  make install   - Install dependencies"
	@echo "  make data     - Generate corpus (requires projet_gaza sources)"
	@echo "  make analyses_extended - Generate extended CSVs (trajectoires, movers, target, etc.)"
	@echo "  make analyses - Run supplemental analyses (fig21-fig25)"
	@echo "  make figures  - Generate all figures (analyses + extended; run notebooks for fig04, fig11, fig12, fig17)"
	@echo "  make ml       - ML pipeline: embeddings + validation (CPU)"
	@echo "  make ml-finetune - Fine-tune CamemBERT (GPU recommended)"
	@echo "  make notebooks - Run all notebooks"
	@echo "  make clean    - Remove caches and generated files"

install:
	pip install -r requirements.txt

data:
	python src/prepare_data.py

notebooks:
	jupyter nbconvert --to notebook --execute notebooks/01_corpus_validation.ipynb
	jupyter nbconvert --to notebook --execute notebooks/02_framing_lexique_emotions.ipynb
	jupyter nbconvert --to notebook --execute notebooks/03_evenements_convergence.ipynb
	jupyter nbconvert --to notebook --execute notebooks/04_ml_validation.ipynb

analyses:
	python src/analyses_supplementaires.py

figures: analyses
	@echo "Figures fig21-25 generees. Pour fig04, fig11, fig12, fig17 : make notebooks"

analyses_extended:
	python src/build_analyses_extended.py

ml:
	python src/ml_pipeline.py --mode embeddings
	python src/ml_pipeline.py --mode validate

ml-finetune:
	python src/ml_pipeline.py --mode finetune --epochs 3

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
