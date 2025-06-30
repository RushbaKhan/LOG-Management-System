from django.shortcuts import render, redirect, get_object_or_404
from .models import Player, House, Game # Replace with your actual model name
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.template.loader import render_to_string

#login
def user_login(request):
    if request.method == 'POST':
        print('POST request received')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f'Username: {username}, Password: {password}')
        if username == 'log123' and password == 'fast1234':
            print('Credentials are correct')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print('User authenticated')
                login(request, user)
                return redirect('dashboard')
            else:
                print('Authentication failed')
                return render(request, 'login.html', {'error': 'Invalid username or password'})
        else:
            print('Invalid credentials')
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    print('GET request received')
    return render(request, 'login.html')

#dashboard
def dashboard(request):
    return render(request, 'Dashboard.html')

#Player
def add_player(request):
    if request.method == "POST":
        # Get data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        house_name = request.POST.get('house')
        game_name = request.POST.get('game')

        # Debugging: Print the received form data
        print(f"Received Data - First Name: {first_name}, Last Name: {last_name}, Phone Number: {phone_number},Email: {email}, House: {house_name}, Game: {game_name}")

        # Ensure all fields are provided
        if not first_name or not last_name or not phone_number or not email or not house_name or not game_name:
            error_message = "All fields are required. Please fill in all fields."
            houses = House.objects.all()
            games = Game.objects.all()
            return render(request, 'AddPlayer.html', {'error_message': error_message, 'houses': houses, 'games': games})

        # Fetch house and game objects
        try:
            house = House.objects.get(house_name=house_name)
        except House.DoesNotExist:
            house = None
            print(f"House not found: {house_name}")

        try:
            game = Game.objects.get(game_name=game_name)
        except Game.DoesNotExist:
            game = None
            print(f"Game not found: {game_name}")

        # Check if house or game is not found
        if not house or not game:
            error_message = "Invalid house or game selected. Please try again."
            houses = House.objects.all()
            games = Game.objects.all()
            return render(request, 'AddPlayer.html', {'error_message': error_message, 'houses': houses, 'games': games})
        # Create player if all fields are valid
        try:
            player = Player.objects.create(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
                house=house,
                game=game
            )
            success_message = "Player added successfully!"
            print(f"Player created: {player}")
            return render(request, 'AddPlayer.html', {'success_message': success_message, 'houses': House.objects.all(), 'games': Game.objects.all()})

        except Exception as e:
            # Catch any other errors during player creation
            print(f"Error creating player: {str(e)}")
            error_message = "An error occurred while adding the player. Please try again."
            return render(request, 'AddPlayer.html', {'error_message': error_message, 'houses': House.objects.all(), 'games': Game.objects.all()})
    # If it's a GET request, render the form
    houses = House.objects.all()
    games = Game.objects.all()
    return render(request, 'AddPlayer.html', {'houses': houses, 'games': games})

#view players
def view_players(request):
    try:
        # Get the search query from the request
        query = request.GET.get('q', '')

        # Fetch all players initially
        players = Player.objects.all()

        # Filter players based on the search query
        if query:
            players = players.filter(
                first_name__icontains=query  # Search by first name
            ) | players.filter(
                last_name__icontains=query  # Search by last name
            ) | players.filter(
                house__name__icontains=query  # Search by house name
            ) | players.filter(
                game__name__icontains=query  # Search by game name
            )

        # Check if it's an AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('partials/player_table.html', {'players': players})
            return JsonResponse({'html': html})

        # Pass the query and players to the template for non-AJAX requests
        return render(request, 'ViewPlayers.html', {'players': players, 'query': query})
    
    except Exception as e:
        # Handle errors gracefully
        error_message = f"An error occurred while fetching players: {str(e)}"
        return render(request, 'ViewPlayers.html', {'error_message': error_message})
       
