from apscheduler.schedulers.background import BackgroundScheduler

import EnvVars
import apiCalls
import api_controller
import sqliteDatabase


def mainTask(envs):
    print("\n\n")

    newIp = apiCalls.getCurrentIp(envs)
    apiCalls.updateDynuIp(newIp, envs)


def scheduled_task(envs):
    mainTask(envs)


# run the first time
print("STARTING SCRIPT..")

# get all env vars
print("Reading global vars..")
globalEnvs = EnvVars.read_envs()

# initialize the db
print("Initializing sqlite database..")
sqliteDatabase.init_db(r"/pyScript/nova.db")

# run for the first time
mainTask(globalEnvs)

scheduler = BackgroundScheduler()
job = scheduler.add_job(lambda: scheduled_task(globalEnvs), 'interval', seconds=globalEnvs.refreshTime)

scheduler.start()

api_controller.runApi()
