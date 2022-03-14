import argparse
import subprocess
import requests
import psutil

parser = argparse.ArgumentParser(
    '''
    backup your data by tdbackup tools. 
    1. configure tdbackup tool
    2. fast backup use default policy
    3. add your custom backup policy
    '''
)

subparsers = parser.add_subparsers(dest='command')
subparsers.required = True
config_parser = subparsers.add_parser(
    'config', help='prepare tdbackup tools')
config_parser.add_argument('--server_alias', type=str,
                           default='tdbackup_server', help='server_alias')
config_parser.add_argument('--server_url', type=str,
                           default='http://minio-tdbackup-offline.te.td:9000')
config_parser.add_argument('--AccessKey', type=str, default='ai_vision')
config_parser.add_argument('--SecretKey', type=str,
                           default='"~(TB%PgLW2e<uz$OHJ}k"')

oneshot_backup_parser = subparsers.add_parser(
    'fast-backup', help='one shot backup for dl training data')
oneshot_backup_parser.add_argument(
    '--name', type=str, help='backup policy name', required=True)
oneshot_backup_parser.add_argument('--data_path', type=str,
                                   help='your data absolute path', required=True)
oneshot_backup_parser.add_argument('--server_alias', type=str,
                                   help='server alias', default='tdbackup_server')


add_backup_policy_parser = subparsers.add_parser(
    'add', help='add extra backup policy.')
add_backup_policy_parser.add_argument(
    '--name', type=str, required=True, help='backup policy name')
add_backup_policy_parser.add_argument(
    '--data_path', type=str, required=True, help='the absolute path of your data')
add_backup_policy_parser.add_argument(
    '--cron_str', type=str, required=True, help='cron tab str')
add_backup_policy_parser.add_argument(
    '--server_alias', type=str, default='tdbackup_server')

def get_network_name():
    interfaces = psutil.net_if_addrs()
    wlan_network = ""
    for k, v in interfaces.items():
        address = v[0].address
        if "10.5" in address:
            wlan_network = k
            break
    return wlan_network

def download_tdbackup():
    '''
    download tdbackup tools from server.
    '''
    headers = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBY2Nlc3NLZXkiOiJiaW4ud2FuZyIsIlNlY3JldEtleSI6ImlWR0dGcFRCNURGNnk5eGpvYSIsImV4cCI6MTk0NTE1MTYzNCwiaXNzIjoiYmluLndhbmcifQ.6OMAAwSMbYSsIoiDQW-GXZUOWA6IBCU-S0tTQy9ogMM',
    }
    params = (
        ('path', '~/soft/tdbackup'),
    )
    response = requests.get(
        'http://minio-tdbackup-offline.te.td:8488/object/get?path=~/db-package/tdbackup', headers=headers, params=params)
    with open('tdbackup', 'wb') as f:
        f.write(response.content)
    return


def configure_backup_host(server_alias,
                          host_url,
                          AccessKey,
                          SecretKey):
    status, _ = subprocess.getstatusoutput('./tdbackup')
    if status == 1:
        print('tdbackup tools has already configure.')
        print('current server host:')
        subprocess.run('./tdbackup config host ls'.split())
    else:
        print('downloading tdbackup tools ...')
        download_tdbackup()
        _ = subprocess.getoutput('chmod a+x ./tdbackup')

    print(f'add host alias {server_alias}')
    config_cmd = f'./tdbackup config host add {server_alias} {host_url} {AccessKey} {SecretKey}'
    print(config_cmd)
    out = subprocess.getoutput(config_cmd)
    print(out)
    return


def start_tdbackup_agent(server_alias: str,
                         token: str = '',
                         interface: str = 'eno1'):
    r = subprocess.run(['pgrep', 'tdbackup'], stdout=subprocess.DEVNULL)
    if r.returncode != 0:
        print('start tdbackup serivce')
        start_cmd = f'./tdbackup agent --start {"--token " + token if token else ""} -i {interface}  --backup_set_bucket tdbackup-ai-vision -d -l /tmp/tdbackup_daemon.log {server_alias}'
        print(start_cmd)
        r = subprocess.run(start_cmd.split(), check=True, stderr=subprocess.STDOUT)
    else:
        print('tdbackup service has already start by your peer!')


def add_backup(name: str, data_path: str,
               server_alias: str, cron_str: str,
               interface: str = 'eno1',
               expiration_days=0,
               full=False):
    cmd = f'./tdbackup bp add file --name={name} --source={data_path} -i {interface} --scheduler="{cron_str}" --ed {expiration_days} --backup_set_bucket tdbackup-ai-vision'
    if full:
        cmd += f' --full {server_alias}'
    else:
        cmd += f' {server_alias}'
    print(cmd)
    output = subprocess.getoutput(cmd)
    print(output)
    return


def oneshot_backup(name: str, data_path: str,
                   server_alias: str, interface: str = 'eno1'):
    # latest backup at 3:00 on Sunday
    latest_cron_str = "0 3 * * 0"
    add_backup(f'{name}_latest', data_path,
               server_alias, latest_cron_str, interface)

    # 每月1号凌晨4点进行备份，保留200天
    expiration_days = 200
    add_backup(f'{name}', data_path,
               server_alias, f"0 4 1 * *", interface, expiration_days, full=True)


if __name__ == '__main__':
    args = parser.parse_args()
    interface = get_network_name()
    if args.command == 'config':
        configure_backup_host(args.server_alias, args.server_url,
                              args.AccessKey, args.SecretKey)
        start_tdbackup_agent(args.server_alias, interface=interface)
    if args.command == 'fast-backup':
        oneshot_backup(args.name, args.data_path, args.server_alias, interface=interface)
    if args.command == 'add':
        add_backup(args.name, args.data_path, args.server_alias, args.cron_str, interface=interface)
