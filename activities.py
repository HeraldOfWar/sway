import pygame_gui
from system_func import terminate
from constants import *


class BasicActivity:
    """Класс стандартного окна (активности)"""

    def __init__(self, background, buttons=[], sprites=[], old_activity=None):
        """Инициализация основных параметров окна"""
        self.background = background  # фон
        self.buttons = buttons  # список кнопок
        self.ui_buttons = []  # список ui-кнопок
        self.sprites = sprites  # спрайты
        self.old_activity = old_activity  # предыдущая активность
        self.previous_activity = None  # ещё одна предыдущая активность... (escape_button)
        self.next_activity = None  # следующая активность
        self.start_game_activity = None  # активность для запуска игры
        self.manager = pygame_gui.UIManager(size, default_theme)  # менеджер для управления элементами
        # пользовательского интерфейса
        for button in self.buttons:
            self.load_ui(button)  # преобразование кнопок в ui-кнопки
        self.termination_dialog =  None  # подтверждение хода и выхода
        self.exception_msg = None  # сообщение с ошибкой

    def run(self, card=None):
        """Запуск основного цикла"""
        while True:  # а вот и цикл!
            for event in pygame.event.get():  # pygame ждёт, чтобы пользователь что-то сделал
                if event.type == pygame.QUIT:  # ты куда???... (выход при нажатии на системный крестик)
                    """Создание диалогового окна для подтверждения выхода из игры"""
                    self.termination_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),  # размеры
                        manager=self.manager,  # менеджер
                        window_title='Подтверждение выхода',  # название
                        action_long_desc='Вы уверены, что хотите выйти?',  # основной тескт
                        action_short_name='OK',  # текст кнопки подтверждения
                        blocking=True  # блокировка всех ui-элементов
                    )
                    self.termination_dialog.close_window_button.set_text('x')
                    for sprite in self.sprites:
                        sprite.is_enabled = False  # блокировка всех спрайтов
                    for button in self.buttons:
                        button.is_enabled = False  # и кнопок
                elif event.type == pygame.USEREVENT:  # проверка событий, связанных с ui-элементами
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:  # подтверждение
                        terminate()  # выход
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:  # нажатие кнопки
                        for element in self.ui_buttons:
                            if element == event.ui_element:
                                return self.mouse_click(element)
                        if event.ui_element == self.termination_dialog.cancel_button or \
                                event.ui_element == self.termination_dialog.close_window_button:
                            for sprite in self.sprites:  # при закрытии диалогового окна
                                sprite.is_enabled = True  # разблокируем спрайты
                            for button in self.buttons:
                                button.is_enabled = True  # и изображения
                elif event.type == pygame.KEYDOWN:  # нажатие клавиши на клавиатуре
                    if event.key == pygame.K_ESCAPE:
                        if self.old_activity:
                            pygame.time.wait(100)  # искуственная задержка (100 мс)
                            for button in self.buttons:
                                button.is_hovered = False  # периросовка кнопок
                            return self.old_activity.run()  # запуск предыдущей активности
                        else:
                            self.termination_dialog = pygame_gui.windows.UIConfirmationDialog(
                                rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                manager=self.manager,
                                window_title='Подтверждение выхода',
                                action_long_desc='Вы уверены, что хотите выйти?',
                                action_short_name='OK',
                                blocking=True)
                            self.termination_dialog.close_window_button.set_text('x')
                elif event.type == pygame.MOUSEMOTION:  # движение мыши
                    self.mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:  # нажатие клавиши мыши
                    if event.button == pygame.BUTTON_LEFT:  # только левой!
                        for sprite in self.sprites:
                            if sprite.rect.collidepoint(event.pos) and sprite.is_enabled:
                                return self.mouse_click(sprite)
                self.manager.process_events(event)  # проверка событий ui-интерфеса
            self.manager.update(FPS)  # обновление менеджера
            self.output()  # отрисовка окна
            if card:
                card.get_info()  # при нажатии на карту выдаётся информация о ней
            self.manager.draw_ui(screen)  # отрисовка всех ui-элементов
            pygame.display.flip()  # смена кадров

    def output(self):
        """Отрисовка всех элементов"""
        screen.blit(self.background, (0, 0))  # отрисовка фона
        if self.sprites:
            self.sprites.draw(screen)  # отрисовка всех спрайтов

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
        pygame.time.wait(50)
        for button in self.buttons:  # если мышь пересекает кнопку, она подсвечивается другим цветом
            if button.collidepoint(event.pos) and button.is_enabled:
                button.is_hovered = True
            else:
                button.is_hovered = False

    def mouse_click(self, view):
        """Обработка нажатия клавиши мыши"""
        global FRACTION
        pygame.time.wait(100)
        if view.rect == play_button:
            self.next_activity.run()  # запуск следующей активности
        if view.rect == exit_button:
            self.old_activity.run()  # запуск предыдущей активности
        if view.rect == escape_button:
            self.previous_activity.run()  # запуск предыдущей активности
        if view == konohagakure:
            FRACTION = KONOHAGAKURE  # выбрана фракция Конохагакуре
            self.start_game_activity.run()  # запуск игровой активности
        if view == ivagakure:
            FRACTION = IVAGAKURE  # выбрана фракция Ивагакуре
            self.start_game_activity.run()
        if view == info_1:
            FRACTION = KONOHAGAKURE
            self.next_activity.load_cardlist(0)  # загрузка списка карт
            self.next_activity.run()
        if view == info_2:
            FRACTION = IVAGAKURE
            self.next_activity.load_cardlist(0)  # загрузка списка карт (игровых)
            self.next_activity.run()
        if view == playcards:
            self.load_cardlist(0)
            self.run()
        if view == bonuscards:
            self.load_cardlist(1)  # загрузка списка карт-бонусов
            self.run()
        for sprite in info_sprites:
            if view == sprite:
                self.next_activity.run(card=sprite)  # выдача информации о карте

    def load_cardlist(self, cards):
        """Загрузка списка карт"""
        self.sprites.empty()
        self.sprites.add(playcards)  # добавление 1 кнопки (Игровые карты)
        self.sprites.add(bonuscards)  # добавление 2 кнопки (Бонусные карты)
        """Предварительная установка позиции всех карт для просмотра информации о них"""
        for i in range(len(BONUSCARDS)):
            BONUSCARDS[i].rect.x = 5 + 160 * ((i % 5) % 3)
            BONUSCARDS[i].rect.y = 200 + 275 * ((i % 5) // 3)
        for i in range(len(PLAYCARDS)):
            PLAYCARDS[i].rect.x = 5 + 160 * ((i % 6) % 3)
            PLAYCARDS[i].rect.y = 200 + 275 * ((i % 6) // 3)
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
            screen.blit(self.screen2, (0, 0))
        if self.f_type == 'card_info':  # если это фрагмент с информацией о карте, то отрисовываем только фон
            screen.blit(self.background, (0, 0))

    def load_ui(self, ui_element):
        """Отрисовка всех кнопок"""
        if ui_element == ok_button:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=ok_button,
                manager=self.manager,
                text='OK')
            self.ui_buttons.append(ui_button)
        if ui_element == exit_button:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=exit_button,
                manager=self.manager,
                text='X')
            self.ui_buttons.append(ui_button)

    def mouse_click(self, view):
        """Обработка нажатия клавиши мыши"""
        pygame.time.wait(100)
        for button in self.buttons:
            button.is_hovered = False
        return


