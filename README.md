# Cloudflare Random Hitokoto
使用Cloudflare规则实现的不限请求次数的随机一言接口    
数据来源：[sentences-bundle](https://github.com/hitokoto-osc/sentences-bundle)   
全随机重写规则：   
```javascript
concat("/orig_data/", substring(uuidv4(cf.random_seed),0,4), ".json")
```
带分类重写规则：    
```javascript
concat("/categories/", substring(http.request.uri.query,2,3), "/", substring(uuidv4(cf.random_seed),0,3), ".json")
```

因为Cloudflare求随机数只能生成uuid，所以只能靠循环重复的方式避免找不到文件了😂。   
用法（拿规则想实现只能靠预载了）：

| 参数 | 值 | 可选 | 说明 |
| - | - | - | - |
| c | 见后表 | 是 | 句子类型 |