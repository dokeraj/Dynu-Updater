import requests
import sqliteDatabase
import hashlib
import time


def getCurrentIp(envs):
    print("Calling ipSource (ipfy) api..")
    timestamp = int(round(time.time() * 1000))

    try:
        ipfyResponse = requests.get(envs.ipSource, timeout=10)
        if ipfyResponse.status_code == 200:
            currentIp = str(ipfyResponse.json()["ip"])
            print(f"Current public IP is: {currentIp}")
            sqliteDatabase.update_db("ipfy", ipfyResponse.status_code, str(currentIp), timestamp)
            return currentIp
        else:
            print(f"Error: Cannot get current public IP address from {envs.ipSource}")
            sqliteDatabase.update_db("ipfy", ipfyResponse.status_code, f"Error getting IP from {envs.ipSource}",
                                     timestamp)
            return None
    except requests.exceptions.Timeout:
        strErr = f"WARN! Timeout has occurred while calling {envs.ipSource}! Will try again in {envs.refreshTime} seconds."
        print(strErr)
        sqliteDatabase.update_db("ipfy", 408, strErr, timestamp)
        return None
    except Exception as e:
        strErr = f"WARN! Error \'{str(e)}\' has occurred while calling {envs.ipSource}! Will try again in {envs.refreshTime} seconds."
        print(strErr)
        sqliteDatabase.update_db("ipfy", 500, strErr, timestamp)
        return None


def updateDynuIp(newIp: str, envs):
    timestamp = int(round(time.time() * 1000))
    if newIp is not None:
        print("Calling dynu Api..")

        md5Pass = hashlib.md5(envs.password.encode('utf-8')).hexdigest()
        requestUrl = f"{envs.dynuUpdateUrl}?hostname={envs.hostnames}&myip={newIp}&password={md5Pass}"

        try:
            response = requests.get(requestUrl, timeout=15)

            if response.status_code == 200 and (response.text == "nochg" or response.text.startswith("good")):
                print(f"-> Success - Response from dynu: {response.text}")
                sqliteDatabase.update_db("dynu", response.status_code, response.text, timestamp)
            else:
                print(
                    f"-> Error - response code: {response.status_code} from DYNU api with message: \'{response.text.strip()}\'. Will try again in {envs.refreshTime} seconds.")
                sqliteDatabase.update_db("dynu", response.status_code, response.text,timestamp)
        except requests.exceptions.Timeout:
            strErr = f"WARN! Timeout has occurred while calling {envs.dynuUpdateUrl}! Will try again in {envs.refreshTime} seconds."
            print(strErr)
            sqliteDatabase.update_db("dynu", 408, strErr, timestamp)
        except Exception as e:
            strErr = f"WARN! Error \'{str(e)}\' has occurred while calling {envs.dynuUpdateUrl}! Will try again in {envs.refreshTime} seconds."
            print(strErr)
            sqliteDatabase.update_db("dynu", 500, strErr, timestamp)

    else:
        errTxt = f"WARN! Before calling dynu API: Public IP address pulled from {envs.ipSource} is not valid - dynu api is not called!"
        print(errTxt)
        sqliteDatabase.update_db("dynu", 0, errTxt, timestamp)
