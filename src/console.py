import pytest
import uvicorn


def dev() -> None:
    uvicorn.run("src.main:app", port=8000, reload=True)


def test() -> None:
    pytest.main(["-v"])