#edit players
def edit_player(request, player_id):
    # Retrieve the player object
    player = get_object_or_404(Player, player_id=player_id)
    houses = House.objects.all()  # Fetch all houses for the dropdown
    games = Game.objects.all()    # Fetch all games for the dropdown

    if request.method == "POST":
        # Get data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        house_name = request.POST.get('house')   # Get the house value from the form
        game_name = request.POST.get('game')

        try:
            # Get corresponding House and Game objects
            house = get_object_or_404(House, house_name=house_name)
            game = get_object_or_404(Game, game_name=game_name)
        except:
            error_message = "Invalid house or game selection."
            return render(request, 'EditPlayer.html', {'player': player, 'houses': houses, 'games': games, 'error_message': error_message})
        
        # Update the player object with new values
        player.first_name = first_name
        player.last_name = last_name
        player.phone_number = phone_number
        player.email = email
        player.house = house
        player.game = game
        player.save()  # Save changes to the database

        success_message = "Player details updated successfully!"
        return render(request, 'EditPlayer.html', {'player': player, 'houses': houses, 'games': games, 'success_message': success_message})

    # For GET request, render the form prefilled with existing player data
    return render(request, 'EditPlayer.html', {'player': player, 'houses': houses, 'games': games})

#delete player
def delete_player(request, player_id):
    # Get the player object or return 404 if not found
    player = get_object_or_404(Player, player_id=player_id)

    
    if request.method == 'POST':
        player.delete()  # Delete the player from the database
        return redirect('view_players')  # Redirect to the players list view

    # If it's a GET request, you can render a confirmation page or redirect as needed
    return render(request, 'DeletePlayer.html', {'player': player})



#House Statisttics
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from .models import House, Game, Match, MatchHouse, MatchResult

def house_stats(request, house_name):
    # Format house name properly
    house_name = house_name.strip().capitalize()

    # Fetch all matches where the house is involved
    match_houses = MatchHouse.objects.filter(
        house1__house_name__iexact=house_name
    ) | MatchHouse.objects.filter(
        house2__house_name__iexact=house_name
    )

    # Fetch games related to those matches
    games = [matchhouse.match.game for matchhouse in match_houses if matchhouse.match.game]

    # Background and color setup
    house_colors = {
        "Ares": "#800000",
        "Kronos": "#228B22",
        "Zeus": "#00008B",
        "Apollo": "#DAA520",
    }
    house_backgrounds = {
        "Ares": "red.jpeg",
        "Kronos": "green.jpg",
        "Zeus": "blue.jpg",
        "Apollo": "yellow.jpeg",
    }

    house_color = house_colors.get(house_name, "#FFFFFF")
    background_image = house_backgrounds.get(house_name, "default.jpg")

    # Prepare data for charts
    data = {
        'Game': [game.game_name for game in games],
        'Score': [game.score if game.score is not None else 0 for game in games],
    }
    df = pd.DataFrame(data)

    # Check if DataFrame is empty
    if df.empty:
        return render(request, 'HouseStats.html', {
            'house_name': house_name,
            "house_color": house_color,
            "background_image": background_image,
            'total_points': 0,
            'current_rank': 'N/A',
            'games': [],
        })

    # Total points for the current house
    total_points = df['Score'].sum()

    # Calculate rank by total score for all houses from MatchResult
    house_scores = []
    for house in House.objects.all():
        house_matches = MatchHouse.objects.filter(
            match__game__house=house
        )
        total_score = 0
        for matchhouse in house_matches:
            match_result = MatchResult.objects.filter(match=matchhouse.match).first()
            if match_result:
                if matchhouse.house1 == house:
                    total_score += int(match_result.scores.split("-")[0])
                elif matchhouse.house2 == house:
                    total_score += int(match_result.scores.split("-")[1])
        house_scores.append((house.house_name, total_score))

    # Sort houses by their scores in descending order
    sorted_house_scores = sorted(house_scores, key=lambda x: x[1], reverse=True)

    # Find the rank of the current house
    current_rank = 1  # Default rank starts at 1
    for house, score in sorted_house_scores:
        if house == house_name:
            break
        current_rank += 1

    # Generate Pie Chart
    game_distribution = df.groupby("Game").sum()
    pie_data = game_distribution['Score']
    fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
    ax_pie.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
    ax_pie.axis('equal')
    buf_pie = BytesIO()
    fig_pie.savefig(buf_pie, format='png')
    buf_pie.seek(0)
    pie_chart_url = base64.b64encode(buf_pie.getvalue()).decode('utf-8')

    # Generate Bar Chart
    fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
    ax_bar.bar(df['Game'], df['Score'])
    ax_bar.set_title('Scores by Game')
    ax_bar.set_xlabel('Game')
    ax_bar.set_ylabel('Score')
    buf_bar = BytesIO()
    fig_bar.savefig(buf_bar, format='png')
    buf_bar.seek(0)
    bar_chart_url = base64.b64encode(buf_bar.getvalue()).decode('utf-8')

    # Generate Line Chart
    fig_line, ax_line = plt.subplots(figsize=(10, 6))
    ax_line.plot(df['Game'], df['Score'], marker='o', linestyle='-', color='b')
    ax_line.set_title('Score Trend by Game')
    ax_line.set_xlabel('Game')
    ax_line.set_ylabel('Score')
    buf_line = BytesIO()
    fig_line.savefig(buf_line, format='png')
    buf_line.seek(0)
    line_chart_url = base64.b64encode(buf_line.getvalue()).decode('utf-8')

    # Generate Scatter Plot
    fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))
    ax_scatter.scatter(df['Game'], df['Score'], color='r')
    ax_scatter.set_title('Game vs Score Performance')
    ax_scatter.set_xlabel('Game')
    ax_scatter.set_ylabel('Score')
    buf_scatter = BytesIO()
    fig_scatter.savefig(buf_scatter, format='png')
    buf_scatter.seek(0)
    scatter_chart_url = base64.b64encode(buf_scatter.getvalue()).decode('utf-8')

    return render(request, 'HouseStats.html', {
        'house_name': house_name,
        "house_color": house_color,
        "background_image": background_image,
        'pie_chart_url': 'data:image/png;base64,' + pie_chart_url,
        'bar_chart_url': 'data:image/png;base64,' + bar_chart_url,
        'line_chart_url': 'data:image/png;base64,' + line_chart_url,
        'scatter_chart_url': 'data:image/png;base64,' + scatter_chart_url,
        'total_points': total_points,
        'current_rank': current_rank,
        'games': data['Game'],
    })



