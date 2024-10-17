import re
from jsmin import jsmin
from cssmin import cssmin

def _open_close_pipe(func, file_path):
    with open(file_path, 'r', encoding='utf-8') as js_file:
        file = js_file.read()

    file = func(file)

    with open(file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(file)


def minify_js_func(s0: str):
    s1 = [s.split("//")[0] for s in s0]  # 1行コメント(//以降)を削除
    s2 = "\n".join([s.strip() for s in s1])  # 各行の前後の空白を削除
    s9 = re.sub('/\*.*?\*/', '', s2)  # コメント(/* */)の削除
    return s9


def minify_css_func(s0: str):
    s0 = s0.split('\n')
    s1 = "".join([s.strip() for s in s0])  # 各行の前後の空白を削除
    s2 = re.sub('/\*.*?\*/', '', s1)  # コメントの削除
    s3 = re.sub(': +?', ':', s2)  # セミコロン後の空白を削除
    s9 = re.sub(' +?{', '{', s3)  # '{'前の空白を削除
    return s9


def minify_js(js_file_path: str):
    pass
    # _open_close_pipe(minify_js_func, js_file_path)


def minify_css(css_file_path: str):
    _open_close_pipe(minify_css_func, css_file_path)
