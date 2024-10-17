import re
import yaml
from io import StringIO


def extract_split_md_frontmatter(
        text, 
) -> tuple[dict[str, any], str]:
    ptt = r"^---*[\r\n]*([\s\S]*?)---*[\r\n]([\s\S]*?)"
    # Front Matterの抽出
    re_text = None
    groups = re.match(ptt, text).groups()
    re_text = groups[0]
    re_content = groups[1]

    # YAMLパーサ
    yaml_meta = None
    with StringIO() as st:                    # メモリストリームを初期化
        st.write(re_text)                     # ストリームへ文字列を書き込み
        st.seek(0)                            # ストリームのカーソル位置を先頭に移動
        yaml_meta = yaml.safe_load(st)        # YAMLを解釈

    return yaml_meta, re_content
