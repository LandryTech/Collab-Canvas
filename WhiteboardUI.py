import pygame
import sys
from point import Point

class WhiteboardUI:
    def __init__(self, width=1920, height=1080):
        pygame.init()
        
        # Set up display
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Collaborative Whiteboard")
        
        # Drawing state
        self.points = []
        self.current_color = Point.BLACK
        self.current_radius = 5
        self.is_drawing = False
        
        # UI colors
        self.bg_color = (255, 255, 255)
        self.toolbar_color = (240, 240, 240)
        self.button_hover_color = (220, 220, 220)
        
        # Toolbar setup
        self.toolbar_height = 80
        self.canvas_y_offset = self.toolbar_height
        
        # Color palette
        self.color_palette = [
            Point.BLACK, Point.RED, Point.ORANGE, Point.YELLOW,
            Point.GREEN, Point.BLUE, Point.PURPLE, Point.PINK,
            Point.BROWN, Point.WHITE, Point.GRAY
        ]
        
        # Brush sizes
        self.brush_sizes = [2, 5, 10, 15, 20]
        
        # Setup UI elements
        self.setup_ui_elements()
        
        # Clock for frame rate
        self.clock = pygame.time.Clock()
    
    def setup_ui_elements(self):
        """Initialize UI element positions"""
        # Color buttons
        self.color_buttons = []
        button_size = 40
        spacing = 10
        start_x = 20
        start_y = 20
        
        for i, color in enumerate(self.color_palette):
            rect = pygame.Rect(start_x + i * (button_size + spacing), start_y, button_size, button_size)
            self.color_buttons.append({'rect': rect, 'color': color})
        
        # Brush size buttons
        self.size_buttons = []
        size_start_x = start_x + len(self.color_palette) * (button_size + spacing) + 40
        
        for i, size in enumerate(self.brush_sizes):
            rect = pygame.Rect(size_start_x + i * (button_size + spacing), start_y, button_size, button_size)
            self.size_buttons.append({'rect': rect, 'size': size})
        
        # Clear button
        clear_x = size_start_x + len(self.brush_sizes) * (button_size + spacing) + 40
        self.clear_button = pygame.Rect(clear_x, start_y, 100, button_size)
    
    def draw_toolbar(self):
        """Draw the toolbar with color palette, brush sizes, and controls"""
        # Draw toolbar background
        pygame.draw.rect(self.screen, self.toolbar_color, (0, 0, self.width, self.toolbar_height))
        
        # Draw color palette
        for button in self.color_buttons:
            # Highlight selected color
            if button['color'] == self.current_color:
                pygame.draw.rect(self.screen, (100, 100, 255), button['rect'].inflate(6, 6), 3)
            
            pygame.draw.rect(self.screen, button['color'], button['rect'])
            pygame.draw.rect(self.screen, (0, 0, 0), button['rect'], 2)
        
        # Draw brush size buttons
        for button in self.size_buttons:
            # Highlight selected size
            if button['size'] == self.current_radius:
                pygame.draw.rect(self.screen, (100, 100, 255), button['rect'].inflate(6, 6), 3)
            
            pygame.draw.rect(self.screen, (200, 200, 200), button['rect'])
            pygame.draw.rect(self.screen, (0, 0, 0), button['rect'], 2)
            
            # Draw size indicator circle
            center = button['rect'].center
            display_radius = min(button['size'], 15)
            pygame.draw.circle(self.screen, (0, 0, 0), center, display_radius)
        
        # Draw clear button
        pygame.draw.rect(self.screen, (255, 100, 100), self.clear_button)
        pygame.draw.rect(self.screen, (0, 0, 0), self.clear_button, 2)
        
        # Draw text on clear button
        font = pygame.font.Font(None, 24)
        text = font.render("Clear", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.clear_button.center)
        self.screen.blit(text, text_rect)
    
    def draw_canvas(self):
        """Draw all points on the canvas"""
        for point in self.points:
            # Update point dimensions if window size changed
            point.setWidth(self.width)
            point.setHeight(self.height)
            
            pygame.draw.circle(
                self.screen,
                point.getColor(),
                (int(point.getPosX()), int(point.getPosY())),
                int(point.getRadScaled())
            )
    
    def handle_click(self, pos):
        """Handle mouse clicks on UI elements"""
        x, y = pos
        
        # Check color palette clicks
        for button in self.color_buttons:
            if button['rect'].collidepoint(pos):
                self.current_color = button['color']
                return
        
        # Check brush size clicks
        for button in self.size_buttons:
            if button['rect'].collidepoint(pos):
                self.current_radius = button['size']
                return
        
        # Check clear button
        if self.clear_button.collidepoint(pos):
            self.points.clear()
            return
    
    def add_point(self, pos):
        """Add a new drawing point"""
        x, y = pos
        
        # Only draw on canvas area (below toolbar)
        if y > self.canvas_y_offset:
            point = Point(x, y, self.width, self.height, self.current_radius, self.current_color)
            self.points.append(point)
    
    def run(self):
        """Main application loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        mouse_pos = pygame.mouse.get_pos()
                        
                        # Check if clicking on toolbar
                        if mouse_pos[1] < self.toolbar_height:
                            self.handle_click(mouse_pos)
                        else:
                            self.is_drawing = True
                            self.add_point(mouse_pos)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.is_drawing = False
                
                elif event.type == pygame.MOUSEMOTION:
                    if self.is_drawing:
                        self.add_point(pygame.mouse.get_pos())
            
            # Clear screen
            self.screen.fill(self.bg_color)
            
            # Draw everything
            self.draw_canvas()
            self.draw_toolbar()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = WhiteboardUI()
    app.run()