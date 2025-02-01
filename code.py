import adafruit_display_text.label as label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import time
import requests

MOCK_API_LIVE_URL = "https://livescore-api.com/api-client/matches/live.json?&key=zlHXiXecsqeiZ04Y&secret=RyVM0eUNgSHayrI7Np55nkhPLw8KxdIo"
LIVE_API_LIVE_URL = "https://livescore-api.com/api-client/matches/live.json?&key=zlHXiXecsqeiZ04Y&secret=RyVM0eUNgSHayrI7Np55nkhPLw8KxdIo&category_id=2"
API_LIVE_URL = MOCK_API_LIVE_URL
# UNCOMMENT FOR FUNCTIONALITY
API_LIVE_URL = LIVE_API_LIVE_URL
API_STANDINGS_URL = "https://livescore-api.com/api-client/leagues/table.json?competition_id=2&key=zlHXiXecsqeiZ04Y&secret=RyVM0eUNgSHayrI7Np55nkhPLw8KxdIo"

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

bmp = displayio.Bitmap(display.width, display.height, 2)

team_id_to_info = {
    "7": {"code": "LIV", "color": "#C8102E"},  # Liverpool
    "18": {"code": "ARS", "color": "#EF0107"},  # Arsenal
    "487": {"code": "NFO", "color": "#DD0000"},  # Nottingham Forest
    "12": {"code": "MCI", "color": "#6CABDD"},  # Manchester City
    "9": {"code": "NEW", "color": "#bbbdbf"},  # Newcastle United
    "17": {"code": "CHE", "color": "#034694"},  # Chelsea
    "1": {"code": "BOU", "color": "#DA291C"},  # AFC Bournemouth
    "495": {"code": "AVL", "color": "#670E36"},  # Aston Villa
    "2": {"code": "BHA", "color": "#0057B8"},  # Brighton & Hove Albion
    "502": {"code": "FUL", "color": "#CC0000"},  # Fulham
    "489": {"code": "BRE", "color": "#D20000"},  # Brentford
    "19": {"code": "MUN", "color": "#DA291C"},  # Manchester United
    "3": {"code": "CRY", "color": "1B458F"},  # Crystal Palace
    "14": {"code": "WHU", "color": "#7A263A"},  # West Ham United
    "15": {"code": "TOT", "color": "#C4CED4"},  # Tottenham Hotspur
    "20": {"code": "EVE", "color": "#003399"},  # Everton
    "6": {"code": "LEI", "color": "#003090"},  # Leicester City
    "497": {"code": "WOL", "color": "#FDB913"},  # Wolverhampton Wanderers
    "491": {"code": "IPS", "color": "#253a97"},  # Ipswich Town
    "4": {"code": "SOU", "color": "#D71920"}  # Southampton
}

def fetch_live_matches():
    try:
        response = requests.get(API_LIVE_URL)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                matches = []
                for match in data["data"]["match"]:
                    match_info = {
                        "id": match["id"],
                        "home_team": match["home"]["name"][:3].upper(),  # 3-letter code
                        "away_team": match["away"]["name"][:3].upper(),  # 3-letter code
                        "score": match["scores"]["score"],
                        "time": match["time"],
                        "status": match["status"]
                    }
                    matches.append(match_info)
                    print (matches)
                return matches
    except Exception as e:
        print(f"Error fetching data: {e}")
    return []

def display_match(match):
    """Display match details on LED matrix."""
    g = displayio.Group()

    home_team = match["home_team"]
    away_team = match["away_team"]
    score = match["score"]
    match_time = match["time"]

    team1_label = label.Label(
        font=terminalio.FONT,
        color=0xFFFFFF,
        scale=1,
        anchor_point=(1, 0.5),
        anchored_position=(28, 5),
        text=home_team,
    )

    team2_label = label.Label(
        font=terminalio.FONT,
        color=0xFF0000,
        scale=1,
        anchor_point=(0, 0.5),
        anchored_position=(36, 5),
        text=away_team,
    )

    score_label = label.Label(
        font=terminalio.FONT,
        color=0xFFFFFF,
        scale=1,
        anchor_point=(0.5, 0.5),
        anchored_position=(32, 15),
        text=score,
    )

    time_label = label.Label(
        font=terminalio.FONT,
        color=0xFFFF00,
        scale=1,
        anchor_point=(0.5, 0.5),
        anchored_position=(37, 25),
        text=f"{match_time}'",
    )

    g.append(team1_label)
    g.append(team2_label)
    g.append(score_label)
    g.append(time_label)

    display.root_group = g
    display.refresh(minimum_frames_per_second=1)


def fetch_standings():
    response = requests.get(API_STANDINGS_URL)
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and "table" in data["data"]:
            return data["data"]["table"]
    return None

def draw_border():
    for i in range(display.width):
        bmp[i, 0] = 1
        bmp[i, display.height - 1] = 1
    for i in range(display.height):
        bmp[0, i] = 1
        bmp[display.width - 1, i] = 1

def draw_football1(group, x, y):
    bitmap1 = displayio.Bitmap(display.width, display.height, 2)
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xFFFFFF
    
    football_pixels = [
        (x, y), (x + 1, y),
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 2, y + 1),
        (x - 1, y + 2), (x, y + 2), (x + 2, y + 2),
        (x, y + 3), (x + 1, y + 3)
    ]
    
    for (dx, dy) in football_pixels:
        if 0 <= dx < display.width and 0 <= dy < display.height:
            bitmap1[dx, dy] = 1
    
    grid1 = displayio.TileGrid(bitmap1, pixel_shader=palette)
    group.append(grid1)
    

