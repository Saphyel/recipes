from pytest import mark


@mark.filterwarnings("ignore:.*Row.keys().*SQLAlchemy.*:DeprecationWarning")
class TestRecipesEndpoints:
    @mark.parametrize(
        ["payload", "expect"],
        [
            (
                {"title": "Tortilla"},
                {
                    "title": "Tortilla",
                    "image": None,
                    "active_cook": None,
                    "total_cook": None,
                    "serves": None,
                    "description": None,
                    "instructions": None,
                    "url": None,
                    "category_name": None,
                    "chef_name": None,
                },
            )
        ],
    )
    def test_create(self, payload: dict, expect: dict, client) -> None:
        response = client.post("/api/recipes", json=expect)
        assert response.status_code == 201
        assert response.json() == expect

    def test_list(self, client) -> None:
        response = client.get("/api/recipes")
        assert response.status_code == 200
        assert len(response.json()) > 0

    @mark.parametrize(
        ["name", "expect"],
        [
            (
                "Tortilla",
                {
                    "title": "Tortilla",
                    "image": None,
                    "active_cook": None,
                    "total_cook": None,
                    "serves": None,
                    "description": None,
                    "instructions": None,
                    "url": None,
                    "category_name": None,
                    "chef_name": None,
                },
            )
        ],
    )
    def test_find(self, name: str, expect: dict, client) -> None:
        response = client.get(f"/api/recipes/{name}")
        assert response.status_code == 200
        assert response.json() == expect

    @mark.parametrize("name", ["Tortilla"])
    def test_remove(self, name: str, client) -> None:
        response = client.delete(f"/api/recipes/{name}")
        assert response.status_code == 204
        assert response.json() == ""
