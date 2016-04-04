test:
	py.test tests \
		--strict \
		--cov=harlequin \
		--cov-report=term-missing
