import pygame

from config import HEIGHT


PIPE_THEME_COLORS = {
    "noon": {
        "body": (111, 188, 55),
        "shade": (67, 122, 28),
        "highlight": (171, 230, 104),
        "rim": (86, 149, 34),
    },
    "sunset": {
        "body": (208, 146, 54),
        "shade": (132, 79, 28),
        "highlight": (241, 193, 109),
        "rim": (173, 107, 40),
    },
    "night": {
        "body": (90, 155, 174),
        "shade": (50, 93, 111),
        "highlight": (145, 205, 226),
        "rim": (67, 125, 145),
    },
    "sunrise": {
        "body": (156, 171, 83),
        "shade": (95, 109, 45),
        "highlight": (215, 226, 129),
        "rim": (124, 138, 59),
    },
}


class PipeRenderer:
    def __init__(self):
        self._cache = {}

    def draw(self, screen, pipes, theme_name):
        colors = PIPE_THEME_COLORS.get(theme_name, PIPE_THEME_COLORS["noon"])
        body_surface, cap_surface, flipped_cap_surface = self._get_surfaces(colors)

        for pipe in pipes:
            top_height = max(1, int(pipe.top))
            bottom_y = int(pipe.top + pipe.gap)
            bottom_height = max(1, HEIGHT - bottom_y)

            self._draw_pipe_segment(screen, body_surface, cap_surface, flipped_cap_surface, int(pipe.x), top_height, True)
            self._draw_pipe_segment(screen, body_surface, cap_surface, flipped_cap_surface, int(pipe.x), bottom_height, False, bottom_y)

    def _get_surfaces(self, colors):
        cache_key = tuple(colors.values())
        if cache_key not in self._cache:
            self._cache[cache_key] = self._build_pipe_surfaces(colors)
        return self._cache[cache_key]

    def _build_pipe_surfaces(self, colors):
        body_width = 80
        cap_width = 96
        cap_height = 26
        body_surface = pygame.Surface((body_width, HEIGHT), pygame.SRCALPHA)
        cap_surface = pygame.Surface((cap_width, cap_height), pygame.SRCALPHA)

        body_rect = pygame.Rect(0, 0, body_width, HEIGHT)
        pygame.draw.rect(body_surface, colors["body"], body_rect)
        pygame.draw.rect(body_surface, colors["shade"], (0, 0, 10, HEIGHT))
        pygame.draw.rect(body_surface, colors["highlight"], (12, 0, 12, HEIGHT))
        pygame.draw.rect(body_surface, colors["shade"], (body_width - 8, 0, 8, HEIGHT))

        pygame.draw.rect(cap_surface, colors["rim"], (0, 0, cap_width, cap_height), border_radius=5)
        pygame.draw.rect(cap_surface, colors["body"], (4, 4, cap_width - 8, cap_height - 8), border_radius=5)
        pygame.draw.rect(cap_surface, colors["highlight"], (12, 6, 12, cap_height - 12), border_radius=4)
        pygame.draw.rect(cap_surface, colors["shade"], (cap_width - 12, 5, 8, cap_height - 10), border_radius=3)
        pygame.draw.line(cap_surface, (46, 72, 21), (0, cap_height - 3), (cap_width, cap_height - 3), 2)

        flipped_cap_surface = pygame.transform.flip(cap_surface, False, True)

        return body_surface, cap_surface, flipped_cap_surface

    def _draw_pipe_segment(self, screen, body_surface, cap_surface, flipped_cap_surface, x, height, is_top, y=0):
        cap_height = cap_surface.get_height()
        body_width = body_surface.get_width()
        cap_x = x - ((cap_surface.get_width() - body_width) // 2)

        if is_top:
            body_height = max(1, height - cap_height)
            if body_height > 0:
                body_image = body_surface.subsurface((0, HEIGHT - body_height, body_width, body_height))
                body_image = pygame.transform.flip(body_image, False, True)
                screen.blit(body_image, (x, 0))

            screen.blit(flipped_cap_surface, (cap_x, max(0, height - cap_height)))
            return

        body_height = max(1, height - cap_height)
        if body_height > 0:
            body_image = body_surface.subsurface((0, 0, body_width, body_height))
            screen.blit(body_image, (x, y + cap_height))

        screen.blit(cap_surface, (cap_x, y))
