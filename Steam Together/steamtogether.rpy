init 5 python:
    import os
    import io

    def get_steam_library_paths(steam_path):
        """Retorna os caminhos das bibliotecas da Steam"""
        library_folders_path = os.path.join(steam_path, 'steamapps', 'libraryfolders.vdf')
        library_paths = []
        
        if os.path.exists(library_folders_path):
            with open(library_folders_path, 'r') as file:
                library_folders = file.read()
            
            for line in library_folders.splitlines():
                if 'path' in line:
                    path = line.split('"')[3]
                    library_paths.append(path)
        
        return library_paths

    def get_installed_games(steam_path):
        """Retorna uma lista dos jogos instalados na Steam"""
        installed_games = []
        library_paths = get_steam_library_paths(steam_path)
        
        for library_path in library_paths:
            steamapps_path = os.path.join(library_path, 'steamapps')
            if os.path.exists(steamapps_path):
                for file in os.listdir(steamapps_path):
                    if file.endswith('.acf'):
                        game_info_path = os.path.join(steamapps_path, file)
                        with open(game_info_path, 'r') as game_file:
                            game_info = game_file.read()
                            if '"name"' in game_info:
                                game_name = game_info.split('"name"')[1].split('"')[1]
                                installed_games.append(game_name)
        
        return installed_games

    steam_path = "C:\\Program Files (x86)\\Steam"
    installed_games = get_installed_games(steam_path)

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="moni_openyour_steam",  
            category=['programa'],
            prompt="Poderia abrir a Steam para mim?",
            random=False,
            pool=True,
        )
    )

screen mas_game_menu():
    modal True
    zorder 200

    frame:
        style_prefix "choice"
        xpos 980
        ypos 100
        xsize 300
        ysize 500
        background None

        has vbox
        spacing 10
        text "{i}Jogos Instalados{/i}" size 40 xalign 0.5

        viewport:
            scrollbars "vertical"
            mousewheel True
            draggable True
            ysize 400

            has vbox
            spacing 5
            for game in installed_games:
                textbutton game:
                    action Return(game)
                    style "choice_button"
                    xfill True
            textbutton "Deixa pra lá":
                action Return("cancel")
                style "choice_button"
                xfill True

label moni_openyour_steam:
    $ steam_exe_path = "C:\\Program Files (x86)\\Steam\\Steam.exe"

    if os.path.exists(steam_exe_path):
        m 1eud "Ah, quer abrir a Steam, [player]?"
        m 1eub "Dê-me só um segundo..."
        m 1dua "..."
        $ os.startfile(steam_exe_path)
        m 3hub "Prontinho! Steam aberta!"

        m 3eub "Agora, me diga: o que você vai jogar hoje?"
        call screen mas_game_menu  
        $ selected_game = _return

        if selected_game and selected_game != "cancel":
            m 3wub "Ótima escolha! [selected_game] parece bem divertido!"
            
            m 3hub "Você vai jogar agora ou depois?{nw}"
            $ _history_list.pop()
            menu:
                "Vou jogar agora.":
                    m 3wub "Entendi! Então aproveite bastante o jogo, [player]!"
                    m 3rksdlb "Mas não se esqueça de voltar para passar um tempinho comigo depois, tá bem?"
                    m 1tublb "Posso ficar com inveja se você passar muito tempo em outro jogo sem mim."
                    m 1hub "Se precisar de uma pausa, estarei aqui, esperando por você!"
                    m 3fubsb "Enfim, espero que você se divirta muito!"
                    $ mas_idle_mailbox.send_idle_cb("moni_openyour_steam_callback")
                    return "idle"

                "Vou jogar mais tarde.":
                    m 1eua "Ah, tudo bem!"
                    m 3hub "Se mudar de ideia, é só me avisar."
                    return

label moni_openyour_steam_callback:
    $ import datetime
    
    if persistent.last_game_time:
        $ last_time = datetime.datetime.fromisoformat(persistent.last_game_time)
        $ now = datetime.datetime.now()
        $ time_diff = (now - last_time).total_seconds()
    else:
        $ time_diff = 0

    if time_diff < 300:
        m 1wud "Ah, você voltou muito rápido!"
        m 1ttb "Mudou de ideia ou estava fazendo uma speedrun?~"

        $ _history_list.pop()
        menu:
            "Só estou fazendo uma pausa.":
                m 3hub "Entendi!"
                m 5ekb "Pausas são importantes! Ficar muito tempo olhando para a tela não é bom, e não quero que você se sinta sem energia."
                m 7ekb "Quando for voltar a jogar, me avise, tá bem?"

            "Sim, já terminei!":
                m 1wub "Sério?"
                m 2sub "E então, como foi? Se divertiu?"
                m 2tku "Espero que tenha sido divertido, mas não tanto a ponto de me esquecer~"

    elif time_diff < 1800:
        m 1wub "Ah, você voltou! 
        m 7eub "Já terminou de jogar, [player]?"

        $ _history_list.pop()
        menu:
            "Só estou fazendo uma pausa.":
                m 3hub "Entendi!"
                m 5ekb "Pausas são importantes! Ficar muito tempo olhando para a tela não é bom, e não quero que você se sinta sem energia."
                m 7ekb "Quando for voltar a jogar, me avise, tá bem?"

            "Sim, já terminei!":
                m 1wub "Sério?"
                m 2sub "E então, como foi? Se divertiu?"
                m 2tku "Espero que tenha sido divertido, mas não tanto a ponto de me esquecer~"

    else:
        m 7wud "Nossa, você ficou jogando por tanto tempo assim?"
        m 2ttb "O jogo era tão bom assim, ou será que você esqueceu de mim?~"
        m 1eua "Ahaha~ Estou apenas te provocando."
        m 5fkb "O importante é que você tenha aproveitado."

    return