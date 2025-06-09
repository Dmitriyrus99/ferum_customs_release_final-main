APP=ferum_customs
SITE?=dev.localhost
BENCH?=frappe-bench

.PHONY: setup start update fixtures test

setup:
	bench get-app $(APP) --source-path . || true
	bench --site $(SITE) install-app $(APP)
	bench --site $(SITE) migrate

start:
	bench start

update:
	bench --site $(SITE) migrate
	bench build
	bench restart

fixtures:
	bench --site $(SITE) export-fixtures

test:
        bench --site $(SITE) run-tests --app $(APP) \
        --junit-xml=reports/make-results.xml
