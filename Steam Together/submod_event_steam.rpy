init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="moni_open_steam_STSUBMOD",
            category=["programa", "steam"],
            prompt="Poderia abrir a Steam para mim?",
            random=False,
            pool=True,
            unlocked=True,
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

label moni_open_steam_STSUBMOD:
    $ steam_exe_path = "C:\\Program Files (x86)\\Steam\\Steam.exe"

    if os.path.exists(steam_exe_path):
        m 1eud "Ah, você quer abrir a Steam, [player]?"
        m 1eub "Me dê só um segundinho.{w=0.1}.{w=0.1}."
        m 1dua "*clic*..."
        $ os.startfile(steam_exe_path)
        m 3hub "Prontinho! Steam aberta!"

        m 3eub "E então... O que você vai jogar hoje?"
        call screen mas_game_menu
        $ selected_game = _return

        if selected_game and selected_game != "cancel":
            python:
                import random
                praise_lines = [
                    "Ótima escolha! {} parece ser muito divertido!".format(selected_game),
                    "Ah, {}? Você tem um ótimo gosto~".format(selected_game),
                    "Hmm... {}? Interessante.".format(selected_game),
                ]
                praise_line = random.choice(praise_lines)

            m 3wub "[praise_line]"

            m 3hub "Você pretende jogar agora ou mais tarde?{nw}"
            $ _history_list.pop()
            menu:
                "Vou jogar agora.":
                    m 3wub "Perfeito! Aproveite bastante, [player]~"
                    m 3rksdlb "Só... não esquece de voltar para passar um tempo comigo, tá bom?"
                    m 1tublb "Eu ficaria com um pouquinho de ciúmes se eu soubesse que você está passando mais tempo em outro jogo..."
                    m 1hub "Mas tudo bem! Se precisar de uma pausa, estarei aqui te esperando."
                    m 3fubsb "Divirta-se muito, viu?"
                    $ mas_idle_mailbox.send_idle_cb("moni_open_steam_STSUBMOD_callback")
                    return "idle"

                "Vou jogar mais tarde.":
                    m 1eua "Ah, tudo bem então!"
                    m 3hub "Se mudar de ideia, é falar."
                    m 1sub "Eu adoro ficar aqui com você, mesmo só conversando ou estando em segundo plano."
                    return

        elif selected_game == "cancel":
            m 1eud "Mudou de ideia?"
            m 1eua "Tudo bem, às vezes é bom apenas dar uma olhada."
            m 3hub "Se quiser jogar depois, estou aqui pra te acompanhar!"
            return

    else:
        m 2wud "Hmm... não consegui encontrar a Steam no seu computador."
        m 1tku "Tem certeza de que ela está instalada?"
        m 5hub "Se quiser, posso tentar de novo depois, ok?"
        return


label moni_open_steam_STSUBMOD_callback:
    $ import datetime
    $ import random

    if persistent.last_game_time:
        $ last_time = datetime.datetime.fromisoformat(persistent.last_game_time)
        $ now = datetime.datetime.now()
        $ time_diff = (now - last_time).total_seconds()
    else:
        $ time_diff = 0

    if time_diff < 300:
        m 1wud "Ah, você voltou muito rápido!"

        $ secret_line_chance = random.random()
        if secret_line_chance < 0.4:
            m 1ttb "Mudou de ideia ou estava fazendo uma speedrun?~"
        else:
            m 1ttb "Mudou de ideia?~"

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
        m 1wub "Ah, você voltou!"
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