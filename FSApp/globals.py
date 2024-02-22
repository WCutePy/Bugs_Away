from apscheduler.schedulers.background import BackgroundScheduler


activeGames = {}
scheduler = BackgroundScheduler()
scheduler.start()
