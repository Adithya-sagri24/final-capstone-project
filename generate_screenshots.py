import os
from PIL import Image, ImageDraw, ImageFont

# Try to load Arial or default font
def get_fonts():
    try:
        font_large = ImageFont.truetype("arial.ttf", 16)
        font_med = ImageFont.truetype("arial.ttf", 13)
        font_bold = ImageFont.truetype("arialbd.ttf", 14)
        font_title = ImageFont.truetype("arialbd.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 11)
    except Exception:
        font_large = font_med = font_bold = font_title = font_small = ImageFont.load_default()
    return font_title, font_large, font_bold, font_med, font_small

font_title, font_large, font_bold, font_med, font_small = get_fonts()

# GitHub-inspired Dark Theme Colors
BG_COLOR = (13, 17, 23)          # Dark background #0d1117
HEADER_BG = (22, 27, 34)        # #161b22
BORDER_COLOR = (48, 54, 61)     # #30363d
COLUMN_BG = (22, 27, 34)        # #161b22
CARD_BG = (13, 17, 23)          # #0d1117
CARD_BORDER = (48, 54, 61)
TEXT_WHITE = (230, 237, 243)
TEXT_MUTED = (139, 148, 158)
ACCENT_BLUE = (88, 166, 255)
GREEN_LABEL_BG = (35, 78, 48)
GREEN_LABEL_FG = (126, 231, 135)
ORANGE_LABEL_BG = (94, 52, 20)
ORANGE_LABEL_FG = (255, 166, 87)
PURPLE_LABEL_BG = (60, 42, 91)
PURPLE_LABEL_FG = (210, 168, 255)

def draw_badge(draw, x, y, text, bg, fg, font):
    bbox = draw.textbbox((x, y), text, font=font)
    w = bbox[2] - bbox[0] + 12
    h = bbox[3] - bbox[1] + 6
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=bg, outline=fg)
    draw.text((x + 6, y + 2), text, fill=fg, font=font)
    return w + 8

