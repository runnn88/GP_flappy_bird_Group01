class PlayerRenderer:
    def draw(self, screen, player):
        screen.blit(player.animation.get_frame(), (player.x, player.y))
