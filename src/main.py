import pyperclip
from .API.RecordAPI import RecordAPI
from .API.ReasonsAPI import ReasonsAPI
from QuickProject import QproDefaultConsole, QproInfoString, _ask, QproErrorString
from QuickProject.Commander import Commander

#level = [
#    '<img src="https://api-img.alapi.cn/image/2022/03/03/1faa0ff764bb2e2be38903a443d3beed.jpg" alt=""/>',
#    '<img src="https://api-img.alapi.cn/image/2022/03/03/35b05158260697a1fdaf20af4006336d.jpg" alt=""/>',
#    '<img src="https://api-img.alapi.cn/image/2022/03/03/6812c5f466cd564428c574ce7f321b64.jpg" alt=""/>'
#]
level = [
    '<img src="https://cos.rhythmlian.cn/ImgBed/49927c57ee9516a776b922c5b169039a.png" alt=""/>',
    '<img src="https://cos.rhythmlian.cn/ImgBed/8fa034465d839efda7188470f88a5c72.png" alt=""/>',
    '<img src="https://cos.rhythmlian.cn/ImgBed/19d1f8e6e0a614d4a3b48920050c66c7.png" alt=""/>'
]

className = '一年级四班'
tcb_env_id = 'class-flower-3gxlc5aza07b4c02'
font_size = 20
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
    自动生成HTML表单并上传
    """
    import os
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

    with open('dist/template.html', 'r') as f:
        template = f.read()
    table_content = ''
    detail_content = ''
    if not os.path.exists('public') or not os.path.isdir('public'):
        os.mkdir('public')
    with open('public/index.html', 'w') as f:
        max_count = table[0]['count']
        cur_rank = 1
        for rank, record in enumerate(table):
            if record['count'] < max_count:
                cur_rank = rank + 1
                max_count = record['count']
            table_content += '<tr>'
            table_content += '<td style="text-align:center;"><span style="font-size: {}px"><b>{}</b></span></td>'.format(font_size, cur_rank)
            table_content += '<td style="text-align:center;"><span style="font-size: {}px"><b>{}</b></span></td>'.format(font_size, record['name'])
            table_content += '<td style="text-align:center;"><span style="font-size: {}px"><b>{}</b></span></td>'.format(font_size, count2level(record['count']))
            table_content += '</tr>'
        if len(reasons):
            has_add = {}
            for item in reasons:
                str_time = item['date'].strftime('%Y年-%m月-%d日')
                if str_time not in has_add:
                    has_add[str_time] = []
                has_add[str_time].append(f'<li>{item["content"]}</li>\n')
            for str_time in has_add:
                detail_content += f"""<details>
    <summary>{str_time}</summary>
        <ul>
            {''.join(has_add[str_time]).strip()}
        </ul>
</details>"""
        else:
            QproDefaultConsole.print(QproErrorString, '数据库内无明细记录')
        template = template.replace('__CLASS_NAME__', className)
        f.write(template.replace('__CLASS_FLOWER_TBODY_CONTENT__', table_content).replace('__CLASS_FLOWER_DETAIL_CONTENT__', detail_content))

    if _ask({
        'type': 'confirm',
        'message': '确认上传至腾讯云部署',
        'name': 'deploy',
        'default': True
    }):
        import os
        os.chdir('public')
        os.system(f'tcb hosting deploy -e {tcb_env_id}')


@app.command()
def daily_update(json_filepath: str = 'dist/update.json'):
    """
    每日更新，默认用dist/update.json

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
    """
    添加加分项

    :param contents: 加分理由
    :param score: 整数分数
    :param names: 以中文逗号分隔的姓名字符串，默认从粘贴板获取
    :return:
    """
    import json
    name_ls = names.strip().split('，') if '，' in names else names.strip().split(',')
    with open('dist/update.json', 'r') as f:
        res = json.loads(f.read())
    with open('dist/update.json', 'w') as f:
        res['stars'].update({i: score for i in name_ls})
        res['contents'].append(contents)
        json.dump(res, f, indent=1, ensure_ascii=False)


if __name__ == '__main__':
    app()
