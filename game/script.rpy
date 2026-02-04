# Импортируем данные о кластерах
init python:
    # Проверяем, загружены ли кластеры
    if 'clusters' not in globals():
        # Если кластеры не загружены, пробуем загрузить
        try:
            from clusters import clusters
        except:
            # Создаем пустой словарь, если файл не найден
            clusters = {}
    
    # Функция для форматирования списков
    def format_list(items, max_per_line=3):
        """Форматирует список для красивого отображения в диалоге"""
        if not items:
            return ""
        
        result = ""
        for i, item in enumerate(items):
            if i > 0:
                if i % max_per_line == 0:
                    result += "\n"
                else:
                    result += ", "
            result += item
        return result
    # Функция для показа меню со всеми кластерами с прокруткой
    def show_all_clusters_menu_with_pages():
        """
        Показывает меню со всеми кластерами с постраничной прокруткой
        """
        # Создаем список всех кластеров
        all_clusters = list(clusters.keys())
        
        # Сортируем по алфавиту
        all_clusters.sort()
        
        # Настройки пагинации
        items_per_page = 5
        current_page = 0
        total_pages = (len(all_clusters) + items_per_page - 1) // items_per_page
        
        # Основной цикл пагинации
        while True:
            # Рассчитываем элементы для текущей страницы
            start_index = current_page * items_per_page
            end_index = min(start_index + items_per_page, len(all_clusters))
            page_clusters = all_clusters[start_index:end_index]
            
            # Создаем варианты меню для текущей страницы
            menu_items = []
            
            for cluster_key in page_clusters:
                # Получаем короткое имя кластера
                short_name = get_cluster_short_name(cluster_key)
                menu_items.append((f"{short_name}", cluster_key))
            
            # Добавляем элементы навигации
            if current_page > 0:
                menu_items.append(("◀ Назад", "prev_page"))
            
            if current_page < total_pages - 1:
                menu_items.append(("Вперед ▶", "next_page"))
            
            menu_items.append(("Выйти из меню", "exit"))
            
            # Показываем заголовок с номером страницы
            title = f"Все кластеры (страница {current_page + 1} из {total_pages})"
            
            # Показываем меню
            chosen = renpy.display_menu(menu_items, title=title)
            
            # Обрабатываем выбор
            if chosen == "exit":
                return None
            elif chosen == "prev_page":
                current_page -= 1
            elif chosen == "next_page":
                current_page += 1
            else:
                return chosen
    
    # Функция-обертка для обратной совместимости
    def show_all_clusters_menu():
        """
        Показывает меню со всеми кластерами (с прокруткой)
        """
        return show_all_clusters_menu_with_pages()

# Переменные для игрока
default player_gender = "guy"  # или "girl"
default player_name = ""
default selected_cluster = None

# Определяем только коуча
define coach = Character("Амбассадор Профессионалитета", 
                        image="coach",
                        color="#FFA500")  # Оранжевый цвет

# Начало игры
label start:
    
    # Проверяем, загружены ли кластеры
    if not clusters:
        "Ошибка: данные о кластерах не загружены."
        "Пожалуйста, убедитесь, что файл clusters.rpy существует."
        return
    
    # Музыка на фоне
    play music "audio/Gimn.mp3"
    
    # Приветствие
    "Добро пожаловать!"
    "Выбери свой пол: "

    # Выбор персонажа
    menu:
        "Парень":
            $ player_gender = "guy"
            jump choose_guy
        "Девушка":
            $ player_gender = "girl"
            jump choose_girl

# Экран с мальчиком
label choose_guy: 
    show guy at center with dissolve
    "Ты выбрал персонажа - парень."
    "Как тебя зовут?"
    $ player_name = renpy.input("Введи своё имя (Стандартно - Максим):", length=20)
    $ player_name = player_name.strip()
    if player_name == "":
        $ player_name = "Максим"

    $ player = Character(player_name, image=player_gender, color="#9ca85b")  # Лаймово-зеленый
    
    hide guy
    jump meeting_with_coach

# Экран с девочкой
label choose_girl:
    show girl at center with dissolve
    "Ты выбрала персонажа - девушка."
    "Как тебя зовут?"
    $ player_name = renpy.input("Введи своё имя (Стандартно - Анна):", length=20)
    $ player_name = player_name.strip()
    if player_name == "":
        $ player_name = "Анна"

    $ player = Character(player_name, image=player_gender, color="#9ca85b")  # Лаймово-зеленый
    
    hide girl
    jump meeting_with_coach