class BattleFragment(Fragment):
    """Класс фрагмента, наследуемый от стандартной активности
    Необходим для того, чтобы не прерывать текущую активность"""

    def __init__(self, f_type, background, buttons=[], sprites=[]):
        """Инициализация фрагмента"""
        super().__init__(f_type, background, buttons)
        self.screen2 = pygame.Surface(screen.get_size())  # второй холст, копия основного
        self.battlepoint = sprites
        self.mode = 'static'
        self.current_card = None
        self.main_activity, self.card_info_fragment = None, None
        self.selection_list, self.move_confirm_dialog = None, None

    def run(self):
        self.battlepoint.set_get_info_mode()
        while True:
            for event in pygame.event.get():  # pygame ждёт, чтобы пользователь что-то сделал
                if event.type == pygame.QUIT:  # ты куда???... (выход при нажатии на системный крестик)
                    self.termination_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),  # размеры
                        manager=self.manager,  # менеджер
                        window_title='Подтверждение выхода',  # название
                        action_long_desc='Вы уверены, что хотите выйти?',  # основной тескт
                        action_short_name='OK',  # текст кнопки подтверждения
                        blocking=True  # блокировка всех ui-элементов
                    )
                    self.termination_dialog.close_window_button.set_text('x')
                    self.block_battlepoint()
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        if event.ui_element == self.termination_dialog:
                            terminate()
                        if event.ui_element == self.move_confirm_dialog:
                            self.set_static_mode()
                            if self.main_activity.first_cards.get_state():
                                self.main_activity.first_cards.update_hand([self.current_card])
                                self.main_activity.first_cards.load()
                                self.battlepoint.point1_cards.remove(self.current_card)
                                self.battlepoint.remove(self.current_card)
                                self.battlepoint.update_card_draw()
                                self.current_card.is_enabled = True
                                return
                            else:
                                self.main_activity.second_cards.update_hand([self.current_card])
                                self.main_activity.second_cards.load()
                                self.battlepoint.point2_cards.remove(self.current_card)
                                self.battlepoint.remove(self.current_card)
                                self.battlepoint.update_card_draw()
                                self.current_card.is_enabled = True
                                return
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            for element in self.ui_buttons:
                                if element == event.ui_element and element.is_enabled:
                                    return self.mouse_click(event.ui_element, True)
                            if self.termination_dialog:
                                if event.ui_element == self.termination_dialog.cancel_button or \
                                        event.ui_element == self.termination_dialog.close_window_button:
                                    self.set_static_mode()
                                    self.termination_dialog = None
                                if self.selection_list:
                                    self.block_battlepoint()
                            if self.move_confirm_dialog:
                                if event.ui_element == self.move_confirm_dialog.cancel_button or \
                                        event.ui_element == self.move_confirm_dialog.close_window_button:
                                    self.set_static_mode()
                            if self.exception_msg:
                                if event.ui_element == self.exception_msg.close_window_button or \
                                        event.ui_element == self.exception_msg.dismiss_button:
                                    self.set_static_mode()
                    elif event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:  # выбор элемента
                        if event.ui_element == self.selection_list:  # всплывающей активности
                            if event.text == 'Атаковать':
                                self.set_static_mode()
                                self.set_attack_mode()
                            elif event.text == 'Переместить':  # переход в состояние перемещения карты
                                self.main_activity.card_is_moving = self.current_card
                                if self.main_activity.first_cards.step == 0 and \
                                        self.main_activity.second_cards.step == 0:
                                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                        html_message='В первом ходу нельзя дважды переместить одну карту!',
                                        manager=self.manager,
                                        window_title='Ошибка')
                                    self.exception_msg.dismiss_button.set_text('OK')
                                    self.exception_msg.close_window_button.set_text('X')
                                elif self.current_card.pace == 0:
                                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                        html_message='Вашему бойцу нужно отдохнуть...',
                                        manager=self.manager,
                                        window_title='Ошибка')
                                    self.exception_msg.dismiss_button.set_text('OK')
                                    self.exception_msg.close_window_button.set_text('X')
                                else:
                                    self.main_activity.set_move_mode(self.battlepoint)
                                    self.set_static_mode()
                                    self.selection_list.kill()
                                    return
                            elif event.text == 'Информация':  # выдача информации о карте
                                self.set_static_mode()
                                self.card_info_fragment.run(card=self.current_card)
                            elif event.text == 'Вернуться в деревню':
                                if self.main_activity.first_cards.step == 0 and \
                                        self.main_activity.second_cards.step == 0:
                                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                        html_message='В первом ходу нельзя дважды переместить одну карту!',
                                        manager=self.manager,
                                        window_title='Ошибка')
                                    self.exception_msg.dismiss_button.set_text('OK')
                                    self.exception_msg.close_window_button.set_text('X')
                                else:
                                    self.main_activity.card_is_moving = self.current_card
                                    self.move_confirm_dialog = pygame_gui.windows.UIConfirmationDialog(
                                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                        manager=self.manager,
                                        window_title='Подтверждение хода',
                                        action_long_desc=f'Вы уверены, что хотите переместить '
                                                         f'{self.main_activity.card_is_moving.name} '
                                                         f'в деревню (в "руку")?',
                                        action_short_name='OK',
                                        blocking=True)
                                    self.move_confirm_dialog.close_window_button.set_text('X')
                                self.block_battlepoint()
                            else:  # возвращаемся в обычное состояние
                                self.set_static_mode()
                            self.selection_list.kill()
                elif event.type == pygame.KEYDOWN:  # нажатие клавиши клавиатуры
                    if event.key == pygame.K_ESCAPE:
                        return
                elif event.type == pygame.MOUSEMOTION:  # движение мыши
                    self.mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:  # клик мыши
                    if event.button == pygame.BUTTON_LEFT:  # только левая кнопка!
                        for button in self.buttons:  # проверка пересечения мыши и кнопки
                            if button.collidepoint(event.pos) and button.is_enabled:
                                self.mouse_click(button)
                self.manager.process_events(event)
            self.manager.update(FPS)
            self.output()
            self.manager.draw_ui(screen)
            pygame.display.flip()

    def output(self):
        """Отрисовка второго холста поверх основного"""
        self.screen2.blit(self.background, (0, 0))
        pygame.draw.rect(self.screen2, pygame.Color('white'), (0, 327, width, 233), 3)
        if self.battlepoint.type == 'Перевал Хорана':
            for i in range(2):
                name = b_font.render(self.battlepoint.title.split()[i], 1, pygame.Color('black'))
                name_coord = name.get_rect()
                name_coord.centerx, name_coord.centery = width // 2, 45 + 45 * i
                self.screen2.blit(name, name_coord)
        else:
            name = b_font.render(self.battlepoint.title, 1, pygame.Color('black'))
            name_coord = name.get_rect()
            name_coord.centerx, name_coord.centery = width // 2, 65
            self.screen2.blit(name, name_coord)
        for point in self.buttons:
            self.draw_points(point)
        screen.blit(self.screen2, (0, 0))  # отрисовка второго холста
        self.battlepoint.draw(screen)  # выдача информации о боевой точке

    def load_ui(self, ui_element):
        """Отрисовка всех кнопок"""
        if ui_element == ok_button:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=ok_button,
                manager=self.manager,
                text='OK')
            self.ui_buttons.append(ui_button)
        if ui_element == exit_button:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=exit_button,
                manager=self.manager,
                text='X')
            self.ui_buttons.append(ui_button)

    def draw_points(self, point):
        """Отрисовка позиций на боевой точке"""
        if point == point1:
            if point.is_hovered and point.is_enabled:
                color = 'red'
            else:
                color = 'white'
            pygame.draw.rect(self.screen2, pygame.Color(color), point1, 4)
        if point == point2:
            if point.is_hovered and point.is_enabled:
                color = 'red'
            else:
                color = 'white'
            pygame.draw.rect(self.screen2, pygame.Color(color), point2, 4)
        if point == point3:
            if point.is_hovered and point.is_enabled:
                color = 'red'
            else:
                color = 'white'
            pygame.draw.rect(self.screen2, pygame.Color(color), point3, 4)
        if point == point4:
            if point.is_hovered and point.is_enabled:
                color = 'red'
            else:
                color = 'white'
            pygame.draw.rect(self.screen2, pygame.Color(color), point4, 4)
        if point == point5:
            if point.is_hovered and point.is_enabled:
                color = 'red'
            else:
                color = 'white'
            pygame.draw.rect(self.screen2, pygame.Color(color), point5, 4)
        if point == point6:
            if point.is_hovered and point.is_enabled:
                color = 'red'
            else:
                color = 'white'
            pygame.draw.rect(self.screen2, pygame.Color(color), point6, 4)

    def mouse_click(self, view, ui=False):
        """Обработка нажатия клавиши мыши"""
        pygame.time.wait(100)
        if self.mode == 'static':  # только в стандартном состоянии!
            for button in self.buttons:
                button.is_hovered = False
            if ui:
                if view.rect == exit_button:
                    self.set_static_mode()
                    return
            if view == point1 and len(self.battlepoint.point1_cards) > 0:
                item_list = ['–', 'Атаковать', 'Переместить', 'Информация']
                self.selection_list = pygame_gui.elements.UISelectionList(
                    relative_rect=pygame.Rect(view.right, view.top, 125, 150),
                    item_list=item_list,
                    default_selection='–',
                    manager=self.manager)
                if self.battlepoint.view == b_pass1 or self.battlepoint.view == b_pass2 \
                        or self.battlepoint.view == b_pass3:
                    item_list.append('Вернуться в деревню')
                    self.selection_list.set_item_list(item_list)
                self.selection_list.set_default_selection()
                self.current_card = self.battlepoint.point1_cards[0]
                self.block_battlepoint()
            if view == point2 and len(self.battlepoint.point1_cards) > 1:
                item_list = ['–', 'Атаковать', 'Переместить', 'Информация']
                self.selection_list = pygame_gui.elements.UISelectionList(
                    relative_rect=pygame.Rect(view.right, view.top, 125, 150),
                    item_list=item_list,
                    default_selection='–',
                    manager=self.manager)
                if self.battlepoint.view == b_pass1 or self.battlepoint.view == b_pass2 \
                        or self.battlepoint.view == b_pass3:
                    item_list.append('Вернуться в деревню')
                    self.selection_list.set_item_list(item_list)
                self.selection_list.set_default_selection()
                self.current_card = self.battlepoint.point1_cards[1]
                self.block_battlepoint()
            if view == point3 and len(self.battlepoint.point1_cards) > 2:
                item_list = ['–', 'Атаковать', 'Переместить', 'Информация']
                self.selection_list = pygame_gui.elements.UISelectionList(
                    relative_rect=pygame.Rect(view.right - 245, view.top, 125, 150),
                    item_list=item_list,
                    default_selection='–',
                    manager=self.manager)
                if self.battlepoint.view == b_pass1 or self.battlepoint.view == b_pass2 \
                        or self.battlepoint.view == b_pass3:
                    item_list.append('Вернуться в деревню')
                    self.selection_list.set_item_list(item_list)
                self.selection_list.set_default_selection()
                self.current_card = self.battlepoint.point1_cards[2]
                self.block_battlepoint()
            if view == point4 and len(self.battlepoint.point2_cards) > 0:
                item_list = ['–', 'Атаковать', 'Переместить', 'Информация']
                self.selection_list = pygame_gui.elements.UISelectionList(
                    relative_rect=pygame.Rect(view.right, view.top, 125, 150),
                    item_list=item_list,
                    default_selection='–',
                    manager=self.manager)
                if self.battlepoint.view == b_pass4 or self.battlepoint.view == b_pass5 \
                        or self.battlepoint.view == b_pass6:
                    item_list.append('Вернуться в деревню')
                    self.selection_list.set_item_list(item_list)
                self.selection_list.set_default_selection()
                self.current_card = self.battlepoint.point2_cards[0]
                self.block_battlepoint()
            if view == point5 and len(self.battlepoint.point2_cards) > 1:
                item_list = ['–', 'Атаковать', 'Переместить', 'Информация']
                self.selection_list = pygame_gui.elements.UISelectionList(
                    relative_rect=pygame.Rect(view.right, view.top, 125, 150),
                    item_list=item_list,
                    default_selection='–',
                    manager=self.manager)
                if self.battlepoint.view == b_pass4 or self.battlepoint.view == b_pass5 \
                        or self.battlepoint.view == b_pass6:
                    item_list.append('Вернуться в деревню')
                    self.selection_list.set_item_list(item_list)
                self.selection_list.set_default_selection()
                self.current_card = self.battlepoint.point2_cards[1]
                self.block_battlepoint()
            if view == point6 and len(self.battlepoint.point2_cards) > 2:
                item_list = ['–', 'Атаковать', 'Переместить', 'Информация']
                self.selection_list = pygame_gui.elements.UISelectionList(
                    relative_rect=pygame.Rect(view.right - 245, view.top, 125, 150),
                    item_list=item_list,
                    default_selection='–',
                    manager=self.manager)
                if self.battlepoint.view == b_pass4 or self.battlepoint.view == b_pass5 \
                        or self.battlepoint.view == b_pass6:
                    item_list.append('Вернуться в деревню')
                    self.selection_list.set_item_list(item_list)
                self.selection_list.set_default_selection()
                self.current_card = self.battlepoint.point2_cards[2]
                self.block_battlepoint()
        if self.mode == 'attack':
            if view == point1:
                self.set_static_mode()
            else:
                for point in self.buttons[1:]:
                    if view == point:
                        if self.current_card in self.battlepoint.point1_cards:
                            i = self.battlepoint.second_points.index(view)
                            self.battlepoint.set_battle_mode(self.current_card,
                                                             self.battlepoint.point2_cards[i])
                        else:
                            i = self.battlepoint.first_points.index(view)
                            self.battlepoint.set_battle_mode(self.current_card,
                                                             self.battlepoint.point1_cards[i])

    def set_static_mode(self):
        """Установка стандартного состояния игровой активности"""
        self.mode = 'static'
        for button in self.buttons:
            button.is_hovered = False
            button.is_enabled = True
        for card in self.battlepoint:
            card.is_enabled = True
        for button in self.ui_buttons:
            button.is_enabled = True
        if self.main_activity.first_cards.get_state():
            self.main_activity.second_cards.set_state(False)
        else:
            self.main_activity.first_cards.set_state(False)

    def set_attack_mode(self):
        self.mode = 'attack'
        if self.current_card in self.main_activity.first_cards:
            if self.battlepoint.point1_cards.index(self.current_card) == 0:
                point2.is_enabled, point3.is_enabled = False, False
                for i in range(len(self.battlepoint.second_points)):
                    if len(self.battlepoint.point2_cards) >= i:
                        self.battlepoint.second_points[i].is_enabled = True
                        self.battlepoint.second_points[i].is_hovered = True
                    else:
                        self.battlepoint.second_points[i].is_enabled = False
            elif self.battlepoint.point1_cards.index(self.current_card) == 1:
                point1.is_enabled, point3.is_enabled = False, False
                for i in range(len(self.battlepoint.second_points)):
                    if len(self.battlepoint.point2_cards) >= i:
                        self.battlepoint.second_points[i].is_enabled = True
                        self.battlepoint.second_points[i].is_hovered = True
                    else:
                        self.battlepoint.second_points[i].is_enabled = False
            elif self.battlepoint.point1_cards.index(self.current_card) == 2:
                point1.is_enabled, point2.is_enabled = False, False
                for i in range(len(self.battlepoint.second_points)):
                    if len(self.battlepoint.point2_cards) >= i:
                        self.battlepoint.second_points[i].is_enabled = True
                        self.battlepoint.second_points[i].is_hovered = True
                    else:
                        self.battlepoint.second_points[i].is_enabled = False
        if self.current_card in self.main_activity.second_cards:
            if self.battlepoint.point2_cards.index(self.current_card) == 0:
                point5.is_enabled, point6.is_enabled = False, False
                for i in range(len(self.battlepoint.first_points)):
                    if len(self.battlepoint.first_points) >= i:
                        self.battlepoint.first_points[i].is_enabled = True
                        self.battlepoint.first_points[i].is_hovered = True
                    else:
                        self.battlepoint.first_points[i].is_enabled = False
            elif self.battlepoint.point2_cards.index(self.current_card) == 1:
                point4.is_enabled, point6.is_enabled = False, False
                for i in range(len(self.battlepoint.first_points)):
                    if len(self.battlepoint.first_points) >= i:
                        self.battlepoint.first_points[i].is_enabled = True
                        self.battlepoint.first_points[i].is_hovered = True
                    else:
                        self.battlepoint.first_points[i].is_enabled = False
            elif self.battlepoint.point2_cards.index(self.current_card) == 2:
                point4.is_enabled, point5.is_enabled = False, False
                for i in range(len(self.battlepoint.first_points)):
                    if len(self.battlepoint.first_points) >= i:
                        self.battlepoint.first_points[i].is_enabled = True
                        self.battlepoint.first_points[i].is_hovered = True
                    else:
                        self.battlepoint.first_points[i].is_enabled = False

    def block_battlepoint(self):
        """Блокировка игрового поля"""
        for button in self.buttons:
            button.is_enabled = False
        for button in self.ui_buttons:
            button.is_enabled = False
        for card in self.battlepoint:
            card.is_enabled = False