def draw_football2(group, x, y):
    bitmap2 = displayio.Bitmap(display.width, display.height, 2)
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xFFFFFF
    
    football_pixels = [
        (x, y), (x + 1, y),
        (x - 1, y + 1), (x, y + 1), (x + 2, y + 1),
        (x - 1, y + 2), (x, y+2), (x + 1, y + 2), (x + 2, y + 2),
        (x, y + 3), (x + 1, y + 3)
    ]
    
    for (dx, dy) in football_pixels:
        if 0 <= dx < display.width and 0 <= dy < display.height:
            bitmap2[dx, dy] = 1
    
    grid2 = displayio.TileGrid(bitmap2, pixel_shader=palette)
    group.append(grid2)

def display_standings(standings, index):
    print(standings[index])
    
    display.root_group = None
    g = displayio.Group()

    football1_group = displayio.Group()
    football2_group = displayio.Group()
    
    draw_football1(football1_group, 10, 3)
    draw_football2(football2_group, 55, 3)
    
    g.append(football1_group)
    g.append(football2_group)

    display.root_group = g

    draw_border()
    
    header_label = label.Label(terminalio.FONT, text="STATS", color=0xFFFFFF)
    header_label.anchor_point = (0.5, 0.5)
    header_label.anchored_position = (display.width // 2, 5)
   
    g.append(header_label)
    
    if index < len(standings):
        team = standings[index]
        team_id = str(team['team_id'])

        team_info = team_id_to_info.get(team_id, {"code": team['name'][:3].upper(), "color": "#FFFFFF"})
        team_code = team_info["code"]
        team_color = int(team_info["color"].lstrip("#"), 16)

        rank_label = label.Label(
            font=terminalio.FONT, color=0xFFFFFF, scale=1,
            anchor_point=(0, 0.5), anchored_position=(3, 16),
            text=str(team['rank'])
        )
        g.append(rank_label)

        team_label = label.Label(
            font=terminalio.FONT, color=team_color, scale=1,
            anchor_point=(0, 0.5), anchored_position=(20, 16),
            text=team_code
        )
        g.append(team_label)

        points_label = label.Label(
            font=terminalio.FONT, color=0xFFFFFF, scale=1,
            anchor_point=(0, 0.5), anchored_position=(48, 16),
            text=str(team['points'])
        )
        g.append(points_label)

        wins = str(team['won'])
        draws = str(team['drawn'])
        losses = str(team['lost'])
        goal_diff = int(team['goal_diff'])

        color = 0xFF0000 if goal_diff < 0 else 0x00FF00

        match_info_text = f"{wins}:{draws}:{losses}|{goal_diff}"

        match_info_label = label.Label(
            font=terminalio.FONT, color=color, scale=1,
            anchor_point=(0, 0.5), anchored_position=(5, 25),
            text=match_info_text
        )

        g.append(match_info_label)

    display.root_group = g
    display.refresh(minimum_frames_per_second=1)

def draw_empty_field():
    group = displayio.Group()
    bitmap = displayio.Bitmap(display.width, display.height, 2)
    palette = displayio.Palette(2)
    palette[0] = 0x3f9b0b
    palette[1] = 0xFFFFFF
    
    for x in range(display.width):
        for y in range(display.height):
            bitmap[x, y] = 0
    
    center_x = display.width // 2
    center_y = display.height // 2

    x = center_x
    y = center_y

    bitmap[center_x, center_y] = 1

    football_pixels = [
        (x, y-1), (x + 1, y-1),
        (x - 1, y), (x, y), (x+1, y), (x + 2, y),
        (x - 1, y + 1), (x, y+1), (x + 1, y + 1), (x + 2, y + 1),
        (x, y + 2), (x + 1, y + 2)
    ]

    for (dx, dy) in football_pixels:
        if 0 <= dx < display.width and 0 <= dy < display.height:
            bitmap[dx, dy] = 1
    
    for y in range(display.height):
        bitmap[center_x, y] = 1

    for x in range(display.width):
        bitmap[x, 0] = 1
        bitmap[x, display.height -1] = 1

    for y in range(display.height):
        bitmap[0, y] = 1
        bitmap[display.width-1, y] = 1

    for x in range(5):
        bitmap[x,13] = 1
        bitmap[x+display.width-5, 13] = 1
        bitmap[x,21] = 1
        bitmap[x+display.width-5, 21] = 1

    for y in range(9):
        bitmap[5,y+13] = 1
        bitmap[display.width-5, y+13] = 1
    
    grid = displayio.TileGrid(bitmap, pixel_shader=palette)
    group.append(grid)
    
    display.root_group = group
    display.refresh(minimum_frames_per_second=0)
    time.sleep(3600)

def main_loop():
    while True:
        live_matches = fetch_live_matches()
        # UNCOMMENT TO SEE FUNCTIONALITY
        # live_matches = False
        if live_matches:
            for match in live_matches:
                display_match(match)
                time.sleep(3)
        else:
            print("No live matches")
            standings = fetch_standings()
            # UNCOMMENT TO SEE FUNCTIONALITY
            # standings = False
            if standings:
                for i in range(0, len(standings)):
                    display_standings(standings, i)
                    time.sleep(10)
            draw_empty_field()

main_loop()
