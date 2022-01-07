import pygame, pygame_gui
from system_func import load_image, terminate
from constants import *


class BasicActivity():
    """Класс стандартного окна (активности)"""

    def __init__(self, background, buttons=[], sprites=[], old_activity=None):
        """Инициализация основных параметров окна"""
        self.background = background  # фон
        self.buttons = buttons  # список кнопок
        self.sprites = sprites  # спрайты
        self.old_activity = old_activity  # предыдущая активность
        self.previous_activity = None  # ещё одна предыдущая активность... (escape_button)
        self.next_activity = None  # следующая активность
        self.start_game_activity = None  # активность для запуска игры
        self.manager = pygame_gui.UIManager(size, default_theme)
        self.ui_buttons = []
        for button in self.buttons:
            self.load_ui(button)

    def run(self, card=None):
        """Запуск основного цикла"""
        while True:  # а вот и цикл!
            for event in pygame.event.get():  # pygame ждёт, чтобы пользователь что-то сделал
                if event.type == pygame.QUIT:  # ты куда???... (выход при нажатии на системный крестик)
                    termination_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                        manager=self.manager,
                        window_title='Подтверждение выхода',
                        action_long_desc='Вы уверены, что хотите выйти?',
                        action_short_name='OK', blocking=True)
                    for sprite in self.sprites:
                        sprite.is_enabled = False
                    for button in self.buttons:
                        button.is_enabled = False
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        terminate()
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        for element in self.ui_buttons:
                            if element == event.ui_element:
                                return self.mouse_click(event.ui_element)
                        if event.ui_element == termination_dialog.cancel_button or \
                                event.ui_element == termination_dialog.close_window_button:
                            for sprite in self.sprites:
                                sprite.is_enabled = True
                            for button in self.buttons:
                                button.is_enabled = True
                elif event.type == pygame.KEYDOWN:  # нажатие клавиши на клавиатуре
                    if event.key == pygame.K_ESCAPE:
                        if self.old_activity:
                            pygame.time.wait(150)
                            for button in self.buttons:
                                button.is_hovered = False
                            return self.old_activity.run()
                        else:
                            termination_dialog = pygame_gui.windows.UIConfirmationDialog(
                                rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                manager=self.manager,
                                window_title='Подтверждение выхода',
                                action_long_desc='Вы уверены, что хотите выйти?',
                                action_short_name='OK',
                                blocking=True)
                elif event.type == pygame.MOUSEMOTION:  # движение мыши
                    self.mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        for sprite in self.sprites:
                            if sprite.rect.collidepoint(event.pos) and sprite.is_enabled:
                                return self.mouse_click(sprite)
                self.manager.process_events(event)
            self.manager.update(FPS)
            self.output()  # отрисовка окна
            if card:
                card.get_info()  # при нажатии на карту выдаётся информация о ней
            self.manager.draw_ui(screen)
            pygame.display.flip()  # смена кадров

    def output(self):
        """Отрисовка всех элементов"""
        screen.blit(self.background, (0, 0))  # отрисовка фона
        if self.sprites:
            self.sprites.draw(screen)

    def load_ui(self, ui_element):
        """Отрисовка всех 'элементов пользовательского интерфейса'"""
        if ui_element == play_button:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=play_button,
                manager=self.manager,
                text='Play')
            self.ui_buttons.append(ui_button)
        elif ui_element == exit_button:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=exit_button,
                manager=self.manager,
                text='X')
            self.ui_buttons.append(ui_button)
        elif ui_element == escape_button:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=escape_button,
                manager=self.manager,
                text='<-')
            self.ui_buttons.append(ui_button)

    def mouse_motion(self, event):
        """Проверка наведения пользователем мыши на кнопку"""
        pygame.time.wait(50)  # искуственная задержка (50 мс)
        for button in self.buttons:
            if button.collidepoint(event.pos) and button.is_enabled:
                button.is_hovered = True
            else:
                button.is_hovered = False

    def mouse_click(self, view):
        """Обработка нажатия клавиши мыши"""
        global FRACTION
        pygame.time.wait(100)
        if view.rect == play_button:
            self.next_activity.run()
        if view.rect == exit_button:
            self.old_activity.run()
        if view.rect == escape_button:
            self.previous_activity.run()
        if view == konohagakure:
            FRACTION = KONOHAGAKURE  # выбрана фракция Конохагакуре
            self.start_game_activity.run()
        if view == ivagakure:
            FRACTION = IVAGAKURE  # выбрана фракция Ивагакуре
            self.start_game_activity.run()
        if view == info_1:
            FRACTION = KONOHAGAKURE
            self.next_activity.load_cardlist(0)  # загрузка списка карт
            self.next_activity.run()
        if view == info_2:
            FRACTION = IVAGAKURE
            self.next_activity.load_cardlist(0)
            self.next_activity.run()
        if view == playcards:
            self.load_cardlist(0)
            self.run()
        if view == bonuscards:
            self.load_cardlist(1)  # загрузка списка карт-бонусов
            self.run()
        for sprite in info_sprites:
            if view == sprite:
                self.next_activity.run(card=sprite)

    def load_cardlist(self, cards):
        """Загрузка списка карт"""
        self.sprites.empty()
        self.sprites.add(playcards)  # добавление 1 кнопки (Игровые карты)
        self.sprites.add(bonuscards)  # добавление 2 кнопки (Бонусные карты)
        if cards:
            """Добавление всех бонусных карт выбранной фракции"""
            for card in BONUSCARDS:
                if card.fraction == FRACTION:
                    self.sprites.add(card)
        else:
            """Добавление всех игровых карт выбранной фракции"""
            for card in PLAYCARDS:
                if card.fraction == FRACTION:
                    if card.image != card.info_image:
                        card.image = card.info_image
                    self.sprites.add(card)


