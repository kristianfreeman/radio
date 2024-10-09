PYTHON ?= python3

default:
	$(PYTHON) generate_liquidsoap_config.py
	liquidsoap ./radio_stations.liq
