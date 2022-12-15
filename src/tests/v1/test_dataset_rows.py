from src.tests.v1.mock_data import (
    dataset_rows_create_multi_class_payload,
    dataset_rows_create_binary_payload,
    dataset_rows_create_wrong_model_payload,
)
import pytest
from src import schemas
from src.tests.v1.conftest import get_order_number, state
from fastapi import status


@pytest.mark.order(get_order_number("dataset_rows_create"))
def test_dataset_row_create_many(client):
    response_model_multi = client.post(
        "/v1/dataset-rows",
        json=list(
            map(
                lambda x: {**x, "model_id": state.model_multi["id"]},
                dataset_rows_create_multi_class_payload,
            )
        ),
        headers={"api-key": state.api_key},
    )

    response_model_binary = client.post(
        "/v1/dataset-rows",
        json=list(
            map(
                lambda x: {**x, "model_id": state.model_binary["id"]},
                dataset_rows_create_binary_payload,
            )
        ),
        headers={"api-key": state.api_key},
    )

    response_wrong_model = client.post(
        "/v1/dataset-rows",
        json=(dataset_rows_create_wrong_model_payload),
        headers={"api-key": state.api_key},
    )

    assert response_model_multi.status_code == status.HTTP_201_CREATED
    assert response_model_binary.status_code == status.HTTP_201_CREATED
    assert response_wrong_model.status_code == status.HTTP_404_NOT_FOUND
    validated = [schemas.DatasetRow(**m) for m in response_model_multi.json()]
    validated = [schemas.DatasetRow(**m) for m in response_model_binary.json()]


@pytest.mark.order(get_order_number("dataset_rows_get_model's_all"))
def test_dataset_row_get_models_all(client):
    response_model_multi = client.get(
        f"/v1/dataset-rows?model_id={state.model_multi['id']}",
        headers={"api-key": state.api_key},
    )
    response_model_binary = client.get(
        f"/v1/dataset-rows?model_id={state.model_binary['id']}",
        headers={"api-key": state.api_key},
    )
    response_model_not_found = client.get(
        f"/v1/dataset-rows?model_id=wrong_model_id",
        headers={"api-key": state.api_key},
    )

    assert response_model_multi.status_code == status.HTTP_200_OK
    assert response_model_binary.status_code == status.HTTP_200_OK
    assert response_model_not_found.status_code == status.HTTP_404_NOT_FOUND
    validated = [schemas.DatasetRow(**m) for m in response_model_multi.json()]
    validated = [schemas.DatasetRow(**m) for m in response_model_binary.json()]