class Fragment(BasicActivity):
    """Класс фрагмента, наследуемый от стандартной активности
    Необходим для того, чтобы не прерывать текущую активность"""

    def __init__(self, f_type, background, buttons=[], sprites=[]):
        """Инициализация фрагмента"""
        super().__init__(background, buttons, sprites)
        self.f_type = f_type  # тип фрагмента
        self.screen2 = pygame.Surface(screen.get_size())  # второй холст, копия основного

    def output(self):
        """Отрисовка второго холста поверх основного"""
        self.screen2.blit(self.background, (0, 0))
        if self.f_type == 'rules':  # если это правила, то отрисовываем все правила
            title_rules = b_font.render('Правила', 1, pygame.Color('black'))
            title_rules_rect = title_rules.get_rect()
            title_rules_rect.centerx = pygame.Rect(0, 0, width, height).centerx
            self.screen2.blit(title_rules, (title_rules_rect.x, 45))
        if self.f_type == 'battlepoint':  # если это боевая точка, то отрисовываем всю информацию о точке
            battlepoint = self.sprites
            pygame.draw.rect(self.screen2, pygame.Color('white'), (0, 327, width, 233), 3)
            if battlepoint.number < 3 or battlepoint.number > 5:
                if battlepoint.number < 3:
                    name = b_font1.render(f'Перевал {battlepoint.number + 4}', 1, pygame.Color('black'))
                else:
                    name = b_font1.render(f'Перевал {battlepoint.number - 5}', 1, pygame.Color('black'))
                name_coord = name.get_rect()
                name_coord.centerx, name_coord.centery = width // 2, 65
                self.screen2.blit(name, name_coord)
            elif battlepoint.number == 4:
                for i in range(2):
                    name = b_font.render(f'Перевал Хорана'.split()[i], 1, pygame.Color('black'))
                    name_coord = name.get_rect()
                    name_coord.centerx, name_coord.centery = width // 2, 45 + 45 * i
                    self.screen2.blit(name, name_coord)
            else:
                name = b_font.render(f'Мост {battlepoint.number % 3 // 2 + 1}', 1, pygame.Color('black'))
                name_coord = name.get_rect()
                name_coord.centerx, name_coord.centery = width // 2, 65
                self.screen2.blit(name, name_coord)
            for point in self.buttons:
                self.draw_points(point)
        screen.blit(self.screen2, (0, 0))  # отрисовка второго холста

    def load_ui(self, ui_element):
        """Отрисовка всех кнопок"""
        if ui_element == ok_button:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=ok_button,
                manager=self.manager,
                text='OK')
            self.ui_buttons.append(ui_button)
        elif ui_element == exit_button:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=exit_button,
                manager=self.manager,
                text='X')
            self.ui_buttons.append(ui_button)

    def draw_points(self, point):
        if point == point1:
            if point.is_hovered:
                color = 'red'
            else:
                color = 'white'
            pygame.draw.rect(self.screen2, pygame.Color(color), point1, 4)
        if point == point2:
            if point.is_hovered:
                color = 'red'
            else:
                color = 'white'
            pygame.draw.rect(self.screen2, pygame.Color(color), point2, 4)
        if point == point3:
            if point.is_hovered:
                color = 'red'
            else:
                color = 'white'
            pygame.draw.rect(self.screen2, pygame.Color(color), point3, 4)
        if point == point4:
            if point.is_hovered:
                color = 'red'
            else:
                color = 'white'
            pygame.draw.rect(self.screen2, pygame.Color(color), point4, 4)
        if point == point5:
            if point.is_hovered:
                color = 'red'
            else:
                color = 'white'
            pygame.draw.rect(self.screen2, pygame.Color(color), point5, 4)
        if point == point6:
            if point.is_hovered:
                color = 'red'
            else:
                color = 'white'
            pygame.draw.rect(self.screen2, pygame.Color(color), point6, 4)

    def mouse_click(self, view):
        """Обработка нажатия клавиши мыши"""
        pygame.time.wait(100)
        for button in self.buttons:
            button.is_hovered = False


