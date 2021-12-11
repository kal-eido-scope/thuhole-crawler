#!/bin/env python3
import argparse
import hashlib
import json
import os.path
import time

import requests
from tqdm import tqdm

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')


def main():
    parser = argparse.ArgumentParser('THU Hole Crawler')
    parser.add_argument('--email')
    parser.add_argument('--password')
    parser.add_argument('--token')
    parser.add_argument('--valid_code')
    parser.add_argument('--sleep', type=float, default='0.0')
    parser.add_argument('--start', type=int, required=True, help='Inclusion')
    parser.add_argument('--end', type=int, required=True, help='Exclusion')
    args = parser.parse_args()
    sleep = float(args.sleep)
    s = requests.Session()
    if args.token is None:
        # valid code
        assert args.email is not None and args.password is not None, 'Authorization required'
        r = s.post('https://tapi.thuhole.com/v3/security/login/login?&device=0&v=v3.0.6-455336', data={
            'email': args.email,
            'password_hashed': hashlib.sha256(hashlib.sha256(args.password.encode()).hexdigest().encode()).hexdigest(),
            'device_type': '0',
            'device_info': 'Chrome',
            **({} if args.valid_code is None else { 'valid_code', args.valid_code }),
        }).json()
        if r['code'] != 0:
            raise RuntimeError(r['msg'])
        time.sleep(sleep)
        token = r['token']
    else:
        token = args.token
    for i in tqdm(range(args.start, args.end), desc='Posts'):
        post_path = os.path.join(DATA_PATH, 'json', '%06d.json' % i)
        os.makedirs(os.path.dirname(post_path), exist_ok=True)
        if not os.path.isfile(post_path):
            tqdm.write('Request post %d' % i)
            r = s.get('https://tapi.thuhole.com/v3/contents/post/detail?pid=%d&device=0&v=v3.0.6-455336' % i, headers={
                'TOKEN': token,
            })
            post = r.json()
            assert post['code'] == 0 or post['msg'].startswith('找不到这条树洞'), 'Unknown error'
            with open(post_path, 'wb') as f:
                f.write(r.content)
            time.sleep(sleep)
        else:
            with open(post_path) as f:
                post = json.load(f)
        urls = []
        if 'post' in post and post['post']['url']:
            urls.append(post['post']['url'])
        if 'data' in post:
            urls += [item['url'] for item in post['data'] if item['url']]
        for url in tqdm(urls, desc='Images', leave=False):
            try:
                image_path = os.path.join(DATA_PATH, 'images', url)
                if os.path.isfile(image_path):
                    continue
                tqdm.write('Request image %s' % url)
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                r = s.get('https://i.thuhole.com/' + url)
                with open(image_path, 'wb') as f:
                    f.write(r.content)
            except:
                pass


if __name__ == '__main__':
    main()
