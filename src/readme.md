# Testing Guide

电脑在抽烟！帮帮我们！

---
## What's different in .test/workflow
- 1. Fix the bug in workflow: "Country cannot be found." by using str.strip() to delete space.

- 2. Find an error in .normalization/country.py: "lower has no ().", which is a call to the function, not the value returned by the function, can not be {nan/none}.

- 3. All the normalization steps can have outputs(error/warning), but the program runs so slow when loading embeddings.
---

## 前置条件

在开始之前，请确保已配置好requirements.txt中有或没有的所有工具

```powershell
pip install -r requirements.txt

# 剩下的报错再装
```
---

## 其他准备

首先，克隆仓库并switch到.test/workflow分支：

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