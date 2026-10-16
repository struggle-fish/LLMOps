"""
@Time   : 2026/8/8 15:16
@Author : jzy
@File   : test_app_handler.py
"""
import pytest
from unittest.mock import patch

from langchain_core.language_models.fake_chat_models import FakeListChatModel

from pkg.response import HttpCode


class TestAppHandler:
    """app控制器测试类"""

    @pytest.mark.parametrize(
        "app_id, query",
        [
            ("550e8400-e29b-41d4-a716-446655440000", None),
            ("550e8400-e29b-41d4-a716-446655440000", "你好，你是？")
        ])
    def test_completion(self, app_id, query, client, monkeypatch, tmp_path):
        """验证参数校验及聊天响应，隔离外部模型和真实会话文件。"""
        # 测试不上传追踪数据，也不读写开发环境的聊天记录。
        monkeypatch.setenv("LANGSMITH_TRACING", "false")
        monkeypatch.setenv("LANGCHAIN_TRACING_V2", "false")
        monkeypatch.setattr("internal.handler.app_handler.file_path", str(tmp_path / "history.json"))
        # 只替换外部模型，保留提示词、记忆和响应解析的实际执行流程。
        with patch("internal.handler.app_handler.ChatOpenAI",
                   return_value=FakeListChatModel(responses=["你好，我是测试助手。"])) as model:
            resp = client.post(f"/apps/{app_id}/debug", json={"query": query})
        assert resp.status_code == 200
        if query is None:
            assert resp.json["code"] == HttpCode.VALIDATION_ERROR
            model.assert_not_called()
        else:
            assert resp.json["code"] == HttpCode.SUCCESS
            assert resp.json["data"]["content"] == "你好，我是测试助手。"
            model.assert_called_once()
        print("相应内容", resp.json)
