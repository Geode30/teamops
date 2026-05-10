def api_request(
    *,
    client,
    method,
    url,
    payload=None,
    query_params=None,
    expected_status=200,
    format="json",
):
    request_method = getattr(client, method.lower())

    method = method.lower()

    if method == "get":
        response = request_method(url, data=query_params)
    else:
        response = request_method(url, data=payload, format=format)

    assert response.status_code == expected_status
    return response

def assert_api_create(*, client, api, payload, expected_status=201):
    return api_request(
        client=client,
        method="post",
        url=api,
        payload=payload,
        expected_status=expected_status,
    )

def assert_api_update(*, client, api, instance, payload, expected_status=200):
    return api_request(
        client=client,
        method="put",
        url=f"{api}{instance.id}/",
        payload=payload,
        expected_status=expected_status,
    )

def assert_api_list(*, client, api, instances=None, query_params=None, expected_status=200):
    response = api_request(
        client=client,
        method="get",
        url=api,
        expected_status=expected_status,
        query_params=query_params
    )

    assert isinstance(response.data, list)

    expected_ids = {u.id for u in instances}
    response_ids = {u["id"] for u in response.data}

    assert response_ids == expected_ids

    return response

def assert_api_retrieve(*, client, api, instance, expected_status=200):
    response = api_request(
        client=client,
        method="get",
        url=f"{api}{instance.id}/",
        expected_status=expected_status,
    )

    assert response.data["id"] == instance.id
    return response

def assert_api_delete(*, client, api, instance, expected_status=204):
    return api_request(
        client=client,
        method="delete",
        url=f"{api}{instance.id}/",
        expected_status=expected_status,
    )