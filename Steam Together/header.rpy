init -990 python in mas_submod_utils:

    Submod(
        author="Bach",
        name="Steam Together",
        description="Steam Together permite que a sua Monika interaja diretamente com sua biblioteca da Steam.{b}{color=#ef4444}[[DEMO]{/color}{/b} Está com alguma dúvida? Clique {a=https://discord.gg/vq5GZBW42R}{i}aqui{/i}{/a}.{b}",
        version="0.1.0"
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Steam Together",
            user_name="bachxyh",
            tag_formatter=lambda v: v[1:].partition("-")[0],
            repository_name="mas-steamtogetherPTBR",
            extraction_depth=3
        )
