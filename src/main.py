import pyperclip
from .API.RecordAPI import RecordAPI
from .API.ReasonsAPI import ReasonsAPI
from QuickProject import QproDefaultConsole, QproInfoString, _ask, QproErrorString
from QuickProject.Commander import Commander

level = [
    '<img src="https://api-img.alapi.cn/image/2022/03/03/1faa0ff764bb2e2be38903a443d3beed.jpg" alt=""/>',
    '<img src="https://api-img.alapi.cn/image/2022/03/03/35b05158260697a1fdaf20af4006336d.jpg" alt=""/>',
    '<img src="https://api-img.alapi.cn/image/2022/03/03/6812c5f466cd564428c574ce7f321b64.jpg" alt=""/>'
]
className = '一年级四班'
tcb_env_id = 'class-flower-3gxlc5aza07b4c02'
app = Commander()


def count2level(count):
    if count < 0:
        return str(count)
    res = []
    index = 0
    while count:
        res.append(level[index] * (count % 5))
        count //= 5
        index += 1
    return ''.join(res) if res else '暂无'


@app.command()
def gen():
    """
    生成Markdown文件，半自动上传
    """
    from QuickStart_Rhy import open_file

    reasons = ReasonsAPI.list_reasons_ordered_by_date()
    if not reasons['status']:
        QproDefaultConsole.print(QproErrorString, reasons['message'])
        return
    reasons = reasons['data']

    table = RecordAPI.list_records_order_by_count()
    if not table['status']:
        QproDefaultConsole.print(QproInfoString, table['message'])
        return
    table = table['data']

    with open('dist/index.md', 'w') as f:
        print(f'# {className}小红花榜\n\n<center><a href="#每日明细">点此查看每日明细</a></center>\n', file=f)
        print('|排名|姓名|小红花|\n|:---:|:---:|:---:|', file=f)
        if len(table):
            max_count = table[0]['count']
            cur_rank = 1
            for rank, item in enumerate(table):
                if item['count'] < max_count:
                    cur_rank = rank + 1
                    max_count = item['count']
                print(f'|{cur_rank}|{item["name"]}|{count2level(item["count"])}|', file=f)
        else:
            QproDefaultConsole.print(QproErrorString, '数据库内无小红花记录')
        print('\n## 每日明细\n', file=f)
        if len(reasons):
            has_add = {}
            for item in reasons:
                str_time = item['date'].strftime('%Y年-%m月-%d日')
                if str_time not in has_add:
                    has_add[str_time] = []
                has_add[str_time].append(f'<li>{item["content"]}</li>\n')
            for str_time in has_add:
                print(
f"""<details>
    <summary>{str_time}</summary>
        <ul>
            {''.join(has_add[str_time]).strip()}
        </ul>
</details>""", file=f
                )
        else:
            QproDefaultConsole.print(QproErrorString, '数据库内无明细记录')
        print('## 兑换规则\n\n|图标|兑换方式|\n|:---:|:---:|', file=f)
        print(f'|{level[2]}|5个{level[1]}|', file=f)
        print(f'|{level[1]}|5个{level[0]}|', file=f)
    QproDefaultConsole.print(QproInfoString, 'Markdown文件更新在 "dist/index.md", 已通过Typora打开。')
    QproDefaultConsole.print(QproInfoString, '请将导出的HTML文件放置在public文件夹中。')

    open_file(['dist/index.md'])

    if _ask({
        'type': 'confirm',
        'message': '确认上传至腾讯云部署',
        'name': 'deploy',
        'default': True
    }):
        import os
        os.chdir('public')
        with open('index.html', 'r') as f:
            ct = f.read().split('\n')
        with open('index.html', 'w') as f:
            not_write = True
            for line in ct:
                if line.startswith('<meta') and not_write:
                    not_write = False
                    print('<title>一年级四班小红花榜</title>\n'
                          '<link rel="shortcut icon" href="https://rhythmlian.cn/img/favicon.ico">', file=f)
                print(line, file=f)
        os.system(f'tcb hosting deploy -e {tcb_env_id}')


@app.command()
def daily_update(json_filepath: str = 'dist/update.json'):
    """
    每日更新，默认是用dist/update.json

    :param json_filepath: 每日更新表
    :return:
    """
    import json
    import datetime

    try:
        with open(json_filepath, 'r') as f:
            update_info = json.load(f)
        for item in update_info['stars']:
            res = RecordAPI.update_record(item, update_info['stars'][item])
            if not res['status']:
                QproDefaultConsole.print(QproErrorString, res['message'])
        date = datetime.datetime.today()
        for item in update_info['contents']:
            res = ReasonsAPI.add_reason(date, item)
            if not res['status']:
                QproDefaultConsole.print(QproErrorString, res['message'])
    except:
        QproDefaultConsole.print_exception()
    else:
        QproDefaultConsole.print(QproInfoString, f'{date} 已成功更新!')


@app.command()
def gen_update_template():
    """
    生成一个空白的每日更新表
    """
    import json

    with open('dist/update.json', 'w') as f:
        json.dump(
            {
                'stars': {},
                'contents': []
            },
            f, indent=1
        )
    QproDefaultConsole.print(QproInfoString, '日常更新模板已更新在 "dist/update.json"')


@app.command()
def add_update(contents: str, score: int, names: str = pyperclip.paste()):
    import json
    name_ls = names.strip().split('，')
    with open('dist/update.json', 'r') as f:
        res = json.loads(f.read())
    with open('dist/update.json', 'w') as f:
        res['stars'].update({i: score for i in name_ls})
        res['contents'].append(contents)
        json.dump(res, f, indent=1, ensure_ascii=False)


if __name__ == '__main__':
    app()
