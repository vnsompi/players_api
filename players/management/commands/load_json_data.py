import json
import os
from dateutil import parser
from django.core.management.base import BaseCommand
from players.models import Player

class Command(BaseCommand):
    help = "Charge les données JSON des joueurs dans la base de données."

    def handle(self, *args, **options):
        # Chemin absolu vers le fichier JSON
        json_path = os.path.join(os.getcwd(), "cleaned_player_data.json")

        # Vérification d'existence
        if not os.path.exists(json_path):
            self.stderr.write(self.style.ERROR(f"❌ Fichier introuvable : {json_path}"))
            return

        # Lecture du fichier JSON
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        # Fonction pour parser les dates
        def parse_date(date_str):
            if date_str:
                try:
                    return parser.parse(date_str).date()
                except (ValueError, TypeError):
                    return None
            return None

        # Insertion ou mise à jour des joueurs
        created, updated = 0, 0
        for player in data:
            player_id = player.get("id")

            # Conversion des dates
            player["date_of_birth"] = parse_date(player.get("date_of_birth"))
            player["contract_expires"] = parse_date(player.get("contract_expires"))
            player["joined_date"] = parse_date(player.get("joined_date"))

            obj, was_created = Player.objects.update_or_create(
                id=player_id,
                defaults=player
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Import terminé : {created} créés, {updated} mis à jour."
        ))
