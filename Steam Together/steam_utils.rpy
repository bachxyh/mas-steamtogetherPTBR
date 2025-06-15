init 5 python:
    import os
    import io

    def get_steam_library_paths(steam_path):
        """Returns the paths of the Steam libraries"""
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
        """Returns a list of installed games on Steam"""
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