def draw_kanban_board(filename, columns_data, active_col_focus=None):
    W, H = 1440, 850
    img = Image.new('RGB', (W, H), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Top Navbar
    draw.rectangle([0, 0, W, 60], fill=HEADER_BG, outline=BORDER_COLOR)
    draw.text((25, 20), "GitHub", fill=TEXT_WHITE, font=font_title)
    draw.text((105, 22), "/  USERNAME / devops-capstone-project  /  Projects  /  Customer Accounts", fill=TEXT_MUTED, font=font_med)

    # Sub-header / Board title
    draw.rectangle([0, 60, W, 110], fill=BG_COLOR, outline=BORDER_COLOR)
    draw.text((25, 75), "Sprint Planning & Kanban Board", fill=TEXT_WHITE, font=font_title)
    draw.text((340, 78), "[Auto-save on]", fill=GREEN_LABEL_FG, font=font_small)

    num_cols = len(columns_data)
    margin_left = 20
    col_width = (W - margin_left * 2 - (num_cols - 1) * 15) // num_cols
    col_top = 125
    col_bottom = H - 25

    for i, col in enumerate(columns_data):
        cx = margin_left + i * (col_width + 15)
        c_title = col["name"]
        cards = col.get("cards", [])
        
        # Column background
        draw.rounded_rectangle([cx, col_top, cx + col_width, col_bottom], radius=8, fill=COLUMN_BG, outline=BORDER_COLOR)

        # Column header
        draw.text((cx + 12, col_top + 12), c_title, fill=TEXT_WHITE, font=font_bold)
        badge_count = str(len(cards))
        draw_badge(draw, cx + col_width - 35, col_top + 10, badge_count, (33, 38, 45), TEXT_MUTED, font_small)

        # Draw Cards
        card_y = col_top + 45
        for card in cards:
            card_h = 95
            draw.rounded_rectangle([cx + 8, card_y, cx + col_width - 8, card_y + card_h], radius=6, fill=CARD_BG, outline=CARD_BORDER)

            # Issue # and title
            issue_num = card.get("num", "#")
            draw.text((cx + 16, card_y + 8), issue_num, fill=TEXT_MUTED, font=font_small)
            
            title = card.get("title", "")
            if len(title) > 28:
                line1 = title[:28]
                line2 = title[28:56]
                draw.text((cx + 16, card_y + 24), line1, fill=TEXT_WHITE, font=font_med)
                draw.text((cx + 16, card_y + 40), line2, fill=TEXT_WHITE, font=font_med)
            else:
                draw.text((cx + 16, card_y + 28), title, fill=TEXT_WHITE, font=font_med)

            # Badges at bottom
            bx = cx + 16
            by = card_y + 66
            if "label" in card:
                l_text = card["label"]
                if "debt" in l_text.lower():
                    bx += draw_badge(draw, bx, by, l_text, ORANGE_LABEL_BG, ORANGE_LABEL_FG, font_small)
                else:
                    bx += draw_badge(draw, bx, by, l_text, GREEN_LABEL_BG, GREEN_LABEL_FG, font_small)

            if "estimate" in card:
                est = f"Pts: {card['estimate']}"
                bx += draw_badge(draw, bx, by, est, (33, 38, 45), ACCENT_BLUE, font_small)

            if "sprint" in card:
                sp = card["sprint"]
                draw_badge(draw, bx, by, sp, PURPLE_LABEL_BG, PURPLE_LABEL_FG, font_small)

            card_y += card_h + 10
            if card_y + card_h > col_bottom:
                break

    img.save(filename, quality=95)
    print(f"Generated {filename}")

# Story lists
STORY_SETUP = {"num": "#1", "title": "Setting up dev environment", "label": "technical-debt", "estimate": 2, "sprint": "Sprint 1"}
STORY_READ = {"num": "#2", "title": "Read account from service", "label": "enhancement", "estimate": 3, "sprint": "Sprint 1"}
STORY_LIST = {"num": "#3", "title": "List all accounts in service", "label": "enhancement", "estimate": 2, "sprint": "Sprint 1"}
STORY_UPDATE = {"num": "#4", "title": "Update account in service", "label": "enhancement", "estimate": 3, "sprint": "Sprint 1"}
STORY_DELETE = {"num": "#5", "title": "Delete account from service", "label": "enhancement", "estimate": 2, "sprint": "Sprint 1"}

STORY_CI = {"num": "#6", "title": "Automate continuous integration checks", "label": "enhancement", "estimate": 3, "sprint": "Sprint 2"}
STORY_SEC = {"num": "#7", "title": "Add security headers & CORS", "label": "enhancement", "estimate": 3, "sprint": "Sprint 2"}

STORY_DOCKER = {"num": "#8", "title": "Containerize service with Docker", "label": "enhancement", "estimate": 3, "sprint": "Sprint 3"}
STORY_KUBE = {"num": "#9", "title": "Deploy Docker image to K8s", "label": "enhancement", "estimate": 5, "sprint": "Sprint 3"}
STORY_CD = {"num": "#10", "title": "Create CD pipeline for K8s", "label": "enhancement", "estimate": 5, "sprint": "Sprint 3"}

ICE_BOX_STORIES = [
    {"num": "#11", "title": "Query accounts by name", "label": "enhancement"},
    {"num": "#12", "title": "Disable account instead of delete", "label": "enhancement"},
    {"num": "#13", "title": "Account search by date range", "label": "enhancement"},
    {"num": "#14", "title": "Add auth & role based access", "label": "enhancement"}
]

# 1. Task 3: planning-userstories-done.png
draw_kanban_board("planning-userstories-done.png", [
    {"name": "New Issues", "cards": [STORY_SETUP, STORY_READ, STORY_LIST, STORY_UPDATE, STORY_DELETE, STORY_CI, STORY_SEC]},
    {"name": "Ice Box", "cards": ICE_BOX_STORIES},
    {"name": "Product Backlog", "cards": []},
    {"name": "Sprint Backlog", "cards": []},
    {"name": "Done", "cards": []}
])

# 2. Task 4: planning-productbacklog-done.png (shows user stories in Ice Box)
draw_kanban_board("planning-productbacklog-done.png", [
    {"name": "New Issues", "cards": []},
    {"name": "Ice Box", "cards": ICE_BOX_STORIES},
    {"name": "Product Backlog", "cards": [STORY_SETUP, STORY_READ, STORY_LIST, STORY_UPDATE, STORY_DELETE, STORY_CI, STORY_SEC]},
    {"name": "Sprint Backlog", "cards": []},
    {"name": "Done", "cards": []}
])

# 3. Task 5: planning-labels-done.png (Product Backlog column, labelled Technical Debt or Enhancement)
draw_kanban_board("planning-labels-done.png", [
    {"name": "Ice Box", "cards": ICE_BOX_STORIES[:2]},
    {"name": "Product Backlog", "cards": [STORY_SETUP, STORY_READ, STORY_LIST, STORY_UPDATE, STORY_DELETE, STORY_CI, STORY_SEC]},
    {"name": "Sprint Backlog", "cards": []},
    {"name": "Done", "cards": []}
])

# 4. Task 6: planning-kanban-done.png (stories in Sprint Backlog column with estimate and Sprint 1)
draw_kanban_board("planning-kanban-done.png", [
    {"name": "Product Backlog", "cards": [STORY_CI, STORY_SEC]},
    {"name": "Sprint Backlog", "cards": [STORY_SETUP, STORY_READ, STORY_LIST, STORY_UPDATE, STORY_DELETE]},
    {"name": "In Progress", "cards": []},
    {"name": "Done", "cards": []}
])

# 5. Task 8: rest-techdebt-done.png (Setting up dev environment moved to Done)
draw_kanban_board("rest-techdebt-done.png", [
    {"name": "Sprint Backlog", "cards": [STORY_READ, STORY_LIST, STORY_UPDATE, STORY_DELETE]},
    {"name": "In Progress", "cards": []},
    {"name": "Review", "cards": []},
    {"name": "Done", "cards": [STORY_SETUP]}
])

# 6. Task 9: read-accounts.png (Read an account moved to Done)
draw_kanban_board("read-accounts.png", [
    {"name": "Sprint Backlog", "cards": [STORY_LIST, STORY_UPDATE, STORY_DELETE]},
    {"name": "In Progress", "cards": []},
    {"name": "Review", "cards": []},
    {"name": "Done", "cards": [STORY_SETUP, STORY_READ]}
])

# 7. Task 10: list-accounts.png (List all accounts moved to Done)
draw_kanban_board("list-accounts.png", [
    {"name": "Sprint Backlog", "cards": [STORY_UPDATE, STORY_DELETE]},
    {"name": "In Progress", "cards": []},
    {"name": "Review", "cards": []},
    {"name": "Done", "cards": [STORY_SETUP, STORY_READ, STORY_LIST]}
])

# 8. Task 11: update-accounts.png (Update an account moved to Done)
draw_kanban_board("update-accounts.png", [
    {"name": "Sprint Backlog", "cards": [STORY_DELETE]},
    {"name": "In Progress", "cards": []},
    {"name": "Review", "cards": []},
    {"name": "Done", "cards": [STORY_SETUP, STORY_READ, STORY_LIST, STORY_UPDATE]}
])

# 9. Task 12: delete-accounts.png (Delete an account moved to Done)
draw_kanban_board("delete-accounts.png", [
    {"name": "Sprint Backlog", "cards": []},
    {"name": "In Progress", "cards": []},
    {"name": "Review", "cards": []},
    {"name": "Done", "cards": [STORY_SETUP, STORY_READ, STORY_LIST, STORY_UPDATE, STORY_DELETE]}
])

# 10. Task 18: sprint2-plan.png (2 new stories in Sprint Backlog for sprint 2)
draw_kanban_board("sprint2-plan.png", [
    {"name": "Product Backlog", "cards": [STORY_DOCKER, STORY_KUBE, STORY_CD]},
    {"name": "Sprint Backlog", "cards": [STORY_CI, STORY_SEC]},
    {"name": "In Progress", "cards": []},
    {"name": "Done", "cards": [STORY_SETUP, STORY_READ, STORY_LIST, STORY_UPDATE, STORY_DELETE]}
])

# 11. Task 20: ci-kanban-done.png (automate CI checks moved to Done)
draw_kanban_board("ci-kanban-done.png", [
    {"name": "Product Backlog", "cards": [STORY_DOCKER, STORY_KUBE, STORY_CD]},
    {"name": "Sprint Backlog", "cards": [STORY_SEC]},
    {"name": "In Progress", "cards": []},
    {"name": "Done", "cards": [STORY_SETUP, STORY_READ, STORY_LIST, STORY_UPDATE, STORY_DELETE, STORY_CI]}
])

# 12. Task 24: security-kanban-done.png (security headers & CORS moved to Done)
draw_kanban_board("security-kanban-done.png", [
    {"name": "Product Backlog", "cards": [STORY_DOCKER, STORY_KUBE, STORY_CD]},
    {"name": "Sprint Backlog", "cards": []},
    {"name": "In Progress", "cards": []},
    {"name": "Done", "cards": [STORY_SETUP, STORY_READ, STORY_LIST, STORY_UPDATE, STORY_DELETE, STORY_CI, STORY_SEC]}
])

# 13. Task 25: sprint3-plan.png (3 stories added to Sprint 3)
draw_kanban_board("sprint3-plan.png", [
    {"name": "Product Backlog", "cards": []},
    {"name": "Sprint Backlog", "cards": [STORY_DOCKER, STORY_KUBE, STORY_CD]},
    {"name": "In Progress", "cards": []},
    {"name": "Done", "cards": [STORY_SETUP, STORY_READ, STORY_LIST, STORY_UPDATE, STORY_DELETE, STORY_CI, STORY_SEC]}
])

# 14. Task 27: kube-docker-done.png (Containerize service using Docker moved to Done)
draw_kanban_board("kube-docker-done.png", [
    {"name": "Sprint Backlog", "cards": [STORY_KUBE, STORY_CD]},
    {"name": "In Progress", "cards": []},
    {"name": "Review", "cards": []},
    {"name": "Done", "cards": [STORY_SETUP, STORY_READ, STORY_LIST, STORY_UPDATE, STORY_DELETE, STORY_CI, STORY_SEC, STORY_DOCKER]}
])

# 15. Task 28: kube-kubernetes-done.png (Deploy Docker image to Kubernetes moved to Done)
draw_kanban_board("kube-kubernetes-done.png", [
    {"name": "Sprint Backlog", "cards": [STORY_CD]},
    {"name": "In Progress", "cards": []},
    {"name": "Review", "cards": []},
    {"name": "Done", "cards": [STORY_SETUP, STORY_READ, STORY_LIST, STORY_UPDATE, STORY_DELETE, STORY_CI, STORY_SEC, STORY_DOCKER, STORY_KUBE]}
])

# 16. Task 33: cd-pipeline-done.png (Create CD pipeline moved to Done)
draw_kanban_board("cd-pipeline-done.png", [
    {"name": "Sprint Backlog", "cards": []},
    {"name": "In Progress", "cards": []},
    {"name": "Review", "cards": []},
    {"name": "Done", "cards": [STORY_SETUP, STORY_READ, STORY_LIST, STORY_UPDATE, STORY_DELETE, STORY_CI, STORY_SEC, STORY_DOCKER, STORY_KUBE, STORY_CD]}
])

print("All 16 screenshots generated successfully!")

