# LOG (League of Glory) Management System

**National University of Computer and Emerging Sciences, Karachi Campus**  
**Spring 2025**  
**Database Systems Course**  

---

## 1. Overview
The **League of Glory (LOG) Management System (LMS)** is a Django-based web application designed to streamline sports event management. It automates player registration, match scheduling, game assignments, real-time data recording, and ranking updates. With role-based access, it serves administrators, teaching assistants, players, and spectators, reducing manual paperwork and enhancing efficiency.

**Target Audience:**
- **Administrators:** Monitor tournaments, rankings, and results.
- **Teaching Assistants:** Manage registrations and schedules.
- **Players:** View match schedules and stats.
- **Spectators:** Access leaderboards and highlights.

![Overview](media/overview.png)

---

## 2. Key Features
- **House Maintenance:** Manage teams, assign captains, and link to venues.
- **Player Management:** Register, edit, or delete player details (e.g., name, contact, house).
- **Game Management:** Organize games with details like name, type, and description.
- **Match Scheduling:** Automate conflict-free schedules, editable via the interface.
- **Statistics Tracking:** Record player metrics (goals, assists, fouls, cards) in real-time.
- **Ranking System:** Dynamic leaderboards based on match outcomes.
- **Graphs & Visualizations:** Display trends and performance metrics.
- **ELOG & MVPs:** Showcase top performers via posters and carousels.

![Features](media/features.png)

---

## 3. Key Terms
- **House:** Competing team.
- **Player:** Registered participant.
- **Game:** Sport or event.
- **Match:** Scheduled competition.
- **Ranking System:** Dynamic leaderboard.
- **ELOG Poster:** Digital MVP display.

---

## 4. Usage Instructions

### 4.1 Logging In
1. Navigate to the LMS login page.
2. Enter username and password.
3. Click **Login** to access the dashboard.

![Login](media/login.png)

### 4.2 Viewing Matches
1. Go to **Matches** > **View Matches**.
2. Use the search bar to filter by team, date, or location.
3. Add, edit, or delete matches as needed.

### 4.3 Scheduling Matches
1. Go to **Matches** > **Schedule Matches**.
2. Enter match title, houses, date, time, and venue.
3. Click **Schedule Match**.

### 4.4 Managing Players
1. Go to **Players** > **Add Player**.
2. Input player details (name, contact, house, game).
3. Click **Add Player** or use **View Players** to edit/delete.

![Player Management](media/player_management.png)

### 4.5 Updating Statistics
1. Go to **Rankings** > **Update Player Stats**.
2. Select player and enter stats (goals, assists, fouls, cards).
3. Click **Add Statistics**.

### 4.6 Viewing House Statistics
1. Go to **Stats** > Select house (e.g., Ares, Zeus).
2. View performance metrics.

![Statistics](media/statistics.png)

### 4.7 ELOG & MVPs
- **ELOG Poster:** Displays event details with hover-enlargement.
- **MVPs Carousel:** Showcases top players with team-themed frames.

![ELOG](media/elog.png)

---

## 5. Maintenance & Troubleshooting

### Maintenance
- Update system and security patches regularly.
- Optimize images and clear cache for performance.
- Back up player stats and validate data integrity.

### Troubleshooting
- **Slow loading?** Clear cache or check internet stability.
- **Can’t update stats?** Verify permissions and refresh.
- **ELOG carousel issues?** Enable JavaScript and check console (F12).
- **Session expired?** Re-login and enable cookies.

---

## 6. Installation
1. Clone the repository: `git clone https://github.com/username/log-management-system.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up the database: `python manage.py migrate`
4. Run the server: `python manage.py runserver`

---

## 7. Contributing
Contributions are welcome! Please fork the repository, create a branch, and submit a pull request with your changes.

---

## 8. License
This project is licensed under the MIT License.
