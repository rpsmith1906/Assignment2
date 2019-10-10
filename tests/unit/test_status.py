#!/usr/bin/perl
import requests

address = "http://127.0.0.1:5000"

def test_port():
	assert requests.get(address).status_code == 200

def test_pages():
	for page in ["/", "/register", "/login", "/spell_check", "/logout"]:
		assert requests.get(address + page).status_code == 200
