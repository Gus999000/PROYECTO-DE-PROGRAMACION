def time_to_minutes(time):
    Time = time
    minutes = 0
    seconds = 0

    # Transformar a minutos:segundos
    if Time >= 60:
        minutes = int(Time/60)
        seconds = Time - (minutes*60)
    else:
        seconds = Time

    #Transformar a cadena de texto

    if minutes < 10 and seconds < 10:
        minutes = str(minutes)
        seconds = str(seconds)
        Time = "0" + minutes + ":" + "0" + seconds
    elif minutes < 10 and seconds >= 10:
        minutes = str(minutes)
        seconds = str(seconds)
        Time = "0" + minutes + ":" + seconds
    elif minutes >= 10 and seconds < 10:
        minutes = str(minutes)
        seconds = str(seconds)
        Time = minutes + ":" + "0" + seconds
    else:
        minutes = str(minutes)
        seconds = str(seconds)
        Time = minutes + ":" + seconds

    return Time

def test():
    print(time_to_minutes(600))
test()