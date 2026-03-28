class CoinRenderer:
    def draw(self, screen, coins):
        for coin in coins:
            screen.blit(coin.animation.get_frame(), (coin.x, coin.y))
