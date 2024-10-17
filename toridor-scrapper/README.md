# TORIDORI 自動スクリプト

## スクレーピング
キャンペーン（https://marketing.toridori.me/）から 応募者情報を csv で取得
- analyze/scraper.ipynb を実行
- post_result_0x/の中身をコピーし、末尾に貼り付け
  https://docs.google.com/spreadsheets/d/1CN3J6EH66SXJO3Ic9wRvljYBjKOWa1v3XjlxhF2dD-8/edit?gid=14299579#gid=14299579
- 事後分析共に調整


## トリドリからオープンロジ発送情報
open logi に出力するための csv
- delivery/convert_to_delivery.ipynb を実行
- open logi に結果を入れる

## スクレーピングした csv を束ねる処理
open logi に出力するための csv
```py
from glob import glob
import os
import pandas as pd

FROM_PATH="result_01/"
TO_PATH="post_result_01/"

df=pd.concat([pd.read_csv(x) for x in sorted(glob(os.path.join(FROM_PATH,"*.csv")))], ignore_index=True)
df.to_csv(os.path.join(TO_PATH,"post_result_01.csv"), index=False)
```

