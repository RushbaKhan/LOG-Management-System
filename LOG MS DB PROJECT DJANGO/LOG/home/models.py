from django.db import models

#1
class House(models.Model):
    house_id = models.AutoField(primary_key=True)
    house_name = models.CharField(max_length=100, unique=True)
    captain_id = models.IntegerField()
    captain_name = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=15, default=0)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.house_name

#5
class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=100, unique=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    type = models.CharField(max_length=50)
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Game {self.game_name}"

#2
class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, null=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
# Team Model (with Many-to-Many relationship to players)
class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    house = models.OneToOneField(House, on_delete=models.CASCADE)  # One-to-One relationship with House
    players = models.ManyToManyField(Player, related_name="teams")  # Many-to-Many relationship with players

    def __str__(self):
        return f"Team for {self.house.house_name}"


    
#6
class Venue(models.Model):
    venue_id = models.AutoField(primary_key=True)
    venue_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return self.venue_name

#3
class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    game = models.OneToOneField(Game, on_delete=models.CASCADE, null=True, blank=True)  # Use OneToOneField instead of IntegerField
    venue = models.OneToOneField(Venue, on_delete=models.CASCADE, null=True, blank=True)
    scheduled_date = models.DateField()
    status = models.CharField(max_length=20)

    def __str__(self):
        matchhouse = self.matchhouse_set.first()
        house1_name = matchhouse.house1.house_name if matchhouse else 'Unknown House 1'
        house2_name = matchhouse.house2.house_name if matchhouse else 'Unknown House 2'
        venue_name = self.venue.venue_name if self.venue else 'Unknown Venue'
        return f"Match {self.match_id} - {self.game.game_name} | {house1_name} vs {house2_name} at {venue_name}"

#4
class MatchHouse(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    house1 = models.ForeignKey(House, on_delete=models.CASCADE, related_name="matches_as_house1", null=True, blank=True)
    house2 = models.ForeignKey(House, on_delete=models.CASCADE, related_name="matches_as_house2", null=True, blank=True)

    def __str__(self):
        return f"Match {self.match.match_id} - {self.house1.house_name} vs {self.house2.house_name}"



#7
class Ranking(models.Model):
    rank_id = models.AutoField(primary_key=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    points = models.IntegerField()
    position = models.IntegerField()

    def __str__(self):
        return f"Rank {self.position} - {self.house.house_name}"

#8
class PlayerStatistic(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    goals = models.IntegerField()
    assists = models.IntegerField()
    fouls = models.IntegerField()
    yellow_cards = models.IntegerField()
    red_cards = models.IntegerField()

    def __str__(self):
        return f"Stats for {self.player.first_name} {self.player.last_name}"

#9
class MatchStatistic(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    house1 = models.ForeignKey(House, on_delete=models.CASCADE, related_name="match_statistics_as_house1", null=True, blank=True)
    house2 = models.ForeignKey(House, on_delete=models.CASCADE, related_name="match_statistics_as_house2", null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"Statistics for Match {self.match.match_id}: {self.house1.house_name} vs {self.house2.house_name}"

#10
class MatchResult(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    result_id = models.AutoField(primary_key=True)
    scores = models.CharField(max_length=100)
    winner = models.CharField(max_length=100)

    def __str__(self):
        return f"Result for Match {self.match.match_id}"

#11
class GameRule(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rule = models.TextField()

    def __str__(self):
        return f"Rule for {self.game.game_name}"

#12
class MatchSchedule(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    schedule_date = models.DateField()

    def __str__(self):
        return f"Schedule for Match {self.match.match_id} at {self.venue.venue_name} on {self.schedule_date}"
