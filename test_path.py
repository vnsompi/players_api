import os
from django.conf import settings

json_path = os.path.join(settings.BASE_DIR, "players_api", "cleaned_player_data.json")
print("Chemin :", json_path)
print("Existe :", os.path.exists(json_path))
