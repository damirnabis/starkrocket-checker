import requests
from progress.bar import IncrementalBar
import time
import pandas as pd



with open("wallets.txt", "r") as file:
    wallets = [row.strip() for row in file]


wallets_res  = []
eligible_res = []
points_res   = []


def main():
    bar = IncrementalBar('Progress', max = len(wallets))

    for wallet in wallets:
        wallets_res.append(wallet)

        url = f'https://starkrocket.xyz/api/check_wallet?address={wallet}'

        response = requests.get(url)

        if response.status_code == 200:
            resp_json = response.json()

            eligible_res.append(resp_json['result']['eligible'])

            points_res.append(resp_json['result']['points'])

        else:
            error_text = f'error <{response.status_code}>'
            
            eligible_res.append(error_text)

            points_res.append(error_text)

        bar.next()
        time.sleep(1)

    data_res = {'wallet': wallets_res,
                'eligible': eligible_res, 
                'points': points_res
                }
        
    df_res = pd.DataFrame(data_res)
 
    df_res.to_csv(f'result.csv', encoding='utf-8')

    bar.finish()
        
    print(f'Total points: {sum(points_res)}')


if __name__ == '__main__':
    main()