from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def custom_logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


from .models import Match, MatchHouse  # Ensure these imports are present
def prepare_matches():
    """Helper function to format match data for the template."""
    matches = []
    for match in Match.objects.all():
        matches.append({
            'match_id': match.match_id,
            'game_name': match.game.game_name,
        })
    return matches

#Schedule a Match
from django.shortcuts import render
from django.db import IntegrityError
from .models import Match, Venue, MatchSchedule, Game

def schedule_match(request):
    if request.method == 'POST':
        match_id = request.POST.get('match')
        venue_id = request.POST.get('venue')
        schedule_date = request.POST.get('schedule_date')

        try:
            match = Match.objects.get(match_id=match_id)
            venue = Venue.objects.get(venue_id=venue_id)

            # Create a MatchSchedule entry
            MatchSchedule.objects.create(match=match, venue=venue, schedule_date=schedule_date)

            success_message = 'Match scheduled successfully!'
            return render(request, 'ScheduleMatches.html', {
                'matches': prepare_matches(),
                'venues': Venue.objects.all(),
                'success_message': success_message,
            })
        except Exception as e:
            error_message = str(e)

        return render(request, 'ScheduleMatches.html', {
            'matches': prepare_matches(),
            'venues': Venue.objects.all(),
            'error_message': error_message,
        })

    return render(request, 'ScheduleMatches.html', {
        'matches': prepare_matches(),
        'venues': Venue.objects.all(),
    })







#Edit Schedule
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Match, Venue, MatchSchedule

def edit_schedule(request, pk):
    schedule = get_object_or_404(MatchSchedule, pk=pk)
    if request.method == 'POST':
        match_id = request.POST.get('match')
        venue_id = request.POST.get('venue')
        schedule_date = request.POST.get('schedule_date')

        try:
            match = Match.objects.get(id=match_id)
            venue = Venue.objects.get(id=venue_id)

            # Update the schedule
            schedule.match = match
            schedule.venue = venue
            schedule.schedule_date = schedule_date
            schedule.save()

            return render(request, 'ScheduleMatches.html', {
                'matches': Match.objects.all(),
                'venues': Venue.objects.all(),
                'success_message': 'Match schedule updated successfully!',
            })
        except Exception as e:
            return render(request, 'ScheduleMatches.html', {
                'matches': Match.objects.all(),
                'venues': Venue.objects.all(),
                'error_message': f"Error: {str(e)}",
            })

    return render(request, 'ScheduleMatches.html', {
        'schedule': schedule,
        'matches': Match.objects.all(),
        'venues': Venue.objects.all(),
        'edit_mode': True,
    })

