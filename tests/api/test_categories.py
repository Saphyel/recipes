from pytest import mark


# pytestmark = mark.filterwarnings("ignore:.*Row.keys().*SQLAlchemy.*:DeprecationWarning")


@mark.webtest
@mark.filterwarnings("ignore:.*Row.keys().*SQLAlchemy.*:DeprecationWarning")
class TestCategoriesEndpoints:
    @mark.parametrize(["payload", "expect"], [({"name": "Cena"}, {"name": "Cena"})])
    def test_create(self, payload: dict, expect: dict, client) -> None:
        response = client.post("/api/categories", json=expect)
        assert response.status_code == 201
        assert response.json() == expect

    def test_list(self, client) -> None:
        response = client.get("/api/categories")
        assert response.status_code == 200
        assert len(response.json()) > 0

    @mark.parametrize(["name", "expect"], [("Cena", {"name": "Cena"})])
    def test_find(self, name: str, expect: dict, client) -> None:
        response = client.get(f"/api/categories/{name}")
        assert response.status_code == 200
        assert response.json() == expect

    @mark.parametrize("name", ["Cena"])
    def test_remove(self, name: str, client) -> None:
        response = client.delete(f"/api/categories/{name}")
        assert response.status_code == 204
        assert response.json() == ""