class GameActivity(BasicActivity):
    """Класс игрового окна (активности), наследуемый от стандартного окна"""

    def __init__(self, background, buttons, decks, battlepoints, fragments):
        """Инициализация основных параметров игровой активности"""
        super().__init__(background, buttons)
        self.fragments = fragments  # список фрагментов
        self.decks = decks  # список колод
        self.first_cards = self.decks[0]  # колода игровых карт выбранной фракции
        self.second_cards = self.decks[1]  # колода игровых карт вражеской фракции
        self.battlepoints = battlepoints  # список боевых точек
        self.mode = 'static'  # стандартное состояние игровой активности
        self.move_confirm_dialog = None
        self.selection_list1, self.selection_list2 = None, None  # список действий для карты
        self.card_is_moving, self.battlepoint_is_getting = None, None  # передвигаемая карта и конечная точка

    def run(self):
        """Запуск игрового цикла"""
        if FRACTION == IVAGAKURE:  # если выбрана фракция Ивагакуре
            self.background = i_battlefield  # переворачиваем фон
            self.first_cards = self.second_cards
            self.second_cards = self.decks[0]
        self.first_cards.main_fraction = FRACTION  # передаём колодам выбранную фракцию
        self.second_cards.main_fraction = FRACTION
        self.second_cards.set_state(False)  # сначала ходит 1 игрок!
        self.first_cards.set_hand()  # заполняем руку (1 игрок)
        self.second_cards.set_hand()  # заполняем руку (2 игрок)
        self.get_rules()  # сначала читаем правила!
        for deck in self.decks:
            deck.load()  # загрузка карт в руке
        while True:
            for event in pygame.event.get():  # pygame ждёт, чтобы пользователь что-то сделал
                if event.type == pygame.QUIT:  # ты куда???... (выход при нажатии на системный крестик)
                    self.termination_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),  # размеры
                        manager=self.manager,  # менеджер
                        window_title='Подтверждение выхода',  # название
                        action_long_desc='Вы уверены, что хотите выйти?',  # основной тескт
                        action_short_name='OK',  # текст кнопки подтверждения
                        blocking=True  # блокировка всех ui-элементов
                    )
                    self.termination_dialog.close_window_button.set_text('x')
                    self.block_board()
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        if event.ui_element == self.termination_dialog:
                            terminate()
                        if event.ui_element == self.move_confirm_dialog:
                            if self.card_is_moving in self.first_cards:
                                if self.first_cards.step == 0 and self.first_cards.is_moved == 3:
                                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                        html_message='В первом ходу можно переместить только 3 карты!',
                                        manager=self.manager,
                                        window_title='Ошибка')
                                    self.exception_msg.close_window_button.set_text('X')
                                    self.exception_msg.dismiss_button.set_text('OK')
                                    self.block_board()
                                elif len(self.battlepoint_is_getting.point1_cards) == 3:
                                    """Если на боевой точке уже находятся 3 союзные карты, выдаём ошибку"""
                                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                        html_message='Перевал заполнен!',
                                        manager=self.manager,
                                        window_title='Ошибка')
                                    self.exception_msg.close_window_button.set_text('X')
                                    self.exception_msg.dismiss_button.set_text('OK')
                                    self.block_board()
                                else:
                                    """Перемещение карты"""
                                    if self.card_is_moving in self.first_cards.hand:
                                        self.first_cards.hand.remove(self.card_is_moving)
                                    for battlepoint in self.battlepoints:
                                        if self.card_is_moving in battlepoint:
                                            battlepoint.point1_cards.remove(self.card_is_moving)
                                            battlepoint.remove(self.card_is_moving)
                                            battlepoint.update_card_draw()
                                    self.battlepoint_is_getting.point1_cards.append(self.card_is_moving)
                                    self.battlepoint_is_getting.add(self.card_is_moving)
                                    self.battlepoint_is_getting.update_card_draw()
                                    self.card_is_moving.pace -= 1
                                    if self.first_cards.step == 0:
                                        self.first_cards.is_moved += 1
                            else:
                                if self.second_cards.step == 0 and self.second_cards.is_moved == 3:
                                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                        html_message='В первом ходу можно переместить только 3 карты!',
                                        manager=self.manager,
                                        window_title='Ошибка')
                                    self.exception_msg.close_window_button.set_text('X')
                                    self.exception_msg.dismiss_button.set_text('OK')
                                    self.block_board()
                                elif len(self.battlepoint_is_getting.point2_cards) == 3:
                                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                        html_message='Перевал заполнен!',
                                        manager=self.manager,
                                        window_title='Ошибка')
                                    self.exception_msg.close_window_button.set_text('X')
                                    self.exception_msg.dismiss_button.set_text('OK')
                                    self.block_board()
                                else:
                                    if self.card_is_moving in self.second_cards.hand:
                                        self.second_cards.hand.remove(self.card_is_moving)
                                    for battlepoint in self.battlepoints:
                                        if self.card_is_moving in battlepoint:
                                            battlepoint.point2_cards.remove(self.card_is_moving)
                                            battlepoint.remove(self.card_is_moving)
                                            battlepoint.update_card_draw()
                                    self.battlepoint_is_getting.point2_cards.append(self.card_is_moving)
                                    self.battlepoint_is_getting.add(self.card_is_moving)
                                    self.battlepoint_is_getting.update_card_draw()
                                    if self.second_cards.step == 0:
                                        self.second_cards.is_moved += 1
                            self.move_confirm_dialog = None
                            self.set_static_mode()
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        for element in self.ui_buttons:
                            if element == event.ui_element and element.is_enabled:
                                self.mouse_click(event.ui_element, True)
                        if self.termination_dialog:
                            if event.ui_element == self.termination_dialog.cancel_button or \
                                    event.ui_element == self.termination_dialog.close_window_button:
                                self.set_static_mode()
                                self.termination_dialog = None
                        if self.move_confirm_dialog:
                            if event.ui_element == self.move_confirm_dialog.cancel_button or \
                                    event.ui_element == self.move_confirm_dialog.close_window_button:
                                self.set_static_mode()
                                if self.card_is_moving in self.first_cards.hand:
                                    self.set_move_mode(self.first_cards)
                                elif self.card_is_moving in self.second_cards.hand:
                                    self.set_move_mode(self.second_cards)
                                else:
                                    for battlepoint in self.battlepoints:
                                        if self.card_is_moving in battlepoint:
                                            battlepoint.info_fragment.run()
                                self.move_confirm_dialog = None
                        if self.exception_msg:
                            if event.ui_element == self.exception_msg.close_window_button or \
                                    event.ui_element == self.exception_msg.dismiss_button:
                                self.set_static_mode()
                    elif event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:  # выбор элемента
                        if event.ui_element == self.selection_list1:  # всплывающей активности
                            if event.text == 'Информация':  # выдача информации о карте
                                self.set_static_mode()
                                self.fragments[1].run(self.first_cards.hand[self.first_cards.current])
                            elif event.text == 'Переместить':  # переход в состояние перемещения карты
                                self.set_move_mode(self.first_cards)
                                self.card_is_moving = self.first_cards.hand[self.first_cards.current]
                            else:  # возвращаемся в обычное состояние
                                self.set_static_mode()
                            self.selection_list1.kill()
                        elif event.ui_element == self.selection_list2:
                            if event.text == 'Информация':
                                self.set_static_mode()
                                self.fragments[1].run(self.second_cards.hand[self.second_cards.current])
                            elif event.text == 'Переместить':
                                self.set_move_mode(self.second_cards)
                                self.card_is_moving = self.second_cards.hand[self.second_cards.current]
                            else:
                                self.set_static_mode()
                            self.selection_list2.kill()
                elif event.type == pygame.KEYDOWN:  # нажатие клавиши клавиатуры
                    if event.key == pygame.K_ESCAPE:
                        if self.mode != 'static':
                            self.set_static_mode()
                        else:
                            self.termination_dialog = pygame_gui.windows.UIConfirmationDialog(
                                rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                manager=self.manager,
                                window_title='Подтверждение выхода',
                                action_long_desc='Вы уверены, что хотите выйти?',
                                action_short_name='OK',
                                blocking=True)
                            self.termination_dialog.close_window_button.set_text('x')
                            self.block_board()
                elif event.type == pygame.MOUSEMOTION:  # движение мыши
                    self.mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:  # клик мыши
                    if event.button == pygame.BUTTON_LEFT:  # только левая кнопка!
                        for button in self.buttons:  # проверка пересечения мыши и кнопки
                            if button.collidepoint(event.pos) and button.is_enabled:
                                self.mouse_click(button)
                        if self.first_cards.get_state():
                            if self.first_cards.hand:
                                card = self.first_cards.hand[self.first_cards.current]
                                if card.rect.collidepoint(event.pos) and card.is_enabled:
                                    self.mouse_click(card)
                        if self.second_cards.get_state():
                            if self.second_cards.hand:
                                card = self.second_cards.hand[self.second_cards.current]
                                if card.rect.collidepoint(event.pos) and card.is_enabled:
                                    self.mouse_click(card)
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
                if not button.is_enabled:
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
                if not button.is_enabled:
                    line = b_font3.render('Конец хода'.split()[i], 1, pygame.Color('#332f2c'))
                elif button.is_hovered:
                    line = b_font3.render('Конец хода'.split()[i], 1, pygame.Color('white'))
                else:
                    line = b_font3.render('Конец хода'.split()[i], 1, pygame.Color('black'))
                line_coord = line.get_rect()
                line_coord.centerx = pygame.Rect(35, 85, 90, 55).centerx
                screen.blit(line, (line_coord.x, 90 + 20 * i))
        if button == bonus_button1:
            if button.is_hovered:
                color, size = 'red', 5
            else:
                color, size = 'white', 3
            pygame.draw.rect(screen, pygame.Color(color), bonus_button1, size)
        if button == bonus_button2:
            if button.is_hovered:
                color, size = 'red', 5
            else:
                color, size = 'white', 3
            pygame.draw.rect(screen, pygame.Color(color), bonus_button2, size)
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

    def load_ui(self, ui_element):
        """Загрузка элементов пользовательского интерфейса"""
        if ui_element == leftslide1:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=leftslide1,
                manager=self.manager,
                text='<')
            self.ui_buttons.append(ui_button)
        if ui_element == rightslide1:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=rightslide1,
                manager=self.manager,
                text='>')
            self.ui_buttons.append(ui_button)
        if ui_element == leftslide2:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=leftslide2,
                manager=self.manager,
                text='<')
            self.ui_buttons.append(ui_button)
        if ui_element == rightslide2:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=rightslide2,
                manager=self.manager,
                text='>')
            self.ui_buttons.append(ui_button)

    def mouse_motion(self, event):
        """Проверка наведения пользователем мыши на кнопку"""
        pygame.time.wait(50)
        if self.mode == 'static':  # только в стандартном состоянии!
            for button in self.buttons:
                if button.collidepoint(event.pos) and button.is_enabled:
                    button.is_hovered = True
                else:
                    button.is_hovered = False

    def mouse_click(self, view, ui=False):
        """Обработка нажатия клавиши мыши"""
        pygame.time.wait(100)
        if self.mode == 'static':  # только в стандартном состоянии!
            for button in self.buttons:
                button.is_hovered = False
            if ui:
                if view.rect == leftslide1 and self.first_cards.get_state():  # прокрутка карт в руке влево
                    if self.first_cards.current == 0:
                        self.first_cards.current = len(self.first_cards.sprites()) - 1
                    else:
                        self.first_cards.current -= 1
                    return
                if view.rect == rightslide1 and self.first_cards.get_state():  # прокрутка карт в руке впрво
                    if self.first_cards.current == len(self.first_cards.sprites()) - 1:
                        self.first_cards.current = 0
                    else:
                        self.first_cards.current += 1
                    return
                if view.rect == leftslide2 and self.second_cards.get_state():
                    if self.second_cards.current == 0:
                        self.second_cards.current = len(self.second_cards.sprites()) - 1
                    else:
                        self.second_cards.current -= 1
                    return
                if view.rect == rightslide2 and self.second_cards.get_state():
                    if self.second_cards.current == len(self.second_cards.sprites()) - 1:
                        self.second_cards.current = 0
                    else:
                        self.second_cards.current += 1
                    return
            elif view == endstep_button1:  # 1 игрок заканчивает ход
                self.first_cards.set_state(False)
                self.second_cards.set_state(True)
                self.first_cards.step += 1
                self.second_cards.update_pace()
                for battlepoint in self.battlepoints:
                    if len(battlepoint.point1_cards) > len(battlepoint.point2_cards):
                        self.first_cards.score += battlepoint.score
                return
            elif view == endstep_button2:  # 2 игрок заканчивает ход
                self.first_cards.set_state(True)
                self.second_cards.set_state(False)
                self.second_cards.step += 1
                self.first_cards.update_pace()
                for battlepoint in self.battlepoints:
                    if len(battlepoint.point1_cards) < len(battlepoint.point2_cards):
                        self.second_cards.score += battlepoint.score
                return
            elif view == bonus_button1:
                if self.first_cards.score >= 15:  # если хватает ОЗ, покупаем бонусную карту
                    self.first_cards.score -= 15
                else:  # иначе выдаём ошибку
                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                        html_message='Недостаточно ОЗ для покупки бонусной карты!',
                        manager=self.manager,
                        window_title='Ошибка'
                    )
                    self.exception_msg.close_window_button.set_text('X')
                    self.exception_msg.dismiss_button.set_text('OK')
                    self.block_board()
                    return
            elif view == bonus_button2:
                if self.second_cards.score >= 15:
                    self.second_cards.score -= 15
                else:
                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                        html_message='Недостаточно ОЗ для покупки бонусной карты!',
                        manager=self.manager,
                        window_title='Ошибка'
                    )
                    self.exception_msg.close_window_button.set_text('X')
                    self.exception_msg.dismiss_button.set_text('OK')
                    self.block_board()
                    return
            for battlepoint in self.battlepoints:
                if view == battlepoint.view and view.is_enabled:
                    self.set_static_mode()
                    if not battlepoint.info_fragment.main_activity:
                        battlepoint.info_fragment.main_activity = self
                    if not battlepoint.info_fragment.card_info_fragment:
                        battlepoint.info_fragment.card_info_fragment = self.fragments[1]
                    battlepoint.info_fragment.run()  # выдача информации о боевой точке
                    battlepoint.update_card_draw()
                    return
            if view in self.first_cards.hand:  # при нажатии на карту в руке всплывает список действий
                self.selection_list1 = pygame_gui.elements.UISelectionList(
                    relative_rect=pygame.Rect(width // 2 + 40, height - 135, 80, 120),
                    item_list=['–', 'Переместить', 'Информация'],
                    default_selection='–',
                    manager=self.manager)
                self.block_board()
            if view in self.second_cards.hand:
                self.selection_list2 = pygame_gui.elements.UISelectionList(
                    relative_rect=pygame.Rect(width // 2 + 40, 10, 80, 120),
                    item_list=['–', 'Переместить', 'Информация'],
                    default_selection='–',
                    manager=self.manager)
                self.block_board()
            return
        elif self.mode == 'move':  # только в состоянии перемещения карты!
            for battlepoint in self.battlepoints:  # обязательно спросим у игрока, уверен ли он в своём выборе
                if view == battlepoint.view and battlepoint.view.is_enabled:
                    self.move_confirm_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                        manager=self.manager,
                        window_title='Подтверждение хода',
                        action_long_desc=f'Вы уверены, что хотите переместить {self.card_is_moving.name} '
                                         f'на {battlepoint.title}?',
                        action_short_name='OK',
                        blocking=True
                    )
                    self.move_confirm_dialog.close_window_button.set_text('X')
                    self.battlepoint_is_getting = battlepoint
                    self.block_board()
                    return
            if view in self.first_cards or view in self.second_cards:  # если повторно нажать на карту
                self.set_static_mode()  # тоже можно вернуться в стандартное состояние

    def set_static_mode(self):
        """Установка стандартного состояния игровой активности"""
        self.mode = 'static'
        for button in self.buttons:
            button.is_hovered = False
            button.is_enabled = True
        if self.first_cards.get_state():
            for card in self.first_cards:
                card.is_enabled = True
            self.second_cards.set_state(False)
        else:
            for card in self.second_cards:
                card.is_enabled = True
            self.first_cards.set_state(False)
        for button in self.ui_buttons:
            button.is_enabled = True

    def set_move_mode(self, view):
        """Установка состояния перемещения карты в игровой активности"""
        self.mode = 'move'
        if view == self.first_cards:
            for button in b_battlefields:
                if button == b_pass1 or button == b_pass2 or button == b_pass3:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
            self.first_cards.hand[self.first_cards.current].is_enabled = True
        elif view == self.second_cards:
            for button in b_battlefields:
                if button == b_pass4 or button == b_pass5 or button == b_pass6:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
            self.second_cards.hand[self.second_cards.current].is_enabled = True
        elif view.title == 'Перевал 1':
            for button in b_battlefields:
                if button == b_pass2 or button == b_bridge1:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Перевал 2':
            for button in b_battlefields:
                if button == b_pass1 or button == b_horanpass or button == b_pass3:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Перевал 3':
            for button in b_battlefields:
                if button == b_pass2 or button == b_bridge2:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Перевал 4':
            for button in b_battlefields:
                if button == b_pass5 or button == b_bridge1:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Перевал 5':
            for button in b_battlefields:
                if button == b_pass4 or button == b_horanpass or button == b_pass6:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Перевал 6':
            for button in b_battlefields:
                if button == b_pass5 or button == b_bridge2:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Мост 1':
            for button in b_battlefields:
                if button == b_pass1 or button == b_horanpass or button == b_pass4:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Мост 2':
            for button in b_battlefields:
                if button == b_pass3 or button == b_horanpass or button == b_pass6:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Перевал Хорана':
            for button in b_battlefields:
                if button == b_pass2 or button == b_bridge1 or button == b_pass5 or button == b_bridge2:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()

    def block_board(self):
        """Блокировка игрового поля"""
        for button in self.buttons:
            button.is_enabled = False
        if self.first_cards.get_state():
            for card in self.first_cards:
                card.is_enabled = False
        else:
            for card in self.second_cards:
                card.is_enabled = False
        for button in self.ui_buttons:
            button.is_enabled = False

    def block_hand(self):
        """Блокировка руки"""
        if self.first_cards.get_state():
            endstep_button1.is_enabled = False
            bonus_button1.is_enabled = False
            for card in self.first_cards:
                card.is_enabled = False
        else:
            endstep_button2.is_enabled = False
            bonus_button2.is_enabled = False
            for card in self.second_cards:
                card.is_enabled = False
        for button in self.ui_buttons:
            button.is_enabled = False

    def get_rules(self):
        """Запуск фрагмента правил"""
        self.fragments[0].run()
