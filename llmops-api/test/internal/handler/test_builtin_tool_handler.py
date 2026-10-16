from pkg.response import HttpCode


def test_get_builtin_tools(client):
    """验证实际工具列表及参数元数据，防止 Pydantic 升级导致接口再次返回 500。"""
    response = client.get("/builtin-tools")
    assert response.status_code == 200
    assert response.json["code"] == HttpCode.SUCCESS
    tools = {
        tool["name"]: tool
        for provider in response.json["data"]
        for tool in provider["tools"]
    }
    assert tools["current_time"]["inputs"] == []
    for name in ("google_serper", "duckduckgo_search", "wikipedia_search", "gptimage2", "gaode_weather"):
        inputs = tools[name]["inputs"]
        assert len(inputs) == 1
        assert inputs[0]["name"] == ("city" if name == "gaode_weather" else "query")
        assert inputs[0]["description"]
        assert inputs[0]["type"] == "str"
        assert inputs[0]["required"] is True
