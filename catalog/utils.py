def convert_iso_duration(iso_duration):
    # Inicializa minutos y segundos
    minutes = 0
    seconds = 0

    # Verifica si la duración está en formato esperado
    if iso_duration.startswith('PT'):
        # Extrae minutos
        minutes_part = iso_duration[2:].split('M')[0]
        if minutes_part.isdigit():
            minutes = int(minutes_part)

        # Extrae segundos
        seconds_part = iso_duration.split('M')[-1].split('S')[0]
        if seconds_part.isdigit():
            seconds = int(seconds_part)

    return f"{minutes}min {seconds}seg"