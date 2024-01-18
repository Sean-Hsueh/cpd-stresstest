WORKDIR=/selenium-script
STAGING=

nb_convert_py: clean
	docker run --rm  -ti --workdir=$(WORKDIR) -v `pwd`:$(WORKDIR) python:3-alpine sh -c "sh $(WORKDIR)/script/convert.sh; sh $(WORKDIR)/script_staging/convert.sh"



configmap:
	oc create cm script --from-file=`pwd`/script$(STAGING) --dry-run=client -o yaml | oc apply -f -
	oc create cm area-trend-data --from-file=`pwd`/sample_data/area_trend_v2_utf8.csv --dry-run=client -o yaml | oc apply -f -

	# delete cm before create it
	oc delete cm airline-data || true
	# cm may have large annotation, use create to avoid long annotation, but we have to delete explictly before update
	oc create cm airline-data --from-file=`pwd`/sample_data/airline-data.csv

	oc delete cm go-sales || true
	oc create cm go-sales --from-file=`pwd`/sample_data/GoSales.csv

clean:
	@for f in $(shell ls script/*.ipynb); do \
		f_name=`basename $${f} .ipynb`; \
		rm -f script/$${f_name}.py; \
	done
	@for f in $(shell ls script_staging/*.ipynb); do \
		f_name=`basename $${f} .ipynb`; \
		rm -f script_staging/$${f_name}.py; \
	done
