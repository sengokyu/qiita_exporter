"""Qiitaの記事をGitHubのマークダウンのファイルに出力する

以下のことをおこなっています。
・画像をローカルにダウロードして、リンクを書き換えます。
・コードブロック以外の行にて、改行コードの前にスペース2ついれて改行を行います。
・「#タイトル」という記述があったら「# タイトル」に直します。
・コードブロックのタイトル（例：「```python:test.py」）が表示されないので対応します。

"""
import sys
import re
import urllib
import os
import yaml
import qiita_api


class Paths:
    def __init__(self, root_path):
        self.posts = os.path.join(root_path, '_posts')
        self.images = os.path.join(root_path, 'assets', 'images')

    def __makedirs(self, target):
        if not os.path.exists(target):
            os.makedirs(target)

    def makedirs(self):
        self.__makedirs(self.posts)
        self.__makedirs(self.images)


def fix_titlemiss(line):
    """タイトルタグのスペースの入れ忘れを修正します."""
    if not line:
        return line
    if line[0] != '#':
        return line
    if "# " in line:
        return line
    # #から開始しているが、スペースで区切られていない
    result = ''
    sts = 0
    for s in line:
        if sts == 0 and s != '#':
            # #の後にスペースを挿入
            sts = 1
            result += " "
        result += s
    return result


def has_code_block_mark(line):
    """指定の行がコードブロックのタグ（```）か検査します."""
    if len(line) < 3:
        return False
    if line[0:3] == '```':
        return True
    return False


def fix_newline(line):
    """改行コードの前にスペースを2つ追加します."""
    if line[-2:] == '  ':
        return line
    return line + '  '


def download(url, local_path):
    """ファイルをダウンロードします."""
    with urllib.request.urlopen(url) as web_file, open(local_path, 'wb') as download_file:
        download_file.write(web_file.read())


def fix_image(dst_folder, line):
    """Qiitaのサーバーの画像ファイルから自分のリポジトリのファイルを表示するように修正する."""
    images = re.findall(
        r'https://qiita-image-store.+?\.(?:png|gif|jpeg|jpg)', line)
    if not images:
        return line
    for url in images:
        name = url.split("/")[-1]
        download(url, os.path.join(dst_folder, name))
        ix = line.find(url)

        line = line.replace(url, '/assets/images/' + name)
    return line


def fix_mypage_link(line, dict_title):
    """自分の記事へのURLを修正する"""
    for url in dict_title.keys():
        line = line.replace(url, dict_title[url] + '.md')
    return line


def fix_markdown(paths, body, dict_title):
    """GitHubのマークダウンで表示できるように修正します."""
    result = ''
    lines = body.splitlines()
    code_block_flg = False
    for line in lines:
        if has_code_block_mark(line):
            code_block_flg = not code_block_flg
            if code_block_flg:
                # コードブロックのタイトルを修正
                ix = line.find(":")
                if ix != -1:
                    result += "**" + line[ix+1:] + "**  \n"
        line = fix_titlemiss(line)
        line = fix_image(paths.images, line)

        # コードブロックの外では以下の処理を行う
        # ・自分の記事へのリンクの修正
        # ・改行コードの後にスペースを２ついれる
        if not code_block_flg:
            line = fix_mypage_link(line, dict_title)
            line = fix_newline(line)

        result += line
        result += '\n'
    return result


def remove_bogus_letter(line):
    return re.sub(r'[^a-zA-Z0-9_\-]', '', line)


def extract_post_name(item):
    ix = item['created_at'].find('T')
    created_at = item['created_at'][:ix]

    un_bogus_title = remove_bogus_letter(item['title'])
    if un_bogus_title == '':
        un_bogus_title = item['id']

    return created_at + '-' + un_bogus_title


def create_front_matter(item):
    front_matter = {
        'layout': 'post',
        'title': item['title'],
        'published': ('false' if item['private'] == 'true' else 'true'),
        'tags': map(lambda x: x['name'], item['tags']),
        'created_at: ': item['created_at'],
        'updated_at: ': item['updated_at'],
    }

    return '\n'.join([
        '---',
        yaml.dump(front_matter),
        '---'
    ]) + '\n'


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if argc != 4:
        print(
            "Usage #python %s [userid] [accesstoken] [保存先フォルダ]" % argvs[0])
        exit()

    user = argvs[1]
    token = argvs[2]
    paths = Paths(argvs[3])
    paths.makedirs()

    qiitaApi = qiita_api.QiitaApi(token)

    items = qiitaApi.query_user_items(user)
    dict_title = {}
    for i in items:
        dict_title[i['url']] = extract_post_name(i)

    for i in items:
        print('Trying to save ' + i['title'])

        post_name = extract_post_name(i)
        front_matter = create_front_matter(i)
        text = fix_markdown(paths, i['body'], dict_title)
        with open(os.path.join(paths.posts, post_name + '.md'), 'w', encoding='utf-8') as md_file:
            md_file.write(front_matter)
            md_file.write(text)
