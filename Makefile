.PHONY: help install install-dev format lint type-check check clean

help: ## 显示帮助信息
	@echo "可用的命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 安装项目依赖
	uv venv
	uv pip install -e ".[dev]"
	uv run pre-commit install

format: ## 格式化代码
	uv run black .
	uv run isort .

lint: ## 运行代码风格检查
	uv run flake8 .

type-check: ## 运行类型检查
	uv run mypy .

check: format lint type-check ## 运行所有检查

clean: ## 清理缓存文件
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

start: ## 运行项目
	rm -rf ./download/
	uv run python main.py --url=$(url) $(if $(dir),--dir=$(dir),)
