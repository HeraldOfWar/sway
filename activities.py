import pygame_gui
import numpy
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
        self.termination_dialog = None  # подтверждение выхода
        self.exception_msg = None  # сообщение с ошибкой

    def run(self, card=None):
        """Запуск основного цикла"""
        while True:  # а вот и цикл!
            for event in pygame.event.get():  # pygame ждёт, чтобы пользователь что-то сделал
                if event.type == pygame.QUIT:  # ты куда???... (выход при нажатии на системный крестик)
                    self.get_termination_dialog()  # спросим у пользователя, уверен ли он в своём выходе
                    self.block_activity()  # блокируем активность
                elif event.type == pygame.USEREVENT:  # проверка событий, связанных с ui-элементами
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:  # подтверждение
                        terminate()  # выход
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:  # нажатие кнопки
                        for element in self.ui_buttons:
                            if element == event.ui_element:
                                return self.mouse_click(element)
                        if event.ui_element == self.termination_dialog.cancel_button or \
                                event.ui_element == self.termination_dialog.close_window_button:
                            self.unblock_activity()  # при закрытии окна разблокируем активность
                elif event.type == pygame.KEYDOWN:  # нажатие клавиши на клавиатуре
                    if event.key == pygame.K_ESCAPE:
                        if self.old_activity:
                            pygame.time.wait(100)  # искуственная задержка (100 мс)
                            for button in self.buttons:
                                button.is_hovered = False  # периросовка кнопок
                            return self.old_activity.run()  # запуск предыдущей активности
                        else:
                            self.get_termination_dialog()
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
        """Cоздание всех элементов пользовательского интерфейса"""
        if ui_element == play_button:  # кнопка Play
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=play_button,
                manager=self.manager,
                text='Play')
            self.ui_buttons.append(ui_button)
        elif ui_element == exit_button:  # кнопка Exit ['X']
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=exit_button,
                manager=self.manager,
                text='X')
            self.ui_buttons.append(ui_button)
        elif ui_element == escape_button:  # кнопка Escape [<-]
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=escape_button,
                manager=self.manager,
                text='<-')
            self.ui_buttons.append(ui_button)
        elif ui_element == ok_button:  # кнопка OK
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=ok_button,
                manager=self.manager,
                text='OK')
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
        if view.rect == play_button or view.rect == ok_button:
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
        self.sprites.empty()  # очистка группы спрайтов
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
                    card.is_enabled = True
                    self.sprites.add(card)

    def block_activity(self):
        """Блокировка активости"""
        for sprite in self.sprites:
            sprite.is_enabled = False  # блокировка всех спрайтов
        for button in self.buttons:
            button.is_enabled = False  # и кнопок

    def unblock_activity(self):
        """Разблокировка активности"""
        for sprite in self.sprites:
            sprite.is_enabled = True  # разблокировка всех спрайтов
        for button in self.buttons:
            button.is_enabled = True  # и кнопок

    def get_termination_dialog(self):
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


class Fragment(BasicActivity):
    """Класс фрагмента, наследуемый от стандартной активности.
    Необходим для того, чтобы не прерывать текущую активность"""

    def __init__(self, f_type, background, buttons=[], sprites=[]):
        """Инициализация фрагмента"""
        super().__init__(background, buttons, sprites)
        self.f_type = f_type  # тип фрагмента
        self.main_activity = None  # родительская активность
        self.screen2 = pygame.Surface(screen.get_size())  # второй холст, копия основного

    def output(self):
        """Отрисовка второго холста поверх основного"""
        self.screen2.blit(self.background, (0, 0))
        if self.f_type == 'rules':  # если это правила, то отрисовываем название фрагмента и фон
            title_rules = b_font.render('Правила', 1, pygame.Color('black'))
            title_rules_rect = title_rules.get_rect()
            title_rules_rect.centerx = pygame.Rect(0, 0, width, height).centerx
            self.screen2.blit(title_rules, (title_rules_rect.x, 45))
            screen.blit(self.screen2, (0, 0))
        elif self.f_type == 'help':  # если это справка, то рисуем название фрагмента и фон
            title_help = b_font.render('Справка', 1, pygame.Color('black'))
            title_help_rect = title_help.get_rect()
            title_help_rect.centerx = pygame.Rect(0, 0, width, height).centerx
            self.screen2.blit(title_help, (title_help_rect.x, 45))
            screen.blit(self.screen2, (0, 0))
        elif self.f_type == 'card_info':  # если это фрагмент с информацией о карте, то рисуем только фон
            screen.blit(self.screen2, (0, 0))
        else:
            screen.blit(self.screen2, (0, 0))

    def mouse_click(self, view):
        """Обработка нажатия клавиши мыши"""
        pygame.time.wait(100)
        for button in self.buttons:
            button.is_hovered = False
        if view.rect == ok_button and self.f_type == 'rules':
            self.next_activity.run()
        return


