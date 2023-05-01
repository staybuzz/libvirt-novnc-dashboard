from flask import Flask, render_template
import os

app = Flask(__name__)
domains = [{'name': 'spice', 'ostype': 'hvm', 'uuid': 'cdb2fcc2-bf05-43f6-add3-1b8eda5ae1b8', 'id': 3, 'max_memory_in_mb': 131072, 'max_vcpus': 1, 'vnc_port': -1, 'state': 'running', 'state_reason_code': 1}, {'name': 'vnc-test', 'ostype': 'hvm', 'uuid': '4d8fa98a-3e11-4cfa-948c-2826bc5d2928', 'id': 2, 'max_memory_in_mb': 524288, 'max_vcpus': 1, 'vnc_port': 5901, 'state': 'running', 'state_reason_code': 1},{'name': 'vnc-test2', 'ostype': 'hvm', 'uuid': '4d8fa98a-3e11-4cfa-948c-2826bc5d2928', 'id': 2, 'max_memory_in_mb': 524288, 'max_vcpus': 1, 'vnc_port': 5901, 'state': 'running', 'state_reason_code': 1}]

NOVNC_TOKEN_PATH = os.environ.get('NOVNC_TOKEN_PATH' ,'/tmp/novnc_token.cfg')
NOVNC_HOST = os.environ.get('NOVNC_HOST' ,'127.0.0.1')
NOVNC_PORT = os.environ.get('NOVNC_PORT' ,'6080')

@app.route('/')
def resp_vmlist():
  make_novnc_token_list(domains)
  return render_template('vmlist.html', domains=domains, novnc_host=NOVNC_HOST, novnc_port=NOVNC_PORT)

def make_novnc_token_list(domains) -> bool:
  tokens = []
  for dom in domains:
    if dom['vnc_port'] == -1: continue
    token_line = f'{dom["uuid"]}: 127.0.0.1:{dom["vnc_port"]}'
    tokens.append(token_line)
  with open(NOVNC_TOKEN_PATH, 'w') as f:
    f.writelines([line + '\n' for line in tokens])

  return True

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
