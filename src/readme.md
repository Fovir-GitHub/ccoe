# Testing Guide

电脑在抽烟！帮帮我们！

---

## 前置条件

在开始之前，请确保已配置好requirements.txt中有或没有的所有工具

```powershell
pip install -r requirements.txt

# 剩下的报错再装
```
---

## 其他准备

首先，克隆仓库并cd到.test/workflow分支：

```bash
# 克隆仓库
git clone https://github.com/Fovir-GitHub/ccoe.git
git switch test/workflow

# 在.env里配置好HK_API_KEY
# 注：测试时采用Ollama本地Qwen3.5:4b模型，且只测试极小数据量,测试成功后再做删改
# 详情可见.src/workflow/workflow.py load_embeddings

```
```powershell
# 在ccoe目录下运行workflow
python -m src.workflow.workflow
```