from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Player, Team, House

# Signal to create a team when a player is added
@receiver(post_save, sender=Player)
def create_team_for_player(sender, instance, created, **kwargs):
    if created:
        house = instance.house
        print(f"Player created: {instance.first_name} {instance.last_name}")
        # Check if a team already exists for the house
        team, created = Team.objects.get_or_create(house=house)

        # Log if a new team was created
        if created:
            print(f"New team created for house: {house.house_name}")

        # Add the player to the team
        team.players.add(instance)
        print(f"Player {instance.first_name} added to team {house.house_name}")
