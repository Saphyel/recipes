from pytest import mark


@mark.filterwarnings("ignore:.*Row.keys().*SQLAlchemy.*:DeprecationWarning")
class TestIngredientsEndpoints:
    @mark.parametrize(
        ["payload", "expect"],
        [({"name": "Huevos"}, {"name": "Huevos"})],
    )
    def test_create(self, payload: dict, expect: dict, client) -> None:
        response = client.post("/api/ingredients", json=expect)
        assert response.status_code == 201
        assert response.json() == expect

    def test_list(self, client) -> None:
        response = client.get("/api/ingredients")
        assert response.status_code == 200
        assert len(response.json()) > 0

    @mark.parametrize(
        ["name", "expect"],
        [("Huevos", {"name": "Huevos"})],
    )
    def test_find(self, name: str, expect: dict, client) -> None:
        response = client.get(f"/api/ingredients/{name}")
        assert response.status_code == 200
        assert response.json() == expect

    @mark.parametrize("name", ["Huevos"])
    def test_remove(self, name: str, client) -> None:
        response = client.delete(f"/api/ingredients/{name}")
        assert response.status_code == 204
        assert response.json() == ""
