import libvirt
from xml.etree import ElementTree as ET

LIBVIRT_DOMAIN_STATES = {libvirt.VIR_DOMAIN_NOSTATE: 'nostate',
                         libvirt.VIR_DOMAIN_RUNNING: 'running',
                         libvirt.VIR_DOMAIN_BLOCKED: 'blocked',
                         libvirt.VIR_DOMAIN_PAUSED: 'paused',
                         libvirt.VIR_DOMAIN_SHUTDOWN: 'shutdown',
                         libvirt.VIR_DOMAIN_SHUTOFF: 'shutoff',
                         libvirt.VIR_DOMAIN_CRASHED: 'crached',
                         libvirt.VIR_DOMAIN_PMSUSPENDED: 'pmsuspended'}

def get_vnc_port(dom) -> int:
  vmXml = dom.XMLDesc(0)
  root = ET.fromstring(vmXml)
  graphic_type = root.find('./devices/graphics').get('type')
  if graphic_type != 'vnc':
    print(f'VM "{dom.name()}" does not have vnc console. graphic_type is {graphic_type}.')
    return -1

  vnc_port = int(root.find('./devices/graphics').get('port'))
  return vnc_port

def get_domains(conn) -> dict:
  print('get_domains')
  domains = conn.listAllDomains(0)
  if len(domains) == 0:
    return []

  domain_dicts = []
  for dom in domains:
    domain_dict = {
                    'name': dom.name(),
                    'ostype': dom.OSType(),
                    'uuid': dom.UUIDString(),
                    'id': dom.ID(),
                    'max_memory_in_mb': dom.maxMemory(),
                    'max_vcpus': dom.maxVcpus(),
                    'vnc_port': get_vnc_port(dom),
                    #'time': dom.getTime(), # needs QEMU Guest Agent
                    #'hostname': dom.hostname(), # needs QEMU Guest Agent
                  }
    state, reason = dom.state()
    if not state in LIBVIRT_DOMAIN_STATES:
      domain_dict.update({'state': 'unknown'})
    else:
      domain_dict.update({'state': LIBVIRT_DOMAIN_STATES[state]})
    domain_dict.update({'state_reason_code': reason})

    domain_dicts.append(domain_dict)

  return domain_dicts

libvirt_host = 'qemu:///system'
conn = libvirt.open(libvirt_host)
if conn is None:
  print(f'Failed to open connection to {libvirt_host}')

domains = get_domains(conn)
print(domains)
