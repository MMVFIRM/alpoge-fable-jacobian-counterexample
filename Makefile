.PHONY: install verify frozen-files-integrity frozen-archive-integrity repository-integrity integrity

install:
	python -m pip install -r requirements.txt

verify:
	python scripts/run_all_checks.py

frozen-files-integrity:
	sha256sum -c MANIFEST.sha256

frozen-archive-integrity:
	cd frozen && sha256sum -c referee_package-2026-07-20.sha256

repository-integrity:
	sha256sum -c REPOSITORY_MANIFEST.sha256

integrity: frozen-files-integrity frozen-archive-integrity repository-integrity
