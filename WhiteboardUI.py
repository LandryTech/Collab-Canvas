import pygame
import sys
import math
import socket
from point import Point
from networkClient import NetworkClient

class WhiteboardUI:
    def __init__(self, width=1920, height=1080, server_ip="127.0.0.1", server_port=5002):
        pygame.init()
        
        # Set up display
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Collaborative Whiteboard")
        
        # Initialize network client
        try:
            self.client = NetworkClient(server_ip, server_port)
            # Set socket to non-blocking mode to prevent freezing
            self.client.client_socket.setblocking(False)
            print(f"Connected to server at {server_ip}:{server_port}")
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            sys.exit(1)
        
        # Drawing state
        self.points = []
        self.new_points_this_frame = []  # Track points drawn this frame
        self.current_color = Point.BLACK
        self.current_radius = 5
        self.is_drawing = False
        self.is_erasing = False
        self.last_pos = None  # Track last position for interpolation
        
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
        
        # Eraser button
        eraser_x = size_start_x + len(self.brush_sizes) * (button_size + spacing) + 40
        self.eraser_button = pygame.Rect(eraser_x, start_y, 100, button_size)
        
        # Clear button
        clear_x = eraser_x + 110
        self.clear_button = pygame.Rect(clear_x, start_y, 100, button_size)
    
    def draw_toolbar(self):
        """Draw the toolbar with color palette, brush sizes, and controls"""
        # Draw toolbar background
        pygame.draw.rect(self.screen, self.toolbar_color, (0, 0, self.width, self.toolbar_height))
        
        # Draw color palette
        for button in self.color_buttons:
            # Highlight selected color (only if not erasing)
            if button['color'] == self.current_color and not self.is_erasing:
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
        
        # Draw eraser button
        if self.is_erasing:
            pygame.draw.rect(self.screen, (100, 255, 100), self.eraser_button)
        else:
            pygame.draw.rect(self.screen, (200, 200, 200), self.eraser_button)
        pygame.draw.rect(self.screen, (0, 0, 0), self.eraser_button, 2)
        
        # Draw text on eraser button
        font = pygame.font.Font(None, 24)
        text = font.render("Eraser", True, (0, 0, 0))
        text_rect = text.get_rect(center=self.eraser_button.center)
        self.screen.blit(text, text_rect)
        
        # Draw clear button
        pygame.draw.rect(self.screen, (255, 100, 100), self.clear_button)
        pygame.draw.rect(self.screen, (0, 0, 0), self.clear_button, 2)
        
        # Draw text on clear button
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
                self.is_erasing = False
                return
        
        # Check brush size clicks
        for button in self.size_buttons:
            if button['rect'].collidepoint(pos):
                self.current_radius = button['size']
                return
        
        # Check eraser button
        if self.eraser_button.collidepoint(pos):
            self.is_erasing = not self.is_erasing
            return
        
        # Check clear button
        if self.clear_button.collidepoint(pos):
            self.points.clear()
            return
    
    def interpolate_points(self, start_pos, end_pos):
        """Generate interpolated points between two positions for smooth lines"""
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Calculate distance between points
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        # Calculate number of interpolation steps based on distance and radius
        # This ensures smooth lines without gaps
        steps = max(int(distance / (self.current_radius * 0.3)), 1)
        
        interpolated = []
        for i in range(steps + 1):
            t = i / steps if steps > 0 else 0
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            interpolated.append((x, y))
        
        return interpolated
    
    def add_point(self, pos):
        """Add a new drawing point with interpolation"""
        x, y = pos
        
        # Only draw on canvas area (below toolbar)
        if y > self.canvas_y_offset:
            # If we have a last position, interpolate between them
            if self.last_pos is not None:
                interpolated_positions = self.interpolate_points(self.last_pos, pos)
                for interp_pos in interpolated_positions:
                    point = Point(interp_pos[0], interp_pos[1], self.width, self.height, 
                                self.current_radius, self.current_color)
                    self.points.append(point)
                    self.new_points_this_frame.append(point)
            else:
                # First point, just add it
                point = Point(x, y, self.width, self.height, self.current_radius, self.current_color)
                self.points.append(point)
                self.new_points_this_frame.append(point)
            
            self.last_pos = pos

    def erase_point(self, pos):
        """Erase points near the cursor position"""
        x, y = pos
        
        # Only erase on canvas area (below toolbar)
        if y > self.canvas_y_offset:
            # Eraser radius is larger than current brush size for easier erasing
            erase_radius = self.current_radius * 2
            
            # Find and remove points within eraser radius
            points_to_remove = []
            for point in self.points:
                point_x = point.getPosX()
                point_y = point.getPosY()
                
                # Calculate distance from cursor to point
                distance = math.sqrt((x - point_x)**2 + (y - point_y)**2)
                
                # If point is within eraser radius, mark for removal
                if distance <= erase_radius + point.getRadScaled():
                    points_to_remove.append(point)
            
            # Remove all marked points
            for point in points_to_remove:
                self.points.remove(point)
    
    def send_points(self):
        """Send new points drawn this frame to the server"""
        try:
            if self.new_points_this_frame:
                # Create list of string representations (decode the bytes)
                msg_list = [point.toStringEncode().decode() for point in self.new_points_this_frame]
                self.client.send(msg_list)
            else:
                # Send empty message if no points drawn
                self.client.send("NONE")
        except Exception as e:
            print(f"Error sending points: {e}")
    
    def receive_points(self):
        """Receive and add points from other clients (non-blocking)"""
        try:
            # Try to receive data (won't block since socket is non-blocking)
            data = self.client.client_socket.recv(1024)
            
            if data:
                decoded = data.decode().split('<')
                
                if decoded and decoded[0] != "NONE":
                    # Process each received point message
                    for msg in decoded:
                        if msg and msg != "NONE" and msg != "":
                            # Try to initialize point from received message
                            msg_bytes = msg.encode()
                            point = Point.initialization(msg_bytes, self.width, self.height)
                            
                            # Add point if initialization was successful
                            if point is not None:
                                self.points.append(point)
        except socket.error as e:
            # socket.error is raised when no data is available (non-blocking)
            # This is expected and normal, so we just pass
            pass
        except Exception as e:
            print(f"Error receiving points: {e}")

    def run(self):
        """Main application loop"""
        running = True
        
        while running:
            # Clear new points from previous frame
            self.new_points_this_frame = []
            
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
                            if self.is_erasing:
                                self.erase_point(mouse_pos)
                            else:
                                self.add_point(mouse_pos)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.is_drawing = False
                        self.last_pos = None  # Reset last position when done drawing
                
                elif event.type == pygame.MOUSEMOTION:
                    if self.is_drawing:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.is_erasing:
                            self.erase_point(mouse_pos)
                        else:
                            self.add_point(mouse_pos)
            
            # Network operations - send and receive every frame
            self.send_points()
            self.receive_points()
            
            # Clear screen
            self.screen.fill(self.bg_color)
            
            # Draw everything
            self.draw_canvas()
            self.draw_toolbar()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        # Clean up
        self.client.stop()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Change the IP address to match your server
    app = WhiteboardUI(server_ip="127.0.0.1", server_port=5002)
    app.run()