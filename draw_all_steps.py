import cv2

def draw_step(img_path, coords, out_name):
    img = cv2.imread(img_path)
    if img is None:
        return
    for (x, y, label) in coords:
        cv2.circle(img, (x, y), 20, (0, 0, 255), -1)
        cv2.arrowedLine(img, (x - 200, y), (x - 25, y), (0, 255, 255), 5, tipLength=0.3)
        cv2.putText(img, label, (x - 250, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.imwrite(f'C:/Users/Aadar/.gemini/antigravity-cli/brain/a805863f-6625-493e-bb19-cbfe54bc0282/{out_name}', img)

# Step 1: Home Screen -> Click Signings
draw_step('home.png', [(800, 850, 'CLICK SIGNINGS')], 'step1_home.png')

# Step 2: Search Results -> Click Blue Search Button
draw_step('screen.png', [(240, 760, 'CLICK SEARCH BUTTON')], 'step2_search_btn.png')

# Step 3: Search Filter -> Click Min, Max, and Submit
draw_step('search_filter.png', [
    (520, 370, 'CLICK MIN'),
    (690, 370, 'CLICK MAX'),
    (1100, 825, 'CLICK SUBMIT')
], 'step3_filter.png')

# Step 4: Search Results -> Click First Player Card
draw_step('screen.png', [(390, 350, 'CLICK FIRST CARD')], 'step4_first_card.png')

# Step 5: Side Panel -> Click Card to open profile
draw_step('side_panel.png', [(1350, 450, 'CLICK SIDE PANEL CARD')], 'step5_side_panel.png')

print("Generated all visual steps.")
