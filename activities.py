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
                            pygame.time.wait(100)  # искусственная задержка (100 мс)
                            for button in self.buttons:
                                button.is_hovered = False  # перерисовка кнопок
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
                self.manager.process_events(event)  # проверка событий ui-интерфейса
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

    def get_exception_message(self, message):
        self.exception_msg = pygame_gui.windows.UIMessageWindow(
            rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
            html_message=message,
            manager=self.manager,
            window_title='Ошибка')
        self.exception_msg.dismiss_button.set_text('OK')
        self.exception_msg.close_window_button.set_text('X')


class Fragment(BasicActivity):
    """Класс фрагмента, наследуемый от стандартной активности.
    Необходим для того, чтобы не прерывать текущую активность."""

    def __init__(self, f_type, background, buttons=[], sprites=[]):
        """Инициализация фрагмента"""
        super().__init__(background, buttons, sprites)
        self.f_type = f_type  # тип фрагмента
        self.main_activity = None  # родительская активность
        self.screen2 = pygame.Surface(screen.get_size())  # второй холст, копия основного

    def output(self):
        """Отрисовка второго холста поверх основного"""
        self.screen2.blit(self.background, (0, 0))
        if self.f_type == 'rules':  # если это правила, то рисуем название фрагмента и фон
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
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.get_termination_dialog()
                    self.block_activity()
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        terminate()
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element.rect == escape_button:
                            return self.mouse_click(event.ui_element)
                        for element in self.ui_buttons:
                            if element == event.ui_element:
                                self.mouse_click(element)
                        if self.termination_dialog:
                            if event.ui_element == self.termination_dialog.cancel_button or \
                                    event.ui_element == self.termination_dialog.close_window_button:
                                self.unblock_activity()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.old_activity:
                            pygame.time.wait(100)
                            for button in self.buttons:
                                button.is_hovered = False
                            return self.old_activity.run()
                        else:
                            self.get_termination_dialog()
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        for sprite in self.sprites:
                            if sprite.rect.collidepoint(event.pos) and sprite.is_enabled:
                                return self.mouse_click(sprite)
                self.manager.process_events(event)
            self.manager.update(FPS)
            self.output()
            if card:
                card.get_info()
            self.manager.draw_ui(screen)
            pygame.display.flip()

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
        if ui_element == rules_button:  # кнопка ПРАВИЛА
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=rules_button,
                manager=self.manager,
                text='Правила')
            self.ui_buttons.append(ui_button)
        if ui_element == help_button:  # кнопка ПОМОЩЬ
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=help_button,
                manager=self.manager,
                text='Помощь')
            self.ui_buttons.append(ui_button)
        if ui_element == terminate_button:  # кнопка ВЫЙТИ
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=terminate_button,
                manager=self.manager,
                text='Выйти')
            self.ui_buttons.append(ui_button)

    def mouse_click(self, view):
        """Обработка нажатия клавиши мыши"""
        pygame.time.wait(100)
        if view.rect == rules_button:  # при нажатии на кнопку ПРАВИЛА запускаем фрагмент с правилами
            self.main_activity.get_rules()
        if view.rect == help_button:  # при нажатии на кнопку ПОМОЩЬ запускаем фрагмент со справкой
            self.main_activity.get_help(1)
        if view.rect == terminate_button:  # при нажатии на кнопку ВЫЙТИ
            self.get_termination_dialog()  # создаем диалог с подтверждением выхода
            self.block_activity()  # и блокируем фрагмент
        return


