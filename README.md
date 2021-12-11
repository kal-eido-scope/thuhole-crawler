## 首次Clone后

你需要按照依赖。

```bash
# After clone the repo and cd to the root...
pip install -r requirements.txt
```

## 如何参与爬取？

首先从[Issues](https://github.com/sunziping2016/thuhole-crawler/issues)挑一个你喜欢且无Assignee的区间。点开后，将Assignee设为自己。

然后运行：

```bash
git checkout -b <start>-<end>
python ./main.py --email example@mails.tsinghua.edu.cn --password some_password --start <start> --end <end>
```

或：

```bash
git checkout -b <start>-<end>
python ./main.py --token some_token --start <start> --end <end>
```

其中的`<start>`和`<end>`替换为你的区间。区间左闭右开。

爬取完毕后：

```bash
git add .
git commit -m 'crawled <start>-<end> #<issue-id>'
git push
```

这里的commit信息只是个推荐。只是方便管理。随后你可以关闭issue，标志了区间爬取的完成。

## 关于项目

爬虫是会自动忽略已经爬取的。如果你确认爬取的东西有误，可以删除文件夹`data/<post_id>`和文件`data/<post_id>.json`。

如果图片爬取失败可能会留下空的图片文件，这是符合预期的，可以避免重复爬取。

如果你的今日8000次用光了，程序会抛出`AssertionError: Unknown error`。
