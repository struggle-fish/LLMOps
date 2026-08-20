"""
@Time   : 2026/8/8 15:16
@Author : jzy
@File   : test_app_handler.py
"""
import pytest

from pkg.response import HttpCode


class TestAppHandler:
    """app控制器测试类"""

    @pytest.mark.parametrize("query", [None, "你好,帮我写一首诗"])
    def test_completion(self, query, client):
        resp = client.post("/app/completion", json={"query": query})
        assert resp.status_code == 200
        if query is None:
            assert resp.json["code"] == HttpCode.VALIDATION_ERROR
        else:
            assert resp.json["code"] == HttpCode.SUCCESS
        print("相应内容", resp.json)
