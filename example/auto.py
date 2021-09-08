#! python3
# -*- coding:utf-8 -*-
import os
import re
import json
import shutil

BASE_PATH = os.path.dirname(__file__)

def main():
    annex_path = input('请输入附件绝对路径（没有则跳过）：').strip()
    while annex_path != '' and not os.path.exists(annex_path):
        print("[!] 附件不存在")
        annex_path = input('请输入附件绝对路径（没有则跳过）：').strip()
    
    type = input("请输入题目类型：").strip().lower()
    while type not in ['web', 'pwn', 'crypto', 'misc', 'android', 'eth', 'iot', 'ai', '实战', '靶场']:
        print("[!] 题目类型有误")
        type = input("请输入题目类型：").strip().lower()
    
    title = input("请输入题目名（例如[NSSCTF 2021]test）：").strip()
    desc = input("请输入题目描述（没有则跳过）：").strip()
    tag = input("请输入题目标签（多个标签以,隔开）：").strip().split(',')
    hint = input("请输入题目提示（没有则跳过）：").strip()
    static_flag = input("请输入题目静态flag（动态请跳过）：").strip()
    if static_flag != '' and not static_flag.startswith('NSSCTF{'):
        print("[!] 请使用NSSCTF{}格式。")
        static_flag = input("请输入题目静态flag（动态请跳过）：").strip()

    redirect_type = input("请输入转发类型（0->http，1->tcp/udp，没有docker则跳过）").strip()
    no_docker = True
    while redirect_type != '' and redirect_type not in '12':
        print("[!] 转发类型有误")
        redirect_type = input("请输入转发类型（0->http，1->tcp/udp，没有docker则跳过）").strip()
        
    
    if redirect_type != '':
        no_docker = False
    docker = ''
    if not no_docker:
        while True:
            try:
                redirect_port = int(input("请输入转发端口：").strip())
                if redirect_port < 0 or redirect_port > 65535:
                    print("[!] 转发端口有误")
                else:
                    break
            except Exception:
                print("[!] 转发端口有误")

        docker = input("请输入已经上传至dockerhub的完整名字（包含Dockerfile文件则跳过）：").strip()
    
    res = re.findall('\[(.+) (\d+)(.+)?\](.+)', title)
    
    path = '_'.join([c.lower()for c in res[0] if c != '' ])
    
    path = os.path.join(BASE_PATH, path)
    os.mkdir(path)
    
    if not os.path.exists(path):
        print("[!] %d文件夹创建失败" % path)
        exit(-1)
        
    ext = ''
    if title.find('.') != -1:
        ext = '.' + title.split('.')[-1]
    if annex_path != '':
        shutil.copy(annex_path, os.path.join(path, '附件%s' % (ext)))

    
    if no_docker:
        json_data = {
            "title": title,
            "description": desc,
            "tag": tag,
            "hint": hint if hint else None,
            "annex": ('./附件%s' % ext) if annex_path else None,
            "flag_type": 0,
            "static_flag": static_flag,
            "type": type
        }
    else:
        json_data = {
                "title": title,
                "description": desc,
                "tag": tag,
                "hint": hint if hint else None,
                "annex": ('./附件%s' % ext) if annex_path else None,
                "flag_type": 0,
                "static_flag": static_flag,
                "type": type,
                "redirect_type": redirect_type,
                "redirect_port": redirect_port,
                "docker": docker if docker else None,
                "flag_type": 1,
        }
    with open(os.path.join(path, 'problem.json'), 'w+') as f:
        json.dump(json_data, f)
    
    if not no_docker and docker == '':
        print('[+] 检测到没有提交docker名称，请手动将dockerfile以及所需文件移动至文件夹内')
    
    print('[+] 创建结束，目录生成在%s' % path)    

if __name__ == '__main__':
    main()