#ADD MATCH
from django.shortcuts import render, redirect
from .models import Match, Game, Venue, MatchHouse, House
from django.http import JsonResponse

def add_match(request):
    if request.method == "POST":
        game_name = request.POST.get('game')
        venue_id = request.POST.get('venue')
        house1_name = request.POST.get('house1')
        house2_name = request.POST.get('house2')
        scheduled_date = request.POST.get('scheduled_date')
        status = request.POST.get('status')

        # Validate fields
        if not all([game_name, venue_id, house1_name, house2_name, scheduled_date, status]):
            error_message = "All fields are required. Please fill in all fields."
            games = Game.objects.all()
            venues = Venue.objects.all()
            houses = House.objects.all()
            return render(request, 'AddMatch.html', {'error_message': error_message, 'games': games, 'venues': venues, 'houses': houses})

        try:
            game = Game.objects.get(game_name=game_name)
            venue = Venue.objects.get(venue_id=venue_id)
            house1 = House.objects.get(house_name=house1_name)
            house2 = House.objects.get(house_name=house2_name)

            # Create Match
            match = Match.objects.create(
                game=game,
                venue_id=venue.venue_id,
                scheduled_date=scheduled_date,
                status=status
            )

            # Link houses to the match
            MatchHouse.objects.create(match=match, house1=house1, house2=house2)

            success_message = "Match added successfully!"
            return render(request, 'AddMatch.html', {'success_message': success_message, 'games': Game.objects.all(), 'venues': Venue.objects.all(), 'houses': House.objects.all()})

        except Exception as e:
            print(f"Error creating match: {e}")
            error_message = "An error occurred while adding the match. Please try again."
            return render(request, 'AddMatch.html', {'error_message': error_message, 'games': Game.objects.all(), 'venues': Venue.objects.all(), 'houses': House.objects.all()})

    # Render form for GET request
    games = Game.objects.all()
    venues = Venue.objects.all()
    houses = House.objects.all()
    return render(request, 'AddMatch.html', {'games': games, 'venues': venues, 'houses': houses})


from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Match, MatchHouse

def view_matches(request):
    query = request.GET.get('q', '')

    try:
        # Fetch all matches and prefetch related data
        matches = Match.objects.all().prefetch_related('matchhouse_set', 'game', 'venue')

        # Filter matches based on the query
        if query:
            matches = matches.filter(
                game__game_name__icontains=query
            ) | matches.filter(
                matchhouse__house1__house_name__icontains=query
            ) | matches.filter(
                matchhouse__house2__house_name__icontains=query
            ) | matches.filter(
                venue__venue_name__icontains=query
            )

        # Prepare data for rendering
        match_data = []
        for match in matches:
            matchhouse = match.matchhouse_set.first()  # Assuming one-to-one relationship
            house1_name = matchhouse.house1.house_name if matchhouse and matchhouse.house1 else 'Unknown House 1'
            house2_name = matchhouse.house2.house_name if matchhouse and matchhouse.house2 else 'Unknown House 2'
            venue_name = match.venue.venue_name if match.venue else 'Unknown Venue'

            match_data.append({
                'match': match,
                'house1_name': house1_name,
                'house2_name': house2_name,
                'venue_name': venue_name,
            })

        # Check if the request is AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('partials/match_table.html', {'match_data': match_data})
            return JsonResponse({'html': html})

        return render(request, 'ViewMatches.html', {'match_data': match_data, 'query': query})

    except Exception as e:
        print(f"Error fetching matches: {e}")
        error_message = "An error occurred while fetching matches."
        return render(request, 'ViewMatches.html', {'error_message': error_message})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Match, Game, House, Venue

