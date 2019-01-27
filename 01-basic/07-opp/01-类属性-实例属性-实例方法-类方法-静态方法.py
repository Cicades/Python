class Game(object):
    top_score = 0

    def __init__(self, name):
        self.player_name = name

    @classmethod
    def show_top_score(cls):
        print('历史最高分为%d' % cls.top_score)

    @staticmethod
    def help_info():
        """当类中的方法与类中的其他信息无关时可以使用静态方法"""
        print('帮助信息：让僵尸吃掉你的脑子！')

    def game_start(self):
        print('%s is playing game...' % self.player_name)


hyf = Game('hyf')
hyf.game_start()
Game.show_top_score()
Game.help_info()
