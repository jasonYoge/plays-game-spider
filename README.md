# 文件下载爬虫

## 基础环境搭建

### 安装 uv

> https://docs.astral.sh/uv/getting-started/installation/

### 通过uv 安装 python

``` python
$ uv python install
```

## 运行项目

### 安装开发依赖

```bash
# 安装项目依赖和开发工具
make install
```

### 运行项目

``` python
# dir为可选参数
$ make start url="你的目标URL" [dir="下载目录"]
```


## 代码质量工具

本项目配置了以下代码质量工具：

- **Black**: 代码格式化工具
- **isort**: 导入语句排序工具
- **flake8**: 代码风格检查工具
- **mypy**: 类型检查工具
- **pre-commit**: Git提交前自动检查

### 使用Makefile命令

```bash
# 查看所有可用命令
make help

# 格式化代码
make format

# 运行代码风格检查
make lint

# 运行类型检查
make type-check

# 运行所有检查
make check

# 清理缓存文件
make clean
```

### 手动运行工具

```bash
# 格式化代码
uv run black .
uv run isort .

# 代码风格检查
uv run flake8 .

# 类型检查
uv run mypy .

# 运行pre-commit检查
uv run pre-commit run --all-files
```
