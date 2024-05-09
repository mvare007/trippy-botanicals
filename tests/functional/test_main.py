import pytest

def test_index_route(client, database):
	url = '/'
	response = client.get(url)

	assert response.status_code == 200


