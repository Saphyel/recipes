from pytest import mark


@mark.filterwarnings("ignore:.*Row.keys().*SQLAlchemy.*:DeprecationWarning")
class TestChefsEndpoints:
    @mark.parametrize(
        ["payload", "expect"],
        [
            ({"name": "Ramon"}, {"name": "Ramon", "instagram": None, "reddit": None, "twitter": None}),
            (
                {"name": "Pablo", "reddit": "Loco"},
                {"name": "Pablo", "instagram": None, "reddit": "Loco", "twitter": None},
            ),
        ],
    )
    def test_create(self, payload: dict, expect: dict, client) -> None:
        response = client.post("/api/chefs", json=expect)
        assert response.status_code == 201
        assert response.json() == expect

    def test_list(self, client) -> None:
        response = client.get("/api/chefs")
        assert response.status_code == 200
        assert len(response.json()) > 1

    @mark.parametrize(
        ["name", "expect"],
        [("Ramon", {"name": "Ramon", "instagram": None, "reddit": None, "twitter": None})],
    )
    def test_find(self, name: str, expect: dict, client) -> None:
        response = client.get(f"/api/chefs/{name}")
        assert response.status_code == 200
        assert response.json() == expect

    @mark.parametrize("name", ["Ramon", "Pablo"])
    def test_remove(self, name: str, client) -> None:
        response = client.delete(f"/api/chefs/{name}")
        assert response.status_code == 204
        assert response.json() == ""
