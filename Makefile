POETRY := poetry

test:
	@$(POETRY) run pytest --tb=short

watch-tests:
	ls *.py | entr @$(POETRY) run pytest --tb=short