# Edit match view
def edit_match(request, match_id):
    match = get_object_or_404(Match, match_id=match_id)
    games = Game.objects.all()
    houses = House.objects.all()
    venues = Venue.objects.all()

    if request.method == "POST":
        game_name = request.POST.get('game')
        house1_name = request.POST.get('house1')
        house2_name = request.POST.get('house2')
        venue_name = request.POST.get('venue')
        scheduled_date = request.POST.get('scheduled_date')
        status = request.POST.get('status')

        try:
            game = get_object_or_404(Game, game_name=game_name)
            house1 = get_object_or_404(House, house_name=house1_name)
            house2 = get_object_or_404(House, house_name=house2_name)
            venue = get_object_or_404(Venue, venue_name=venue_name)

            match.game = game
            match.house1 = house1
            match.house2 = house2
            match.venue = venue
            match.scheduled_date = scheduled_date
            match.status = status
            match.save()

            success_message = "Match updated successfully!"
            return render(request, 'EditMatch.html', {
                'match': match, 'games': games, 'houses': houses, 
                'venues': venues, 'success_message': success_message
            })
        except Exception as e:
            error_message = "Error updating match. Please check your input."
            return render(request, 'EditMatch.html', {
                'match': match, 'games': games, 'houses': houses, 
                'venues': venues, 'error_message': error_message
            })

    return render(request, 'EditMatch.html', {
        'match': match, 'games': games, 'houses': houses, 'venues': venues
    })

# Delete match view
def delete_match(request, match_id):
    match = get_object_or_404(Match, match_id=match_id)

    if request.method == 'POST':
        match.delete()
        return redirect('view_matches')

    return render(request, 'DeleteMatch.html', {'match': match})

#ADD GAME
def add_game(request):
    if request.method == 'POST':
        game_name = request.POST.get('game_name')
        type = request.POST.get('type')
        description = request.POST.get('description')
       

        try:
            # Save the game
            Game.objects.create(
                game_name=game_name,
                type=type,
                description=description,
            )
            return render(request, 'AddGame.html', {
                'success_message': 'Game added successfully!',
            })
        except Exception as e:
            return render(request, 'AddGame.html', {
                'error_message': f'Error: {str(e)}',

            })

    return render(request, 'AddGame.html')


#View games
from django.shortcuts import render
from .models import Game

def view_game(request):
    games = Game.objects.all()  # Fetch all games
    return render(request, 'ViewGames.html', {'games': games})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Game
def edit_game(request, game_id):
    game = get_object_or_404(Game, game_id=game_id)

    if request.method == "POST":
        game_name = request.POST.get('game_name')
        game_type = request.POST.get('game_type')
        description = request.POST.get('description')

        try:
            game.game_name = game_name
            game.game_type = game_type
            game.description = description
            game.save()

            success_message = "Game updated successfully!"
            return render(request, 'EditGame.html', {
                'game': game,  
                'success_message': success_message
            })
        except Exception as e:
            error_message = "Error updating game. Please check your input."
            return render(request, 'EditGame.html', {
                'game': game, 
                'error_message': error_message
            })

    return render(request, 'EditGame.html', {
        'game': game,
    })


def delete_game(request, game_id):
    game = get_object_or_404(Game, game_id=game_id)
    if request.method == 'POST':
        game.delete()
        return redirect('view_game')  # Redirect to the list of games
    return render(request, 'DeleteGame.html', {'game': game})


#View Teams
from django.shortcuts import render
from .models import House, Player

def view_teams(request):
    houses = House.objects.all()  # Fetch all houses
    teams_data = []

    for house in houses:
        # Fetch all players associated with this house
        players = Player.objects.filter(house=house)

        teams_data.append({
            'house': house,
            'captain_name': house.captain_name,  # Use the captain_name from the House model
            'players': players,
        })

    return render(request, 'ViewTeams.html', {'teams_data': teams_data})


#Update Player Stats
from django.shortcuts import render, redirect
from .models import Player
from .forms import PlayerStatisticForm  # Import the form

def add_player_stats(request):
    if request.method == "POST":
        form = PlayerStatisticForm(request.POST)
        if form.is_valid():
            form.save()  # Save the player statistics to the database
            success_message = "Player statistics added successfully!"
            return render(request, 'UpdatePlayerStats.html', {'form': form, 'success_message': success_message})
        else:
            error_message = "There were errors in your form submission. Please check your data."
            return render(request, 'UpdatePlayerStats.html', {'form': form, 'error_message': error_message})
    else:
        form = PlayerStatisticForm()  # Display an empty form
        return render(request, 'UpdatePlayerStats.html', {'form': form})


from django.shortcuts import render

def elog_mvp(request):
    return render(request, 'elog_mvp.html')










