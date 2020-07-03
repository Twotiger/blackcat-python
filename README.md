收集python报错


## 如何使用

```
from blackcat import BlackCat
m = BlackCat("http://127.0.0.1:9000/api/issue/issue?token=33a7dd5cd02e9e1c632542f3149f5add")
m.set_labels([{"username": "xyz"}]) # 添加自定标签

1/0 # 捕获这个错误
```