class GameActivity(BasicActivity):
    """Класс игрового окна (активности), наследуемый от стандартного окна"""

    def __init__(self, background, buttons, decks, battlepoints, fragments):
        """Инициализация основных параметров игровой активности"""
        super().__init__(background, buttons)
        self.fragments = fragments
        self.decks = decks
        self.first_cards = self.decks[0]  # колода игровых карт выбранной фракции
        self.second_cards = self.decks[1]  # колода игровых карт вражеской фракции
        self.battlepoints = battlepoints  # список боевых точек
        self.mode = FRACTION  # определение выбранной фракции

    def run(self):
        "Запуск игрового цикл"
        self.mode = FRACTION
        if self.mode == IVAGAKURE:  # если выбрана фракция Ивагакуре
            self.background = i_battlefield  # переворачиваем фон
            self.first_cards = self.second_cards
            self.second_cards = self.decks[0]
        self.first_cards.main_fraction = self.mode  # передаём колодам выбранную фракцию
        self.second_cards.main_fraction = self.mode
        self.second_cards.is_active = False # сначала ходит 1 игрок!
        self.first_cards.set_hand() # заполняем руку (1 игрок)
        self.second_cards.set_hand() # заполняем руку (2 игрок)
        self.get_rules()  # сначала читаем правила!
        while True:
            for event in pygame.event.get():  # pygame ждёт, чтобы пользователь что-то сделал
                if event.type == pygame.QUIT:  # ты куда???... (выход при нажатии на системный крестик)
                    termination_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                        manager=self.manager,
                        window_title='Подтверждение выхода',
                        action_long_desc='Вы уверены, что хотите выйти?',
                        action_short_name='OK', blocking=True)
                    for sprite in self.sprites:
                        sprite.is_enabled = False
                    for button in self.buttons:
                        button.is_enabled = False
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        terminate()
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        for element in self.ui_buttons:
                            if element == event.ui_element:
                                return self.mouse_click(event.ui_element)
                        if event.ui_element == termination_dialog.cancel_button or \
                                event.ui_element == termination_dialog.close_window_button:
                            for sprite in self.sprites:
                                sprite.is_enabled = True
                            for button in self.buttons:
                                button.is_enabled = True
                elif event.type == pygame.KEYDOWN:  # нажатие клавиши на клавиатуре
                    if event.key == pygame.K_ESCAPE:
                        if self.old_activity:
                            pygame.time.wait(150)
                            for button in self.buttons:
                                button.is_hovered = False
                            return self.old_activity.run()
                        else:
                            termination_dialog = pygame_gui.windows.UIConfirmationDialog(
                                rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                manager=self.manager,
                                window_title='Подтверждение выхода',
                                action_long_desc='Вы уверены, что хотите выйти?',
                                action_short_name='OK',
                                blocking=True)
                elif event.type == pygame.MOUSEMOTION:  # движение мыши
                    self.mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:  # клик мыши
                    if event.button == pygame.BUTTON_LEFT:  # только левая кнопка!
                        for button in self.buttons:
                            if button.collidepoint(event.pos) and button.is_enabled:  # проверка пересечения мыши и кнопки
                                self.mouse_click(button)
                self.manager.process_events(event)
            self.manager.update(FPS)
            self.output()
            self.manager.draw_ui(screen)
            pygame.display.flip()

    def output(self):
        """Отрисовка всех элементов"""
        screen.blit(self.background, (0, 0))
        self.first_cards.output()
        self.second_cards.output()
        for battlepoint in self.battlepoints:
            battlepoint.output()
        for button in self.buttons:
            self.draw_button(button)

    def draw_button(self, button):
        """Отрисовка всех кнопок"""
        if button == endstep_button1:
            for i in range(len('Конец хода'.split())):
                if not self.first_cards.is_active:
                    line = b_font3.render('Конец хода'.split()[i], 1, pygame.Color('#332f2c'))
                elif button.is_hovered:
                    line = b_font3.render('Конец хода'.split()[i], 1, pygame.Color('white'))
                else:
                    line = b_font3.render('Конец хода'.split()[i], 1, pygame.Color('black'))
                line_coord = line.get_rect()
                line_coord.centerx = pygame.Rect(width - 125, height - 140, 90, 55).centerx
                screen.blit(line, (line_coord.x, height - 135 + 20 * i))
        if button == endstep_button2:
            for i in range(len('Конец хода'.split())):
                if not self.second_cards.is_active:
                    line = b_font3.render('Конец хода'.split()[i], 1, pygame.Color('#332f2c'))
                elif button.is_hovered:
                    line = b_font3.render('Конец хода'.split()[i], 1, pygame.Color('white'))
                else:
                    line = b_font3.render('Конец хода'.split()[i], 1, pygame.Color('black'))
                line_coord = line.get_rect()
                line_coord.centerx = pygame.Rect(35, 85, 90, 55).centerx
                screen.blit(line, (line_coord.x, 90 + 20 * i))
        if button == bonus_button1:
            if self.first_cards.is_active and button.is_hovered:
                color, size = 'red', 5
            else:
                color, size = 'white', 3
            pygame.draw.rect(screen, pygame.Color(color), bonus_button1, size)
        if button == leftslide1:
            if self.first_cards.is_active and button.is_hovered:
                color = 'black'
            else:
                color = 'white'
            pygame.draw.rect(screen, pygame.Color(color), leftslide1, 3)
            pygame.draw.polygon(screen, pygame.Color(color), ((174, height - 93), (174, height - 53),
                                                              (140, height - 73)))
        if button == rightslide1:
            if self.first_cards.is_active and button.is_hovered:
                color = 'black'
            else:
                color = 'white'
            pygame.draw.rect(screen, pygame.Color(color), rightslide1, 3)
            pygame.draw.polygon(screen, pygame.Color(color), ((width - 174, height - 93),
                                                                (width - 174, height - 53),
                                                                (width - 139, height - 73)))
        if button == bonus_button2:
            if self.second_cards.is_active and button.is_hovered:
                color, size = 'red', 5
            else:
                color, size = 'white', 3
            pygame.draw.rect(screen, pygame.Color(color), bonus_button2, size)
        if button == leftslide2:
            if self.second_cards.is_active and button.is_hovered:
                color = 'black'
            else:
                color = 'white'
            pygame.draw.rect(screen, pygame.Color(color), leftslide2, 3)
            pygame.draw.polygon(screen, pygame.Color(color), ((174, 53), (174, 93), (140, 73)))
        if button == rightslide2:
            if self.second_cards.is_active and button.is_hovered:
                color = 'black'
            else:
                color = 'white'
            pygame.draw.rect(screen, pygame.Color(color), rightslide2, 3)
            pygame.draw.polygon(screen, pygame.Color(color), ((width - 174, 53), (width - 174, 93),
                                                              (width - 139, 73)))
        if button == b_pass1:
            if button.is_hovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_pass1, 4)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_pass1, 3)
        if button == b_pass2:
            if button.is_hovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_pass2, 4)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_pass2, 3)
        if button == b_pass3:
            if button.is_hovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_pass3, 4)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_pass3, 3)
        if button == b_pass4:
            if button.is_hovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_pass4, 4)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_pass4, 3)
        if button == b_pass5:
            if button.is_hovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_pass5, 4)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_pass5, 3)
        if button == b_pass6:
            if button.is_hovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_pass6, 4)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_pass6, 3)
        if button == b_bridge1:
            if button.is_hovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_bridge1, 4)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_bridge1, 3)
        if button == b_bridge2:
            if button.is_hovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_bridge2, 4)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_bridge2, 3)
        if button == b_horanpass:
            if button.is_hovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_horanpass, 4)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_horanpass, 3)

    def mouse_click(self, view):
        """Обработка нажатия клавиши мыши"""
        pygame.time.wait(100)
        if view == leftslide1 and self.first_cards.is_active:
            if self.first_cards.current == 0:
                self.first_cards.current = len(self.first_cards.sprites()) - 1
            else:
                self.first_cards.current -= 1
            return
        if view == rightslide1 and self.first_cards.is_active:
            if self.first_cards.current == len(self.first_cards.sprites()) - 1:
                self.first_cards.current = 0
            else:
                self.first_cards.current += 1
            return
        if view == leftslide2 and self.second_cards.is_active:
            if self.second_cards.current == 0:
                self.second_cards.current = len(self.second_cards.sprites()) - 1
            else:
                self.second_cards.current -= 1
            return
        if view == rightslide2 and self.second_cards.is_active:
            if self.second_cards.current == len(self.second_cards.sprites()) - 1:
                self.second_cards.current = 0
            else:
                self.second_cards.current += 1
            return
        for button in self.buttons:
            button.is_hovered = False
        if view == endstep_button1 and self.first_cards.is_active:
            self.first_cards.is_active = False
            self.second_cards.is_active = True
            self.first_cards.step += 1
            return
        if view == endstep_button2 and self.second_cards.is_active:
            self.first_cards.is_active = True
            self.second_cards.is_active = False
            self.second_cards.step += 1
            return
        for battlepoint in self.battlepoints:
            if view == battlepoint.view:
                return battlepoint.info_fragment.run()

    def get_rules(self):
        """Создание и запуск фрагмента правил"""
        self.fragments[0].run()

