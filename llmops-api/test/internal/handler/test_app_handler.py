"""
@Time   : 2026/8/8 15:16
@Author : jzy
@File   : test_app_handler.py
"""
import pytest

from pkg.response import HttpCode


class TestAppHandler:
    """app控制器测试类"""

    @pytest.mark.parametrize(
        "app_id, query",
        [
            ("550e8400-e29b-41d4-a716-446655440000", None),
            ("550e8400-e29b-41d4-a716-446655440000", "你好，你是？")
        ])
    def test_completion(self, app_id, query, client):
        resp = client.post(f"/apps/{app_id}/debug", json={"query": query})
        assert resp.status_code == 200
        if query is None:
            assert resp.json["code"] == HttpCode.VALIDATION_ERROR
        else:
            assert resp.json["code"] == HttpCode.SUCCESS
        print("相应内容", resp.json)
