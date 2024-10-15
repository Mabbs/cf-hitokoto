# Cloudflare Random Hitokoto
使用Cloudflare规则实现的不限请求次数的随机一言接口    
数据来源：[sentences-bundle](https://github.com/hitokoto-osc/sentences-bundle)   
重写规则：   
```javascript
concat("/orig_data/", substring(uuidv4(cf.random_seed),0,4), ".json")
```
因为Cloudflare求随机数只能生成uuid，如果是3位就只能用4096条，4位是65536条，但一言里只有6975条😂，想来想去只好每条重复十遍这样就能读出6553条数据了，感觉实现的不太好😂。