class BattleFragment(Fragment):
    """Класс фрагмента, наследуемый от стандартной активности.
    Необходим для того, чтобы не прерывать текущую активность."""

    def __init__(self, f_type, background, buttons=[], battlepoint=[]):
        """Инициализация фрагмента"""
        super().__init__(f_type, background, buttons)
        self.screen2 = pygame.Surface(screen.get_size())  # второй холст, копия основного
        self.battlepoint = battlepoint  # боевая точка
        self.mode = 'static'  # состояние фрагмента
        self.current_card, self.card_is_attacked, self.current_point = None, None, \
                                                                       None  # выбранные карты и точки
        self.selection_list, self.move_confirm_dialog,  self.attack_confirm_dialog = None, None, \
                                                                                     None  # диалоговые окна
        self.choose_enemy, self.is_attack = False, False  # режимы фрагмента

    def run(self):
        """Основной цикл"""
        self.battlepoint.set_get_info_mode()  # установка стандартного режима фрагмента боевой точки
        for card in self.battlepoint:
            if card.default_rect != card.rect:
                card.default_rect = card.rect  # сохраняем позиции
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_activity.get_main_menu()  # запуск главного меню
                    self.selection_list.kill()
                    self.set_static_mode()
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        if event.ui_element == self.move_confirm_dialog:  # при подтверждении возвращения
                            self.set_static_mode()  # карты в деревню устанавливаем стандартный режим
                            if self.main_activity.first_cards.get_state():
                                """Перемещение карты"""
                                self.current_card.move(self.battlepoint, self.main_activity.first_cards)
                                self.main_activity.set_static_mode()
                                return
                            else:
                                """Перемещение карты"""
                                self.current_card.move(self.battlepoint, self.main_activity.second_cards)
                                self.main_activity.set_static_mode()
                                return
                        if event.ui_element == self.attack_confirm_dialog:  # при подтверждении атаки
                            # устанавливаем режим боя
                            self.battlepoint.set_battle_mode(self.current_card, self.card_is_attacked)
                            # устраиваем поединок между картами
                            self.battlepoint.battle(self.current_card, self.card_is_attacked)
                            self.load_ui(battle_ok)  # загружаем кнопку ОК
                            self.is_attack, self.choose_enemy = True, False  # устанавливаем значения режимов
                            self.current_card.is_attacked = True  # подтверждаем, что карта уже атаковала в
                            # этом ходу
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element.rect == battle_ok:  # при нажатии на кнопку ОК
                            event.ui_element.kill()  # удаляем элемент
                            self.ui_buttons.remove(event.ui_element)  # отовсюду
                            self.set_static_mode()  # возвращаем стандартное состояние
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
                        if event.ui_element == self.selection_list:  # всплывающего списка
                            if event.text == 'Атаковать':  # переход в состояние атаки
                                if self.current_card.can_attack() == 'len_cards':  # если нет противников
                                    self.get_exception_message('Ложная тревога, всё чисто!')
                                elif self.current_card.can_attack() == 'chakra':  # если нет чакры
                                    self.get_exception_message('Силы вашего бойца на исходе, '
                                                               'пора возвращаться в деревню!')
                                elif self.current_card.can_attack() == 'is_attacked':  # если карта уже
                                    # атаковала в этом ходу
                                    self.get_exception_message('Нужно взять небольшой перерыв: прямо сейчас'
                                                               ' враг готов к нашему нападению.')
                                else:
                                    self.set_static_mode()
                                    self.set_attack_mode()  # установка состояние атаки
                            elif event.text == 'Переместить':  # переход в состояние перемещения карты
                                self.main_activity.card_is_moving = self.current_card  # устанавливаем
                                # перемещаемую карту
                                if self.current_card.can_move() == 'step':  # если это первый ход
                                    self.get_exception_message('В первом ходу нельзя дважды переместить'
                                                               ' одну карту!')
                                elif self.current_card.can_move() == 'pace':  # если закончилась скорость
                                    self.get_exception_message('Вашему бойцу нужно отдохнуть...')
                                elif self.current_card.can_move() == 'pace1':  # если не хватает скорости
                                    self.get_exception_message('Противники перекрыли все пути отступления! '
                                                               'В таком состоянии нам не выбраться!')
                                else:
                                    """Установка режима перемещения, передача текущей боевой точки и карты"""
                                    self.main_activity.set_move_mode(self.battlepoint)
                                    self.set_static_mode()
                                    self.selection_list.kill()
                                    return
                            elif event.text == 'Информация':  # выдача информации о карте
                                self.set_static_mode()
                                self.main_activity.get_card_info(self.current_card)
                            elif event.text == 'Вернуться в деревню':  # перемещение карты в "руку"
                                if self.current_card.can_move() == 'step':  # если это первый ход
                                    self.get_exception_message('В первом ходу нельзя дважды переместить'
                                                               ' одну карту!')
                                elif self.current_card.can_move() == 'pace':  # если закончилась скорость
                                    self.get_exception_message('Вашему бойцу нужно отдохнуть...')
                                elif self.current_card.can_move() == 'pace1':  # если не хватает скорости
                                    self.get_exception_message('Противники перекрыли все пути отступления! '
                                                               'В таком состоянии нам не выбраться!')
                                else:
                                    self.main_activity.card_is_moving = self.current_card
                                    self.move_confirm_dialog = pygame_gui.windows.UIConfirmationDialog(
                                        rect=pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 200),
                                        manager=self.manager,
                                        window_title='Подтверждение хода',
                                        action_long_desc=f'Вы уверены, что хотите переместить '
                                                         f'{self.current_card.name} '
                                                         f'в деревню (в "руку")?',
                                        action_short_name='OK',
                                        blocking=True)
                                    self.move_confirm_dialog.close_window_button.set_text('X')
                                self.block_battlepoint()
                            else:  # возвращаемся в обычное состояние
                                self.set_static_mode()
                            self.selection_list.kill()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # при нажатии на кнопку ESCAPE возвращаемся
                        self.set_static_mode()  # обратно на игровое поле
                        self.selection_list.kill()
                        self.main_activity.set_static_mode()
                        return
                    elif event.key == pygame.K_BACKSPACE:  # при нажатии на кнопку BACKSPACE
                        self.set_static_mode()  # возвращаем фрагмент в обычное состояние
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        for button in self.buttons:
                            if button.collidepoint(event.pos) and button.is_enabled:
                                self.mouse_click(button)
                self.manager.process_events(event)
            self.manager.update(FPS)
            self.output()
            self.manager.draw_ui(screen)
            clock.tick(FPS)  # количество кадров, сменяющихся за одну секунду
            pygame.display.flip()

    def output(self):
        """Отрисовка второго холста поверх основного"""
        self.screen2.blit(self.background, (0, 0))
        pygame.draw.rect(self.screen2, pygame.Color('white'), (0, 327, width, 233), 3)

        """Вывод названия точки"""
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
            self.draw_points(point)  # отрисовка всех точек

        if self.is_attack:  # после подтверждения атаки
            # вывод урона, полученного вражеской картой
            if self.current_card.damage > self.card_is_attacked.resist:
                damage1 = b_font.render(f'-{self.current_card.damage - self.card_is_attacked.resist}',
                                        1, pygame.Color('green'))
            else:
                damage1 = b_font.render('0', 1, pygame.Color('green'))
            dmg_coords1 = damage1.get_rect()
            dmg_coords1.center = pygame.Rect(0, 0, width, height).center
            dmg_coords1.right = self.card_is_attacked.rect.left - 10
            self.screen2.blit(damage1, dmg_coords1)
            if not self.current_card.is_alive:  # если текущая карта погибает
                self.current_card.pieces.update()  # запускаем анимацию её уничтожения
                self.current_card.pieces.draw(self.screen2)
            if self.card_is_attacked.is_alive:  # вывод урона, полученного текущей картой
                if self.card_is_attacked.damage > self.current_card.resist:
                    damage2 = b_font.render(f'-{self.card_is_attacked.damage - self.current_card.resist}',
                                            1, pygame.Color('red'))
                else:
                    damage2 = b_font.render('0', 1, pygame.Color('red'))
                dmg_coords2 = damage2.get_rect()
                dmg_coords2.center = pygame.Rect(0, 0, width, height).center
                dmg_coords2.x = self.current_card.rect.right + 10
                self.screen2.blit(damage2, dmg_coords2)
            else:  # если вражеская карта погибает, запускаем анимацию её уничтожения
                self.card_is_attacked.pieces.update()
                self.card_is_attacked.pieces.draw(self.screen2)

        if self.choose_enemy:  # пока игрок выбирает цель для нападения
            if self.main_activity.first_cards.get_state():  # воспроизводим анимацию "тряски" вражеских карт
                self.main_activity.second_cards.update()
            else:
                self.main_activity.first_cards.update()

        screen.blit(self.screen2, (0, 0))  # отрисовка второго холста
        self.battlepoint.draw(screen)  # выдача информации о боевой точке

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
        for b_point in self.buttons[1:]:
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
            """Вывод списка возможных действий при нажатии на карту"""
            if view in b_points[1:4] and \
                    len(self.battlepoint.point1_cards) > self.battlepoint.first_points.index(view):
                item_list = ['–', 'Атаковать', 'Переместить', 'Информация']  # список действий
                if view == point3:
                    x = view.right - 245
                else:
                    x = view.right
                "Создание ui-элемента со списком"
                self.selection_list = pygame_gui.elements.UISelectionList(
                    relative_rect=pygame.Rect(x, view.top, 125, 150),
                    item_list=item_list,
                    default_selection='–',
                    manager=self.manager)
                self.current_card = self.battlepoint.point1_cards[b_points[1:4].index(view)]
                self.current_point = view
                if self.battlepoint.view == b_pass1 or self.battlepoint.view == b_pass2 \
                        or self.battlepoint.view == b_pass3:  # если карта находится на перевале рядом с базой
                    item_list.append('Вернуться в деревню')  # добавляем действие "Вернуться в деревню"
                if self.current_card.get_ability():  # если у карты есть активная способность
                    item_list.append('Способность')  # добавляем действие "Способность"
                self.selection_list.set_item_list(item_list)  # сохраняем все действия
                self.selection_list.set_default_selection()  # стандартный выбор "–"
                self.block_battlepoint()
            if view in b_points[4:] and \
                    len(self.battlepoint.point2_cards) > self.battlepoint.second_points.index(view):
                item_list = ['–', 'Атаковать', 'Переместить', 'Информация']
                if view == point6:
                    x = view.right - 245
                else:
                    x = view.right
                self.selection_list = pygame_gui.elements.UISelectionList(
                    relative_rect=pygame.Rect(x, view.top, 125, 150),
                    item_list=item_list,
                    default_selection='–',
                    manager=self.manager)
                self.current_card = self.battlepoint.point2_cards[b_points[4:].index(view)]
                self.current_point = view
                if self.battlepoint.view == b_pass4 or self.battlepoint.view == b_pass5 \
                        or self.battlepoint.view == b_pass6:
                    item_list.append('Вернуться в деревню')
                if self.current_card.get_ability():
                    item_list.append('Пассивная способность')
                self.selection_list.set_item_list(item_list)
                self.selection_list.set_default_selection()
                self.block_battlepoint()
        if self.mode == 'attack':  # только в состоянии атаки!
            if view == self.current_point:  # при нажатии на текущую карту возвращаемся в обычное состояние
                self.set_static_mode()
                return
            elif view in self.buttons[1:]:  # выбор цели для нападения
                if self.current_card in self.main_activity.first_cards:
                    i = self.battlepoint.second_points.index(view)
                    self.card_is_attacked = self.battlepoint.point2_cards[i]
                else:
                    i = self.battlepoint.first_points.index(view)
                    self.card_is_attacked = self.battlepoint.point1_cards[i]
                """Создание диалогового окна с подтверждением атаки"""
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
        """Установка стандартного состояния фрагмента боевой точки"""
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
        """Установка состояния атаки"""
        self.mode = 'attack'
        self.choose_enemy = True
        if self.current_card in self.main_activity.first_cards:
            for point in self.battlepoint.first_points:
                if point == self.current_point:
                    point.is_hovered = True  # подсвечиваeм текущую карту
                else:
                    point.is_enabled = False  # и блокируем все остальные союзные
            for i in range(len(self.battlepoint.second_points)): # подсвечиваем все вражеские карты
                if len(self.battlepoint.point2_cards) > i:
                    self.battlepoint.second_points[i].is_enabled = True
                    self.battlepoint.second_points[i].is_hovered = True
        if self.current_card in self.main_activity.second_cards:
            for point in self.battlepoint.second_points:
                if point == self.current_point:
                    point.is_hovered = True
                else:
                    point.is_enabled = False
            for i in range(len(self.battlepoint.first_points)):
                if len(self.battlepoint.point1_cards) > i:
                    self.battlepoint.first_points[i].is_enabled = True
                    self.battlepoint.first_points[i].is_hovered = True
        for button in self.ui_buttons:
            button.is_enabled = False

    def block_battlepoint(self):
        """Блокировка боевой точки"""
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
        self.move_confirm_dialog = None  # диалоговое окно подтверждения хода
        self.selection_list1, self.selection_list2 = None, None  # список действий для карты
        self.card_is_moving, self.battlepoint_is_getting = None, None  # передвигаемая карта и конечная точка
        self.bonus_card = None  # выпавшая бонусная карта

    def run(self):
        """Запуск игрового цикла"""
        if FRACTION == IVAGAKURE:  # если выбрана фракция Ивагакуре
            self.background = i_battlefield  # переворачиваем фон
            self.first_cards = self.second_cards  # и устанавливаем колоду Ивагакуре активной (первой)
            self.second_cards = self.decks[0]
            self.battlepoints[0].info_fragment.background = img_iva_pass1  # меняем местами фоны боевых точек
            self.battlepoints[1].info_fragment.background = img_iva_pass2
            self.battlepoints[2].info_fragment.background = img_iva_pass3
            self.battlepoints[6].info_fragment.background = img_konoha_pass1
            self.battlepoints[7].info_fragment.background = img_konoha_pass2
            self.battlepoints[8].info_fragment.background = img_konoha_pass3
        self.first_cards.main_fraction = FRACTION  # передаём колодам выбранную фракцию
        self.second_cards.main_fraction = FRACTION
        self.second_cards.set_state(False)  # сначала ходит 1 игрок!
        self.first_cards.set_hand()  # заполняем руку (1 игрок)
        self.second_cards.set_hand()  # заполняем руку (2 игрок)
        self.get_help()  # сначала читаем о том, куда и когда нажимать!
        for deck in self.decks:
            deck.update_hand()  # загрузка карт в руке
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.get_main_menu()  # переход в главное меню
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        if event.ui_element == self.move_confirm_dialog:
                            pygame.time.wait(100)
                            if self.card_is_moving.can_move() == 'step':
                                # при попытке переместить больше 3 карт в первом ходу
                                self.get_exception_message('В первом ходу можно переместить только 3 карты!')
                                self.block_board()
                            elif self.card_is_moving.can_move(self.battlepoint_is_getting) == 'len_cards':
                                # если на боевой точке уже находятся 3 союзные карты
                                self.get_exception_message('Отправлять слишком много бойцов на одну точку'
                                                           ' неразумно. Не забывайте: ваши ресурсы '
                                                           'ограничены!')
                                self.block_board()
                            elif self.card_is_moving.can_move() == 'pace':
                                # если закончилась скорость
                                if self.card_is_moving.fraction == KONOHAGAKURE:  # для Конохагакуре
                                    self.get_exception_message('Вашему бойцу нужно передохнуть... '
                                                               'Сходите перекусить в Ичираку Рамен!')
                                else:  # для Ивагакуре
                                    self.get_exception_message('Вашему бойцу нужно передохнуть... Самое время'
                                                               ' посетить монумент Кеико Гисе!')
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
                                    if self.first_cards.step == 0:  # обновление количества карт, перемещённых
                                        self.first_cards.is_moved += 1  # в первом ходу
                                else:
                                    if self.second_cards.step == 0:
                                        self.second_cards.is_moved += 1
                                self.set_static_mode()
                            self.move_confirm_dialog = None
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        for button in self.ui_buttons:
                            if button == event.ui_element and button.is_enabled:
                                self.mouse_click(button, True)
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
                                            self.set_move_mode(battlepoint)
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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.mode != 'static':
                            for battlepoint in self.battlepoints:
                                if self.card_is_moving in battlepoint:
                                    self.set_static_mode()
                                    self.get_battlepoint_info(battlepoint)
                        else:
                            self.get_main_menu()
                    elif event.key == pygame.K_SPACE:
                        if self.first_cards.get_state():
                            self.mouse_click(endstep_button1)
                        else:
                            self.mouse_click(endstep_button2)
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        for button in self.buttons:
                            if button.collidepoint(event.pos) and button.is_enabled:
                                self.mouse_click(button)
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
                self.manager.process_events(event)
            if self.first_cards.score >= 100 or len(self.second_cards) == 0:
                return
            if self.second_cards.score >= 100 or len(self.first_cards) == 0:
                return
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
        else:  # если игрок покупает бонусную карту, затемняем экран
            background = pygame.surfarray.array3d(self.background)
            src = numpy.array(background)
            dest = numpy.zeros(background.shape)
            dest[:] = 0, 0, 0
            diff = (dest - src) * 0.65
            background = src + diff.astype(numpy.uint)
            background = pygame.surfarray.make_surface(background)
            screen.blit(background, (0, 0))

            # рисуем базы и игровое поле более тёмным цветом
            self.first_cards.output('#a5a5a5')
            self.second_cards.output('#a5a5a5')
            for battlepoint in self.battlepoints:
                battlepoint.output('#a5a5a5')
            for button in self.buttons:
                self.draw_button(button)
            self.bonus_card.update()  # и запускаем анимацию выпадения бонусной карты
            screen.blit(self.bonus_card.image, self.bonus_card.rect)
            if self.bonus_card.update() == 'ready':  # как только карта дойдёт до нужной точки,
                pygame.time.wait(100)
                self.get_card_info(self.bonus_card)  # выведем информацию о карте
                self.set_static_mode()

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
        if ui_element == leftslide1:  # слайдер влево
            ui_button = pygame_gui.elements.UIButton(
                relative_rect=leftslide1,
                manager=self.manager,
                text='<')
            self.ui_buttons.append(ui_button)
        if ui_element == rightslide1:  # слайдер вправо
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
            if view == self.card_is_moving:  # если повторно нажать на карту
                self.set_static_mode()
            elif self.card_is_moving.point in self.battlepoints and \
                    view == self.card_is_moving.point.view:  # или на точку, с которой перемещаетесь
                pygame.time.wait(50)
                self.set_static_mode()  # тоже можно вернуться в стандартное состояние
                self.get_battlepoint_info(self.card_is_moving.point)
            else:
                for battlepoint in self.battlepoints:
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

    def set_static_mode(self):
        """Установка стандартного состояния игровой активности"""
        self.mode = 'static'
        self.first_cards.update_hand()  # загрузка всех карт в руке
        self.second_cards.update_hand()
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
            battlepoint.update_card_draw()  # обновление всех карт на боевых точках

    def set_move_mode(self, place):
        """Установка состояния перемещения карты в игровой активности"""
        self.mode = 'move'
        if place == self.first_cards:  # если карта на союзной базе
            for point in b_battlepoints:
                if point in play_board[2]:  # подсвечиваем союзные перевалы
                    point.is_hovered = True
                    point.is_enabled = True
                else:
                    point.is_enabled = False  # и блокируем все остальные точки
            self.block_hand()
            self.first_cards.hand[self.first_cards.current].is_enabled = True
        elif place == self.second_cards:  # если карта на вражеской базе
            for point in b_battlepoints:
                if point in play_board[0]:  # подсвечиваем вражеские перевалы
                    point.is_hovered = True
                    point.is_enabled = True
                else:
                    point.is_enabled = False  # и блокируем все остальные точки
            self.block_hand()
            self.second_cards.hand[self.second_cards.current].is_enabled = True
        else:  # если карточка на боевой точке
            for i in range(len(play_board)):
                for j in range(len(play_board)):
                    if place.view == play_board[i][j]:  # подсвечиваем все ближайшие точки
                        if i - 1 >= 0:  # cлева
                            play_board[i - 1][j].is_hovered = True
                            play_board[i - 1][j].is_enabled = True
                        if i + 1 < len(play_board):  # справа
                            play_board[i + 1][j].is_hovered = True
                            play_board[i + 1][j].is_enabled = True
                        if j - 1 >= 0:  # сверху
                            play_board[i][j - 1].is_hovered = True
                            play_board[i][j - 1].is_enabled = True
                        if j + 1 < len(play_board):  # и снизу
                            play_board[i][j + 1].is_hovered = True
                            play_board[i][j + 1].is_enabled = True
                    elif not play_board[i][j].is_hovered:  # остальные блокируем
                        play_board[i][j].is_enabled = False
            self.block_hand()

    def set_bonus_bought_mode(self):
        """Установка состояния выпадения бонусной карты на игровой активности"""
        self.mode = 'bonus_is_bought'
        self.bonus_card.rect.y = height  # установка карте позицию за пределами экрана для вылета
        self.block_board()

    def block_board(self):
        """Блокировка игрового поля"""
        for button in self.buttons:
            button.is_enabled = False  # все кнопки
        if self.first_cards.get_state():
            for card in self.first_cards:
                card.is_enabled = False  # все карты
        else:
            for card in self.second_cards:
                card.is_enabled = False
        for button in self.ui_buttons:
            button.is_enabled = False  # все ui-кнопки
        # БЛОКИРУЕМ

    def block_hand(self):
        """Блокировка руки (базы)"""
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