class MenuFragment(Fragment):
    """Класс Главного Меню в игре, также наследуемый от фрагмента,
    Чтобы не прерывать игровой цикл"""

    def run(self, card=None):
        """Запуск основного цикла"""
        while True:  # а вот и цикл!
            for event in pygame.event.get():  # pygame ждёт, чтобы пользователь что-то сделал
                if event.type == pygame.QUIT:  # ты куда???... (выход при нажатии на системный крестик)
                    """Создание диалогового окна для подтверждения выхода из игры"""
                    self.get_termination_dialog()
                    self.block_activity()
                elif event.type == pygame.USEREVENT:  # проверка событий, связанных с ui-элементами
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:  # подтверждение
                        terminate()  # выход
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:  # нажатие кнопки
                        if event.ui_element.rect == escape_button:
                            return self.mouse_click(event.ui_element)
                        for element in self.ui_buttons:
                            if element == event.ui_element:
                                self.mouse_click(element)
                        if self.termination_dialog:
                            if event.ui_element == self.termination_dialog.cancel_button or \
                                    event.ui_element == self.termination_dialog.close_window_button:
                                self.unblock_activity()
                elif event.type == pygame.KEYDOWN:  # нажатие клавиши на клавиатуре
                    if event.key == pygame.K_ESCAPE:
                        if self.old_activity:
                            pygame.time.wait(100)  # искуственная задержка (100 мс)
                            for button in self.buttons:
                                button.is_hovered = False  # периросовка кнопок
                            return self.old_activity.run()  # запуск предыдущей активности
                        else:
                            self.get_termination_dialog()
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
        screen.blit(self.background, (0, 0))  # рисуем только фон

    def load_ui(self, ui_element):
        if ui_element == escape_button:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=escape_button,
                manager=self.manager,
                text='<-')
            self.ui_buttons.append(ui_button)
        if ui_element == rules_button:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=rules_button,
                manager=self.manager,
                text='Правила')
            self.ui_buttons.append(ui_button)
        if ui_element == help_button:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=help_button,
                manager=self.manager,
                text='Помощь')
            self.ui_buttons.append(ui_button)
        if ui_element == terminate_button:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=terminate_button,
                manager=self.manager,
                text='Выйти')
            self.ui_buttons.append(ui_button)

    def mouse_click(self, view):
        """Обработка нажатия клавиши мыши"""
        pygame.time.wait(100)
        if view.rect == rules_button:  # при нажатиии на кнопку ПРАВИЛА, запускаем фрагмент с правилами
            self.main_activity.get_rules()
        if view.rect == help_button:  # при нажатии на кнопку ПОМОЩЬ, запускаем фрагмент со справкой
            self.main_activity.get_help(1)
        if view.rect == terminate_button:  # при нажатии на кнопку ВЫЙТИ
            self.get_termination_dialog()  # создаем диалог с подтверждением выхода
            self.block_activity()  # и блокируем фрагмент
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
        self.current_card, self.card_is_attacked, self.current_point = None, None, None
        self.selection_list, self.move_confirm_dialog,  self.attack_confirm_dialog = None, None, None
        self.choose_enemy, self.is_attack = False, False

    def run(self):
        self.battlepoint.set_get_info_mode()
        for card in self.battlepoint:
            card.default_rect = card.rect
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
                                self.set_static_mode()
                                self.current_card.move(self.battlepoint, self.main_activity.first_cards)
                                return
                            else:
                                self.set_static_mode()
                                self.current_card.move(self.battlepoint, self.main_activity.second_cards)
                                return
                        if event.ui_element == self.attack_confirm_dialog:
                            self.battlepoint.set_battle_mode(self.current_card, self.card_is_attacked)
                            self.battlepoint.battle(self.current_card, self.card_is_attacked)
                            self.load_ui(battle_ok)
                            self.is_attack, self.choose_enemy = True, False
                            self.current_card.is_attacked = True
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element.rect == battle_ok:
                            event.ui_element.kill()
                            self.ui_buttons.remove(event.ui_element)
                            self.set_static_mode()
                        if self.termination_dialog:
                            if event.ui_element == self.termination_dialog.cancel_button or \
                                    event.ui_element == self.termination_dialog.close_window_button:
                                self.set_static_mode()
                            if self.selection_list:
                                self.block_battlepoint()
                        if self.move_confirm_dialog:
                            if event.ui_element == self.move_confirm_dialog.cancel_button or \
                                    event.ui_element == self.move_confirm_dialog.close_window_button:
                                self.set_static_mode()
                        if self.attack_confirm_dialog:
                            if event.ui_element == self.attack_confirm_dialog.close_window_button or \
                                    event.ui_element == self.attack_confirm_dialog.cancel_button:
                                self.set_static_mode()
                        if self.exception_msg:
                            if event.ui_element == self.exception_msg.close_window_button or \
                                    event.ui_element == self.exception_msg.dismiss_button:
                                self.set_static_mode()
                        for element in self.ui_buttons:
                            if element == event.ui_element and element.is_enabled:
                                return self.mouse_click(element, True)
                    elif event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:  # выбор элемента
                        if event.ui_element == self.selection_list:  # всплывающей активности
                            if event.text == 'Атаковать':
                                if self.current_card.can_attack() == 'len_cards':
                                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                        html_message='Ложная тревога, всё чисто!',
                                        manager=self.manager,
                                        window_title='Ошибка')
                                    self.exception_msg.dismiss_button.set_text('OK')
                                    self.exception_msg.close_window_button.set_text('X')
                                elif self.current_card.can_attack() == 'chakra':
                                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                        html_message='Силы бойца на исходе, пора возвращаться в деревню!',
                                        manager=self.manager,
                                        window_title='Ошибка')
                                    self.exception_msg.dismiss_button.set_text('OK')
                                    self.exception_msg.close_window_button.set_text('X')
                                elif self.current_card.can_attack() == 'is_attacked':
                                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                        html_message='Нужно взять небольшой перерыв: прямо сейчас враг готов'
                                                     'к нашему нападению.',
                                        manager=self.manager,
                                        window_title='Ошибка')
                                    self.exception_msg.dismiss_button.set_text('OK')
                                    self.exception_msg.close_window_button.set_text('X')
                                else:
                                    self.set_static_mode()
                                    self.set_attack_mode()
                            elif event.text == 'Переместить':  # переход в состояние перемещения карты
                                self.main_activity.card_is_moving = self.current_card
                                if self.main_activity.first_cards.step == 0 or \
                                        self.main_activity.second_cards.step == 0:
                                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                        html_message='В первом ходу нельзя дважды переместить одну карту!',
                                        manager=self.manager,
                                        window_title='Ошибка')
                                    self.exception_msg.dismiss_button.set_text('OK')
                                    self.exception_msg.close_window_button.set_text('X')
                                elif self.current_card.can_move() == 'pace':
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
                                self.main_activity.get_card_info(self.current_card)
                            elif event.text == 'Вернуться в деревню':
                                if self.main_activity.first_cards.step == 0 or \
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
                        if self.mode != 'static':
                            self.set_static_mode()
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        if self.mode != 'static':
                            self.set_static_mode()
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
        if self.is_attack:
            if self.current_card.damage > self.card_is_attacked.resist:
                damage1 = b_font.render(f'-{self.current_card.damage - self.card_is_attacked.resist}',
                                        1, pygame.Color('red'))
            else:
                damage1 = b_font.render('0', 1, pygame.Color('red'))
            dmg_coords1 = damage1.get_rect()
            dmg_coords1.center = pygame.Rect(0, 0, width, height).center
            dmg_coords1.right = self.card_is_attacked.rect.left - 10
            self.screen2.blit(damage1, dmg_coords1)
            if not self.current_card.is_alive:
                self.current_card.pieces.update()
                self.current_card.pieces.draw(self.screen2)
            if self.card_is_attacked.is_alive:
                if self.card_is_attacked.damage > self.current_card.resist:
                    damage2 = b_font.render(f'-{self.card_is_attacked.damage - self.current_card.resist}',
                                            1, pygame.Color('green'))
                else:
                    damage2 = b_font.render('0', 1, pygame.Color('green'))
                dmg_coords2 = damage2.get_rect()
                dmg_coords2.center = pygame.Rect(0, 0, width, height).center
                dmg_coords2.x = self.current_card.rect.right + 10
                self.screen2.blit(damage2, dmg_coords2)
            else:
                self.card_is_attacked.pieces.update()
                self.card_is_attacked.pieces.draw(self.screen2)
        if self.choose_enemy:
            if self.main_activity.first_cards.get_state():
                self.main_activity.second_cards.update()
            else:
                self.main_activity.first_cards.update()
        screen.blit(self.screen2, (0, 0))  # отрисовка второго холста
        self.battlepoint.draw(screen)  # выдача информации о боевой точке
        clock.tick(FPS)

    def load_ui(self, ui_element):
        """Отрисовка всех кнопок"""
        if ui_element == exit_button:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=exit_button,
                manager=self.manager,
                text='X')
            self.ui_buttons.append(ui_button)
        if ui_element == battle_ok:
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=battle_ok,
                manager=self.manager,
                text='OK')
            self.ui_buttons.append(ui_button)

    def draw_points(self, point):
        """Отрисовка позиций на боевой точке"""
        for b_point in b_points[1:]:
            if point == b_point:
                if point.is_hovered:
                    color = 'red'
                else:
                    color = 'white'
                pygame.draw.rect(self.screen2, pygame.Color(color), point, 4)

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
                if view.rect == exit_button:
                    self.set_static_mode()
                    self.main_activity.set_static_mode()
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
                self.current_point = view
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
                self.current_point = view
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
                self.current_point = view
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
                self.current_point = view
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
                self.current_point = view
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
                self.current_point = view
                self.block_battlepoint()
        if self.mode == 'attack':
            if view == self.current_point:
                self.set_static_mode()
                return
            elif view in self.buttons[1:]:
                if self.current_card in self.main_activity.first_cards:
                    i = self.battlepoint.second_points.index(view)
                    self.card_is_attacked = self.battlepoint.point2_cards[i]
                else:
                    i = self.battlepoint.first_points.index(view)
                    self.card_is_attacked = self.battlepoint.point1_cards[i]
                self.attack_confirm_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                    manager=self.manager,
                    window_title='Подтверждение хода',
                    action_long_desc=f'Вы уверены, что хотите устроить сражение между {self.current_card}'
                                     f' и {self.card_is_attacked}?',
                    action_short_name='OK',
                    blocking=True)
                self.attack_confirm_dialog.close_window_button.set_text('X')
                self.block_battlepoint()

    def set_static_mode(self):
        """Установка стандартного состояния игровой активности"""
        self.mode = 'static'
        self.is_attack, self.choose_enemy = False, False
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
        self.battlepoint.set_get_info_mode()

    def set_attack_mode(self):
        self.mode = 'attack'
        self.choose_enemy = True
        if self.current_card in self.main_activity.first_cards:
            if self.battlepoint.point1_cards.index(self.current_card) == 0:
                point1.is_hovered = True
                point2.is_enabled, point3.is_enabled = False, False
                for i in range(len(self.battlepoint.second_points)):
                    if len(self.battlepoint.point2_cards) > i:
                        self.battlepoint.second_points[i].is_enabled = True
                        self.battlepoint.second_points[i].is_hovered = True
                    else:
                        self.battlepoint.second_points[i].is_enabled = False
            elif self.battlepoint.point1_cards.index(self.current_card) == 1:
                point2.is_hovered = True
                point1.is_enabled, point3.is_enabled = False, False
                for i in range(len(self.battlepoint.second_points)):
                    if len(self.battlepoint.point2_cards) > i:
                        self.battlepoint.second_points[i].is_enabled = True
                        self.battlepoint.second_points[i].is_hovered = True
                    else:
                        self.battlepoint.second_points[i].is_enabled = False
            elif self.battlepoint.point1_cards.index(self.current_card) == 2:
                point3.is_hovered = True
                point1.is_enabled, point2.is_enabled = False, False
                for i in range(len(self.battlepoint.second_points)):
                    if len(self.battlepoint.point2_cards) > i:
                        self.battlepoint.second_points[i].is_enabled = True
                        self.battlepoint.second_points[i].is_hovered = True
                    else:
                        self.battlepoint.second_points[i].is_enabled = False
        if self.current_card in self.main_activity.second_cards:
            if self.battlepoint.point2_cards.index(self.current_card) == 0:
                point4.is_hovered = True
                point5.is_enabled, point6.is_enabled = False, False
                for i in range(len(self.battlepoint.first_points)):
                    if len(self.battlepoint.point1_cards) > i:
                        self.battlepoint.first_points[i].is_enabled = True
                        self.battlepoint.first_points[i].is_hovered = True
                    else:
                        self.battlepoint.first_points[i].is_enabled = False
            elif self.battlepoint.point2_cards.index(self.current_card) == 1:
                point5.is_hovered = True
                point4.is_enabled, point6.is_enabled = False, False
                for i in range(len(self.battlepoint.first_points)):
                    if len(self.battlepoint.point1_cards) > i:
                        self.battlepoint.first_points[i].is_enabled = True
                        self.battlepoint.first_points[i].is_hovered = True
                    else:
                        self.battlepoint.first_points[i].is_enabled = False
            elif self.battlepoint.point2_cards.index(self.current_card) == 2:
                point6.is_hovered = True
                point4.is_enabled, point5.is_enabled = False, False
                for i in range(len(self.battlepoint.first_points)):
                    if len(self.battlepoint.point1_cards) > i:
                        self.battlepoint.first_points[i].is_enabled = True
                        self.battlepoint.first_points[i].is_hovered = True
                    else:
                        self.battlepoint.first_points[i].is_enabled = False
            for button in self.ui_buttons:
                button.is_enabled = False

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
        self.bonus_card = None

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
        self.get_help()  # сначала читаем о том, куда и когда нажимать!
        for deck in self.decks:
            deck.load()  # загрузка карт в руке
        while True:
            for event in pygame.event.get():  # pygame ждёт, чтобы пользователь что-то сделал
                if event.type == pygame.QUIT:  # ты куда???... (выход при нажатии на системный крестик)
                    self.get_main_menu()
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        if event.ui_element == self.termination_dialog:
                            terminate()
                        if event.ui_element == self.move_confirm_dialog:
                            pygame.time.wait(100)
                            if self.card_is_moving.can_move() == 'step':
                                self.exception_msg = pygame_gui.windows.UIMessageWindow(
                                    rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                    html_message='В первом ходу можно переместить только 3 карты!',
                                    manager=self.manager,
                                    window_title='Ошибка')
                                self.exception_msg.close_window_button.set_text('X')
                                self.exception_msg.dismiss_button.set_text('OK')
                                self.block_board()
                            elif self.card_is_moving.can_move(self.battlepoint_is_getting) == 'len_cards':
                                """Если на боевой точке уже находятся 3 союзные карты, выдаём ошибку"""
                                self.exception_msg = pygame_gui.windows.UIMessageWindow(
                                    rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                    html_message='Перевал заполнен!',
                                    manager=self.manager,
                                    window_title='Ошибка')
                                self.exception_msg.close_window_button.set_text('X')
                                self.exception_msg.dismiss_button.set_text('OK')
                                self.block_board()
                            elif self.card_is_moving.can_move() == 'pace':
                                if self.card_is_moving.fraction == KONOHAGAKURE:
                                    message = 'Вашему бойцу нужно передохнуть... ' \
                                              'А пока можете зайти перекусить в Ичираку Рамен!'
                                else:
                                    message = 'Вашему бойцу нужно передохнуть... ' \
                                              'Самое время посетить монумент Кеико Гисе!'
                                self.exception_msg = pygame_gui.windows.UIMessageWindow(
                                    rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                    html_message=message,
                                    manager=self.manager,
                                    window_title='Ошибка')
                                self.exception_msg.close_window_button.set_text('X')
                                self.exception_msg.dismiss_button.set_text('OK')
                                self.block_board()
                            else:
                                """Перемещение карты"""
                                if self.card_is_moving in self.first_cards.hand:
                                    self.card_is_moving.move(self.first_cards,
                                                             self.battlepoint_is_getting)
                                elif self.card_is_moving in self.second_cards.hand:
                                    self.card_is_moving.move(self.second_cards,
                                                             self.battlepoint_is_getting)
                                else:
                                    for battlepoint in self.battlepoints:
                                        if self.card_is_moving in battlepoint:
                                            self.card_is_moving.move(battlepoint,
                                                                     self.battlepoint_is_getting)
                                            break
                                if self.card_is_moving in self.first_cards:
                                    if self.first_cards.step == 0:
                                        self.first_cards.is_moved += 1
                                else:
                                    if self.second_cards.step == 0:
                                        self.second_cards.is_moved += 1
                                self.set_static_mode()
                            self.move_confirm_dialog = None
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        for button in self.ui_buttons:
                            if button == event.ui_element and button.is_enabled:
                                self.mouse_click(button, True)
                        if self.termination_dialog:
                            if event.ui_element == self.termination_dialog.cancel_button or \
                                    event.ui_element == self.termination_dialog.close_window_button:
                                self.set_static_mode()
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
                                self.get_card_info(self.first_cards.hand[self.first_cards.current])
                            elif event.text == 'Переместить':  # переход в состояние перемещения карты
                                self.set_move_mode(self.first_cards)
                                self.card_is_moving = self.first_cards.hand[self.first_cards.current]
                            else:  # возвращаемся в обычное состояние
                                self.set_static_mode()
                            self.selection_list1.kill()
                        elif event.ui_element == self.selection_list2:
                            if event.text == 'Информация':
                                self.set_static_mode()
                                self.get_card_info(self.second_cards.hand[self.second_cards.current])
                            elif event.text == 'Переместить':
                                self.set_move_mode(self.second_cards)
                                self.card_is_moving = self.second_cards.hand[self.second_cards.current]
                            else:
                                self.set_static_mode()
                            self.selection_list2.kill()
                elif event.type == pygame.KEYDOWN:  # нажатие клавиши клавиатуры
                    if event.key == pygame.K_ESCAPE:
                        if self.mode != 'static':
                            for battlepoint in self.battlepoints:
                                if self.card_is_moving in battlepoint:
                                    self.get_battlepoint_info(battlepoint)
                            self.set_static_mode()
                        else:
                            self.get_main_menu()
                    elif event.key == pygame.K_SPACE:
                        if self.first_cards.get_state():
                            self.mouse_click(endstep_button1)
                        else:
                            self.mouse_click(endstep_button2)
                elif event.type == pygame.MOUSEMOTION:  # движение мыши
                    self.mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:  # клик мыши
                    if event.button == pygame.BUTTON_LEFT:  # только левая кнопка!
                        if self.first_cards.get_state():
                            if self.first_cards.hand:
                                card = self.first_cards.hand[self.first_cards.current]
                                if card.rect.collidepoint(event.pos) and card.is_enabled:
                                    self.mouse_click(card)
                        elif self.second_cards.get_state():
                            if self.second_cards.hand:
                                card = self.second_cards.hand[self.second_cards.current]
                                if card.rect.collidepoint(event.pos) and card.is_enabled:
                                    self.mouse_click(card)
                        for button in self.buttons:  # проверка пересечения мыши и кнопки
                            if button.collidepoint(event.pos) and button.is_enabled:
                                self.mouse_click(button)
                self.manager.process_events(event)
            self.manager.update(FPS)
            self.output()
            self.manager.draw_ui(screen)
            clock.tick(FPS)
            pygame.display.flip()

    def output(self):
        """Отрисовка всех элементов"""
        if self.mode != 'bonus_is_bought':
            screen.blit(self.background, (0, 0))
            self.first_cards.output('white')
            self.second_cards.output('white')
            for battlepoint in self.battlepoints:
                battlepoint.output('white')
            for button in self.buttons:
                self.draw_button(button)
        else:
            background = pygame.surfarray.array3d(self.background)
            src = numpy.array(background)
            dest = numpy.zeros(background.shape)
            dest[:] = 0, 0, 0
            diff = (dest - src) * 0.65
            background = src + diff.astype(numpy.uint)
            background = pygame.surfarray.make_surface(background)
            screen.blit(background, (0, 0))

            self.first_cards.output('#a5a5a5')
            self.second_cards.output('#a5a5a5')
            for battlepoint in self.battlepoints:
                battlepoint.output('#a5a5a5')
            for button in self.buttons:
                self.draw_button(button)
            self.bonus_card.update()
            if self.bonus_card.update() == 'ready':
                pygame.time.wait(100)
                self.get_card_info(self.bonus_card)
                self.set_static_mode()
            screen.blit(self.bonus_card.image, self.bonus_card.rect)

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
                color, is_size = 'red', 5
            elif self.mode == 'bonus_is_bought':
                color, is_size = '#a5a5a5', 3
            else:
                color, is_size = 'white', 3
            pygame.draw.rect(screen, pygame.Color(color), bonus_button1, is_size)
        if button == bonus_button2:
            if button.is_hovered:
                color, is_size = 'red', 5
            elif self.mode == 'bonus_is_bought':
                color, is_size = '#a5a5a5', 3
            else:
                color, is_size = 'white', 3
            pygame.draw.rect(screen, pygame.Color(color), bonus_button2, is_size)
        for view in b_battlepoints:
            if button == view:
                if button.is_hovered:
                    pygame.draw.rect(screen, pygame.Color('red'), button, 4)
                else:
                    pygame.draw.rect(screen, pygame.Color('white'), button, 3)

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
                        self.first_cards.current = len(self.first_cards.hand) - 1
                    else:
                        self.first_cards.current -= 1
                    return
                if view.rect == rightslide1 and self.first_cards.get_state():  # прокрутка карт в руке впрво
                    if self.first_cards.current == len(self.first_cards.hand) - 1:
                        self.first_cards.current = 0
                    else:
                        self.first_cards.current += 1
                    return
                if view.rect == leftslide2 and self.second_cards.get_state():
                    if self.second_cards.current == 0:
                        self.second_cards.current = len(self.second_cards.hand) - 1
                    else:
                        self.second_cards.current -= 1
                    return
                if view.rect == rightslide2 and self.second_cards.get_state():
                    if self.second_cards.current == len(self.second_cards.hand) - 1:
                        self.second_cards.current = 0
                    else:
                        self.second_cards.current += 1
                    return
            elif view == endstep_button1:  # 1 игрок заканчивает ход
                self.first_cards.set_state(False)
                self.second_cards.set_state(True)
                self.first_cards.step += 1
                self.second_cards.update_pace()
                for card in self.first_cards:
                    card.is_attacked = False
                for card in self.first_cards.hand:
                    card.recover()
                for battlepoint in self.battlepoints:
                    if len(battlepoint.point1_cards) > len(battlepoint.point2_cards):
                        if battlepoint.title == 'Перевал 4' or battlepoint.title == 'Перевал 5' or\
                           battlepoint.title == 'Перевал 6':
                            self.first_cards.score += 1
                        self.first_cards.score += battlepoint.score
                return
            elif view == endstep_button2:  # 2 игрок заканчивает ход
                self.first_cards.set_state(True)
                self.second_cards.set_state(False)
                self.second_cards.step += 1
                self.first_cards.update_pace()
                for card in self.second_cards:
                    card.is_attacked = False
                for card in self.second_cards.hand:
                    card.recover()
                for battlepoint in self.battlepoints:
                    if len(battlepoint.point1_cards) < len(battlepoint.point2_cards):
                        if battlepoint.title == 'Перевал 1' or battlepoint.title == 'Перевал 2' or\
                           battlepoint.title == 'Перевал 3':
                            self.first_cards.score += 1
                        self.second_cards.score += battlepoint.score
                return
            elif view == bonus_button1:
                if self.first_cards.score < 25:
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
                elif len(self.first_cards.bonus_deck) == 0:
                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                        html_message='Бонусные карты закончились, дальше сам!',
                        manager=self.manager,
                        window_title='Ошибка'
                    )
                    self.exception_msg.close_window_button.set_text('X')
                    self.exception_msg.dismiss_button.set_text('OK')
                    self.block_board()
                    return
                else:
                    self.first_cards.score -= 25
                    self.bonus_card = self.first_cards.get_bonus()
                    self.set_bonus_bought_mode()
                    return
            elif view == bonus_button2:
                if self.second_cards.score < 25:
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
                elif len(self.second_cards.bonus_deck) == 0:
                    self.exception_msg = pygame_gui.windows.UIMessageWindow(
                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                        html_message='Бонусные карты закончились, дальше сам!',
                        manager=self.manager,
                        window_title='Ошибка'
                    )
                    self.exception_msg.close_window_button.set_text('X')
                    self.exception_msg.dismiss_button.set_text('OK')
                    self.block_board()
                    return
                else:
                    self.second_cards.score -= 25
                    self.bonus_card = self.second_cards.get_bonus()
                    self.set_bonus_bought_mode()
                    return
            for battlepoint in self.battlepoints:
                if view == battlepoint.view and view.is_enabled:
                    self.set_static_mode()
                    if not battlepoint.info_fragment.main_activity:
                        battlepoint.info_fragment.main_activity = self
                    self.get_battlepoint_info(battlepoint)
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
                        blocking=True)
                    self.move_confirm_dialog.close_window_button.set_text('X')
                    self.battlepoint_is_getting = battlepoint
                    self.block_board()
                    return
            if view in self.first_cards or view in self.second_cards:  # если повторно нажать на карту
                self.set_static_mode()  # тоже можно вернуться в стандартное состояние

    def set_static_mode(self):
        """Установка стандартного состояния игровой активности"""
        self.mode = 'static'
        self.card_is_moving = None
        self.first_cards.load()
        self.second_cards.load()
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
        for battlepoint in self.battlepoints:
            battlepoint.update_card_draw()

    def set_move_mode(self, view):
        """Установка состояния перемещения карты в игровой активности"""
        self.mode = 'move'
        if view == self.first_cards:
            for button in b_battlepoints:
                if button == b_pass1 or button == b_pass2 or button == b_pass3:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
            self.first_cards.hand[self.first_cards.current].is_enabled = True
        elif view == self.second_cards:
            for button in b_battlepoints:
                if button == b_pass4 or button == b_pass5 or button == b_pass6:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
            self.second_cards.hand[self.second_cards.current].is_enabled = True
        elif view.title == 'Перевал 1':
            for button in b_battlepoints:
                if button == b_pass2 or button == b_bridge1:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Перевал 2':
            for button in b_battlepoints:
                if button == b_pass1 or button == b_horanpass or button == b_pass3:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Перевал 3':
            for button in b_battlepoints:
                if button == b_pass2 or button == b_bridge2:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Перевал 4':
            for button in b_battlepoints:
                if button == b_pass5 or button == b_bridge1:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Перевал 5':
            for button in b_battlepoints:
                if button == b_pass4 or button == b_horanpass or button == b_pass6:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Перевал 6':
            for button in b_battlepoints:
                if button == b_pass5 or button == b_bridge2:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Мост 1':
            for button in b_battlepoints:
                if button == b_pass1 or button == b_horanpass or button == b_pass4:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Мост 2':
            for button in b_battlepoints:
                if button == b_pass3 or button == b_horanpass or button == b_pass6:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()
        elif view.title == 'Перевал Хорана':
            for button in b_battlepoints:
                if button == b_pass2 or button == b_bridge1 or button == b_pass5 or button == b_bridge2:
                    button.is_hovered = True
                    button.is_enabled = True
                else:
                    button.is_enabled = False
            self.block_hand()

    def set_bonus_bought_mode(self):
        self.mode = 'bonus_is_bought'
        self.bonus_card.rect.y = height
        self.block_board()

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

    def get_main_menu(self):
        """Запуск фрагмента главного меню"""
        self.fragments[0].run()
        self.first_cards.load()
        self.second_cards.load()
        for battlepoint in self.battlepoints:
            battlepoint.update_card_draw()

    def get_rules(self):
        """Запуск фрагмента с правилами"""
        self.fragments[1].run()

    def get_help(self, num=0):
        """Запуск фрагмента с правилами"""
        if num:
            self.fragments[-1].run()
        else:
            self.fragments[2].run()

    def get_card_info(self, card):
        """Запуск фрагмента с информацией о карте"""
        self.fragments[3].run(card)

    def get_battlepoint_info(self, battlepoint):
        battlepoint.info_fragment.run()  # выдача информации о боевой точке
        battlepoint.update_card_draw()
