
#1. Task to count all player objects  --count_player
#2.Task to update Player DB -update_players_from_json
import os
import json
import logging
from celery import shared_task
from dateutil import parser
from players.models import Player  # adapte selon ton projet
from django.conf import settings

@shared_task
def count_players():

    count = Player.objects.count()

    return f"Number of players: {count}"


logger = logging.getLogger(__name__)



@shared_task
def update_players_from_json():
    """
    Tâche Celery pour mettre à jour les joueurs existants
    depuis un fichier JSON situé dans le dossier BASE_DIR.
    Aucun nouveau joueur n'est créé.
    """

    # 1. Construire le chemin vers le fichier JSON
    json_path = os.path.join(settings.BASE_DIR, "cleaned_player_data.json")

    # 2. Vérifier l'existence du fichier
    if not os.path.exists(json_path):
        logger.error(f"❌ Fichier introuvable : {json_path}")
        return {"updated": 0, "skipped": 0, "error": "Fichier introuvable"}

    # 3. Charger le contenu JSON
    try:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Erreur lors de la lecture du JSON : {e}")
        return {"updated": 0, "skipped": 0, "error": str(e)}

    # 4. Fonction utilitaire pour parser les dates
    def parse_date(date_str):
        if date_str:
            try:
                return parser.parse(date_str).date()
            except (ValueError, TypeError):
                return None
        return None

    # 5. Mise à jour des joueurs existants
    updated, skipped = 0, 0
    for player in data:
        player_id = player.get("id")
        if not player_id:
            logger.warning(f"⚠️ Joueur sans ID ignoré : {player}")
            skipped += 1
            continue

        try:
            obj = Player.objects.get(id=player_id)

            # Conversion des champs de date
            player["date_of_birth"] = parse_date(player.get("date_of_birth"))
            player["contract_expires"] = parse_date(player.get("contract_expires"))
            player["joined_date"] = parse_date(player.get("joined_date"))

            # Mise à jour des champs
            for field, value in player.items():
                setattr(obj, field, value)
            obj.save()

            updated += 1
        except Player.DoesNotExist:
            logger.info(f"⏭ Joueur inexistant ignoré (id={player_id})")
            skipped += 1

    # 6. Log final
    logger.info(f"✅ Mise à jour terminée : {updated} joueurs mis à jour, {skipped} ignorés.")
    return {"updated": updated, "skipped": skipped}