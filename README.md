###项目名称
《豆瓣图书信息爬取》

###项目描述
使用Python编程语言编写一个网络爬虫项目，将豆瓣图书网站上的所有图书信息爬取下来，并存储到MySQL数据库中。
爬取信息字段要求：ID号、书名、作者、出版社、原作名、译者、出版年、页数、定价、装帧、丛书、ISBN、评分、评论人数
***

###爬取思路
1. 从[豆瓣图书标签](https://book.douban.com/tag/?view=type&icn=index-sorttags-all)获取所有的标签和对应的url
2. 逐个访问这些url，会获得这些标签对应下的图书列表页
3. 图书列表有很多页，观察url会发现每页的偏移量是20，因此可以构造出每页图书列表的url
3. 从图书列表页获取图书详细信息url
4. 访问图书详细信息url，提取字段

###优化问题
1. 多个请求头随机使用 已解决
2. 多个IP代理随机使用 已解决
3. 多线程  已解决
4. 分布式  