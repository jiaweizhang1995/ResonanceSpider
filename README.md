# 雷索纳斯商品倒卖增幅分析工具

这个 Python 脚本用于分析和识别最佳的商品倒卖机会。通过从 https://resonance.breadio.wiki/ 获取数据，该工具能够解析和计算不同城市之间商品价格的潜在增幅，帮助用户找到利润最大化的倒卖机会。

## 主要功能

- **数据抓取**：自动从网站获取最新的商品价格数据。
- **数据解析**：分析商品数据，包括本地和其他城市的价格增幅。
- **优化分析**：识别并列出具有最高价格增幅差异的商品倒卖机会。

## 如何使用

1. 确保你的环境中安装了 Python 3 和所需的第三方库：`requests` 和 `beautifulsoup4`。
2. 下载脚本到本地，并在项目目录下打开命令行或终端。
3. 运行脚本：`python <脚本名.py>`。

## 安装依赖

在项目目录下运行以下命令来安装必要的库：

```bash
pip install -r requirements.txt
```


## 后续更新任务:
- [ ] 增加最佳倒卖路线
- [ ] 最优倒卖方案增加价格显示
- [ ] 自动发送邮件/微信提醒
