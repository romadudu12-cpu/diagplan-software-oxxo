import app as diagplan

def test_home_page(tmp_path, monkeypatch):
    monkeypatch.setattr(diagplan, "DB_PATH", tmp_path / "test.db")
    diagplan.init_db()
    client = diagplan.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Painel de estoque" in response.data

def test_create_product(tmp_path, monkeypatch):
    monkeypatch.setattr(diagplan, "DB_PATH", tmp_path / "test.db")
    diagplan.init_db()
    client = diagplan.app.test_client()
    response = client.post("/produtos/novo", data={
        "name": "Leite integral", "category": "Laticínios", "sku": "LEI001"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Leite integral" in response.get_data(as_text=True)
