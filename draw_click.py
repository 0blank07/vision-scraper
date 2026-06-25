import cv2

# Load the side panel screenshot
img = cv2.imread('side_panel.png')

# The coordinate I am clicking
x, y = 1350, 450

# Draw a red circle and a pointer arrow to show exactly where the click happens
cv2.circle(img, (x, y), 20, (0, 0, 255), -1) # Red dot at exact click location
cv2.arrowedLine(img, (x - 200, y), (x - 25, y), (0, 255, 255), 5, tipLength=0.3) # Yellow arrow pointing to it
cv2.putText(img, 'CLICK (1350, 450)', (x - 250, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

# Save the visualization
cv2.imwrite('C:/Users/Aadar/.gemini/antigravity-cli/brain/a805863f-6625-493e-bb19-cbfe54bc0282/click_target.png', img)
cv2.imwrite('C:/Users/Aadar/.gemini/antigravity-cli/brain/a805863f-6625-493e-bb19-cbfe54bc0282/debug_proof.png', cv2.imread('debug2.png'))
