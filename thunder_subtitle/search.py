#!/usr/bin/env python3
# coding: utf-8
import urllib.request
from . import thunder_subs
from drawtable import Table


def search(fp):
    """
    格式化其中一个结果如下：
        {
            'scid': '86AE53FC9D5A2E41E5E9CAB7C1A3794A1B7206B9',
            'sname': '神秘博士2011圣诞篇The.Doctor.The.Widow.And.The.Wardrobe.ass',
            'language': '简体',
            'rate': '4',
            'surl': 'http://subtitle.v.geilijiasu.com/86/AE/86AE53FC9D5A2E41E5E9CAB7C1A3794A1B7206B9.ass',
            'svote': 545,
            'roffset': 4114797192
        }

    每项中需要注意的数据有：
        scid: 猜测为字幕文件的scid
        sname: 字幕文件的原始文件名
        language: 字幕语言
        surl: 字幕下载地址
    """
    # 获取一个本地电影文件名为cid的hash值
    cid = thunder_subs.cid_hash_file(fp)

    info_list = thunder_subs.get_sub_info_list(cid, 1000)
    return info_list


def get_url(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    return data


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='movie path')
    parser.add_argument('-i', '--index', type=int, help='index to download')
    args = parser.parse_args()

    info_list = search(args.path)
    if info_list is None:
        print("超过最大重试次数后仍然未能获得正确结果")
    else:
        info_list.sort(key=lambda x: x['rate'], reverse=True)

        if args.index:
            sub = info_list[args.index - 1]
            name, url = sub['sname'], sub['surl']
            sub_ext = url.rsplit('.', 1)[1]
            data = get_url(url)

            movie_file_path_wo_ext = args.path.rsplit('.', 1)[0]
            sub_file_path = movie_file_path_wo_ext + '.' + sub_ext
            with open(sub_file_path, 'wb') as f:
                f.write(data)
            print('Downloaded {}'.format(sub_file_path))
        else:
            rows = [
                ['Index', 'Rate', 'Votes', 'Language/Name/URL'],
            ]
            for i, x in enumerate(info_list, start=1):
                row = [
                    str(i), x['rate'],
                    str(x['svote']), '{} {}\n{}'.format(
                        x['language'], x['sname'], x['surl'])
                ]
                rows.append(row)

            tb = Table(
                margin_x=1,
                margin_y=0,
                align='left',
                max_col_width=100,
                table_style='base',
            )
            tb.draw(rows)


if __name__ == '__main__':
    main()
