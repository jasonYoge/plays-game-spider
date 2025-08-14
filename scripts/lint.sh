#!/bin/bash

# Python Lint 工具脚本
# 使用方法: ./scripts/lint.sh [format|lint|type-check|all]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
check_command() {
    if ! command -v "$1" &> /dev/null; then
        print_error "$1 未找到，请先安装"
        exit 1
    fi
}

# 格式化代码
format_code() {
    print_message "运行代码格式化..."
    make format
    print_success "代码格式化完成"
}

# 代码风格检查
lint_code() {
    print_message "运行代码风格检查..."
    make lint
    print_success "代码风格检查通过"
}

# 类型检查
type_check() {
    print_message "运行类型检查..."
    make type-check
    print_success "类型检查通过"
}

# 运行所有检查
run_all_checks() {
    print_message "运行所有代码质量检查..."
    make check
    print_success "所有检查通过"
}

# 主函数
main() {
    case "${1:-all}" in
        "format")
            format_code
            ;;
        "lint")
            lint_code
            ;;
        "type-check")
            type_check
            ;;
        "all")
            run_all_checks
            ;;
        *)
            print_error "未知参数: $1"
            echo "使用方法: $0 [format|lint|type-check|all]"
            exit 1
            ;;
    esac
}

# 检查是否在项目根目录
if [ ! -f "pyproject.toml" ]; then
    print_error "请在项目根目录运行此脚本"
    exit 1
fi

# 检查uv是否可用
check_command "uv"

main "$@"