# Встреча с коучем
label meeting_with_coach:
    # Показываем коуча
    show colledge_logo_bg
    show coach at left with dissolve
    
    # Диалог с коучем
    coach "Привет! Я твой наставник в мире профессий."
    
    # Показываем игрока рядом с коучем
    if player_gender == "guy":
        show guy at right with dissolve
    else:
        show girl at right with dissolve
    
    coach "Рада познакомиться, [player_name]! Давай пройдём тест на профориентацию."
    coach "Он поможет определить, какая профессия больше всего тебе подходит."
    
    # Ответ игрока
    if player_gender == "guy":
        player "Здравствуйте! Да, я готов пройти тест."
    else:
        player "Здравствуйте! Да, я готова пройти тест."

    coach "Отлично! Тогда начнём..."
    
    pause
    
    # Переход к выбору кластера (вместо теста)
    jump start_test

# Показ информации о выбранном кластере
label show_cluster_info:
    show coach at left
    if player_gender == "guy":
        show guy at right
    else:
        show girl at right
    
    coach "По результатам твоего выбора тебе идеально подходит [selected_cluster['name']]!"
    
    coach "В этой области очень востребованы такие профессии как:"
    
    python:
        professions = selected_cluster['professions']
        chunk_size = 3  # Показываем по 4 за раз
        
        # Разбиваем на части по chunk_size
        for i in range(0, len(professions), chunk_size):
            chunk = professions[i:i + chunk_size]
            renpy.say(coach, ", ".join(chunk))
            
            # Если есть еще элементы после этой части
            if i + chunk_size < len(professions):
                renpy.say(coach, "А также:")
    
    pause
    
    # Работодатели
    coach "Из работодателей, готовых взять тебя:"
    
    python:
        employers = selected_cluster['employers']
        chunk_size = 3  # Показываем по 4 за раз
        
        # Разбиваем на части по chunk_size
        for i in range(0, len(employers), chunk_size):
            chunk = employers[i:i + chunk_size]
            renpy.say(coach, ", ".join(chunk))
            
            # Если есть еще элементы после этой части
            if i + chunk_size < len(employers):
                renpy.say(coach, "А также:")
    
    pause
    
    # Колледжи
    coach "Обучение на эти профессии можно пройти в:"
    
    python:
        colleges = selected_cluster['colleges']
        chunk_size = 3  # Показываем по 4 за раз
        
        # Разбиваем на части по chunk_size
        for i in range(0, len(colleges), chunk_size):
            chunk = colleges[i:i + chunk_size]
            renpy.say(coach, ", ".join(chunk))
            
            # Если есть еще элементы после этой части
            if i + chunk_size < len(colleges):
                renpy.say(coach, "А также:")

    player "Спасибо! Это очень полезная информация."
    
    coach "Хочешь узнать о другом кластере или завершить знакомство?"
    
    menu:
        "Выбрать другой кластер":
            jump select_cluster
        "Завершить":
            jump end_conversation

# Завершение разговора
# Завершение разговора
label end_conversation:
    
    # Скрываем белый фон, если он показан
    if renpy.showing("white_bg"):
        hide white_bg with dissolve
    
    # Скрываем другие возможные элементы
    if renpy.showing("cluster_bg"):
        hide cluster_bg with dissolve
    if renpy.showing("text"):
        hide text with dissolve
    
    show coach at left
    if player_gender == "guy":
        show guy at right
    else:
        show girl at right
    
    coach "Удачи в выборе профессии, [player_name]! Помни, что правильный выбор профессии - это первый шаг к успешной карьере."
    coach "Если захочешь пройти тест еще раз или рассмотреть другие варианты - всегда возвращайся!"
    coach "До встречи в мире профессионалитета!"
    
    if player_gender == "guy":
        player "Спасибо за помощь! До свидания!"
    else:
        player "Спасибо за помощь! До свидания!"
    
    hide coach with dissolve
    if player_gender == "guy":
        hide guy with dissolve
    else:
        hide girl with dissolve
    
    "На этом знакомство с профессиональными кластерами Алтайского края завершено."
    "Надеемся, эта информация поможет тебе сделать осознанный выбор профессии!"
    
    # Предложение пройти тест заново
    menu:
        "Пройти тест заново":
            # Сброс результатов
            $ test_scores = {key: 0 for key in test_scores}
            jump start_test
        "Завершить игру":
            return