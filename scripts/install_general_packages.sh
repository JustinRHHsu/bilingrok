#!/bin/bash
# install_general_packages.sh
# ./scripts/install_general_packages.sh

# 安裝所有在 common_packages.txt 中的 package
DEPENDENCY_LISTS='scripts/dependency_packages.txt'

# 檢查 common_packages.txt 是否存在
if [ ! -f $DEPENDENCY_LISTS ]; then
    echo "dependency_packages.txt 檔案不存在"
    exit 1
fi

# 初始化變數
installed_packages=()
failed_packages=()

# 讀取 common_packages.txt 並安裝每個 package
while IFS= read -r package; do
    if [[ ! -z "$package" && ! "$package" =~ ^# ]]; then
        echo "正在安裝 $package"
        if pip install "$package"; then
            installed_packages+=("$package")
        else
            failed_packages+=("$package")
        fi
    fi
done < $DEPENDENCY_LISTS

echo "所有 package 安裝完成"

# 列出安裝成功的 package
if [ ${#installed_packages[@]} -ne 0 ]; then
    echo "===== 安裝成功的 package ====="
    for pkg in "${installed_packages[@]}"; do
        echo "$pkg"
    done
    echo "=============================="
else
    echo "=== 沒有成功安裝的 package ==="

fi

# 列出安裝失敗的 package
if [ ${#failed_packages[@]} -ne 0 ]; then
    echo "===== 安裝失敗的 package ====="
    for pkg in "${failed_packages[@]}"; do
        echo "$pkg"
    echo "=============================="
    done
else
    echo "=== 沒有安裝失敗的 package ==="
fi