import math

import pygame


RAINBOW_COLORS = [
    (255, 0, 0),
    (255, 127, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 255, 255),
    (0, 0, 255),
    (139, 0, 255),
]


class PlayerRenderer:
    def draw(self, screen, player, context):
        self._draw_rainbow(screen, player.trail)
        self._draw_particles(screen, player.particles)

        frame = player.animation.get_frame()
        if context.is_flipped:
            frame = pygame.transform.flip(frame, False, True)
        screen.blit(frame, (player.x, player.y))

    def _draw_rainbow(self, screen, trail):
        if len(trail) < 2:
            return

        points = [p["pos"] for p in trail]
        smooth = []
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            smooth.append((x1, y1))
            smooth.append((x1 + (x2 - x1) * 0.35, y1 + (y2 - y1) * 0.35))
            smooth.append((x1 + (x2 - x1) * 0.7, y1 + (y2 - y1) * 0.7))
        smooth.append(points[-1])

        for i in range(1, len(smooth)):
            x1, y1 = smooth[i - 1]
            x2, y2 = smooth[i]
            dx = x2 - x1
            dy = y2 - y1
            length = math.hypot(dx, dy)
            if length == 0:
                continue

            nx = -dy / length
            ny = dx / length
            t = i / len(smooth)
            alpha = int(255 * (t ** 2))
            width = max(1, int(8 * t + 1))

            for j, color in enumerate(RAINBOW_COLORS):
                offset = (j - 3) * 3
                start_pos = (x1 + nx * offset, y1 + ny * offset)
                end_pos = (x2 + nx * offset, y2 + ny * offset)
                pygame.draw.line(screen, (*color, alpha), start_pos, end_pos, width)

    def _draw_particles(self, screen, particles):
        for p in particles:
            x, y = p["pos"]
            life = max(0.0, p["life"])
            alpha = int(255 * min(1.0, life ** 1.35))
            color = p["color"]
            kind = p.get("kind", "base")
            size = p["size"]

            if kind == "boost":
                glow_radius = int(size * (1.8 + life))
                core_radius = max(2, int(size * (0.9 + life * 0.3)))
                pygame.draw.circle(screen, (*color, int(alpha * 0.35)), (int(x), int(y)), glow_radius)
                pygame.draw.circle(screen, (*color, alpha), (int(x), int(y)), core_radius)
                pygame.draw.circle(screen, (255, 245, 255, alpha), (int(x), int(y)), max(1, core_radius // 2))
            else:
                span = max(2, int(size * (0.6 + life * 0.3)))
                pygame.draw.line(screen, (*color, alpha), (x - span, y), (x + span, y), 2)
                pygame.draw.line(screen, (*color, alpha), (x, y - span), (x, y + span), 2)
                pygame.draw.line(screen, (*color, alpha), (x - span, y - span), (x + span, y + span), 1)
                pygame.draw.line(screen, (*color, alpha), (x - span, y + span), (x + span, y - span), 1)
