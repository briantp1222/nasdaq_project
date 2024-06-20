import time
import logging
from concurrent.futures import ProcessPoolExecutor
import concurrent
from src import sl_dict, store_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_all_tables(d):
    start_time = time.time()
    num_processes = 8
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(store_data.process_data, key) for key in d.keys() if not d[key].get('premium', True)]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error: {str(e)}")
    end_time = time.time()
    logging.info(f"Total time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    d = sl_dict.load('data/info_dict.pkl')
    download_all_tables(d)
