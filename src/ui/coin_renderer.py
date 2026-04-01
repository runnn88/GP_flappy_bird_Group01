import pygame


class CoinRenderer:
    def draw(self, screen, coins, context):
        for coin in coins:
            frame = coin.animation.get_frame()
            if context.is_flipped:
                frame = pygame.transform.flip(frame, False, True)
            screen.blit(frame, (coin.x, coin.y))
