# test.rpy - файл с тестом на профориентацию

init python:
  # Функция для получения пути к логотипу кластера
    def get_cluster_logo(cluster_key):
        """
        Возвращает путь к изображению логотипа кластера
        Если логотипа нет, возвращает None
        """
        # Маппинг ключей кластеров на имена файлов
        logo_files = {
            "педагогика": "педагогика",
            "медицина": "медицина",
            "туризм": "туризм",
            "сельское_хозяйство": "сельское_хозяйство",
            "легкая_промышленность": "легкая_промышленность",
            "машиностроение": "машиностроение",
            "агротехника": "агротехника",
            "транспорт": "транспорт",
            "цифровизация": "цифровизация",
            "лесная_промышленность": "лесная_промышленность"
        }
        
        if cluster_key in logo_files:
            logo_name = logo_files[cluster_key]
            # Проверяем разные форматы
            possible_paths = [
                f"logos/{logo_name}.png",
                f"logos/{logo_name}.jpg",
                f"logos/{logo_name}.webp",
                f"images/logos/{logo_name}.png",
                f"images/logos/{logo_name}.jpg"
            ]
            
            # Проверяем существование файла
            for path in possible_paths:
                if renpy.loadable(path):
                    return path
            
            # Если файл не найден, возвращаем путь для будущего использования
            return f"logos/{logo_name}.png"
        
        return None
    # Функция для определения кластеров с максимальным баллом
    def get_max_score_clusters(scores):
        if not scores:
            return ["педагогика"]  # дефолтный кластер
        
        # Находим максимальный балл
        max_score = max(scores.values())
        
        # Находим все кластеры с максимальным баллом
        max_clusters = [cluster for cluster, score in scores.items() if score == max_score]
        
        return max_clusters
    
    # Функция для добавления баллов
    def add_points(scores, cluster_list, points=1):
        for cluster in cluster_list:
            if cluster in scores:
                scores[cluster] += points
        return scores
    
    # Функция для получения кластеров со вторым по величине баллом
    def get_second_best_clusters(scores, exclude_clusters):
        """
        Возвращает кластеры со вторым по величине баллом
        """
        if not scores:
            return []
        
        # Находим максимальный балл
        max_score = max(scores.values())
        
        # Находим все кластеры, которые не в exclude_clusters
        other_clusters = {k: v for k, v in scores.items() if k not in exclude_clusters}
        
        if not other_clusters:
            return []
        
        # Находим максимальный балл среди оставшихся
        second_max_score = max(other_clusters.values())
        
        # Находим все кластеры с этим баллом
        second_best = [cluster for cluster, score in scores.items() 
                        if score == second_max_score and cluster not in exclude_clusters]
        
        return second_best

# Переменные для хранения баллов по кластерам
default test_scores = {
    "педагогика": 0,
    "медицина": 0,
    "туризм": 0,
    "сельское_хозяйство": 0,
    "легкая_промышленность": 0,
    "машиностроение": 0,
    "агротехника": 0,
    "транспорт": 0,
    "цифровизация": 0,
    "лесная_промышленность": 0
}

# Список максимальных кластеров для показа
default max_clusters_list = []

# Основной тест
label start_test:
    scene bg
    show background_main
    show coach at left with dissolve
    
    coach "Отлично! Давай начнем тест. Отвечай честно на вопросы, выбирая тот вариант, который больше всего тебе подходит."
    coach "Помни: нет правильных или неправильных ответов, только те, которые помогут понять тебя лучше."
    
    pause 1.0
    
    # Вопрос 1: Работа с людьми
    label question_1:
    coach "Первый вопрос: Как ты относишься к работе с людьми?"
    
    menu:
        "Люблю общаться и помогать другим, особенно детям":
            $ test_scores = add_points(test_scores, ["педагогика", "медицина"], 2)
            coach "Замечательно! Работа с людьми - это твое призвание."
        
        "Готов помогать, но предпочитаю технику или природу":
            $ test_scores = add_points(test_scores, ["агротехника", "транспорт", "цифровизация"], 2)
            coach "Понятно, ты больше технарь или любитель природы."
        
        "Мне нравится создавать что-то своими руками":
            $ test_scores = add_points(test_scores, ["легкая_промышленность", "машиностроение", "сельское_хозяйство"], 2)
            coach "Руки золотые! Это ценно в любой профессии."
        
        "Предпочитаю работать с данными и технологиями":
            $ test_scores = add_points(test_scores, ["цифровизация", "машиностроение"], 2)
            coach "Технологии - это будущее!"

    # Вопрос 2: Тип задач
    label question_2:
    coach "Второй вопрос: Какие задачи тебе интереснее решать?"
    
    menu:
        "Творческие: готовить, шить, создавать красивые вещи":
            $ test_scores = add_points(test_scores, ["туризм", "сельское_хозяйство", "легкая_промышленность", "лесная_промышленность"], 2)
        
        "Технические: чинить, собирать, настраивать":
            $ test_scores = add_points(test_scores, ["машиностроение", "агротехника", "транспорт"], 2)
        
        "Аналитические: программировать, считать, анализировать":
            $ test_scores = add_points(test_scores, ["цифровизация", "педагогика"], 2)
        
        "Социальные: учить, лечить, консультировать":
            $ test_scores = add_points(test_scores, ["педагогика", "медицина", "туризм"], 2)

    # Вопрос 3: Место работы
    label question_3:
    coach "Где тебе работать предпочтительнее?"
    
    menu:
        "В офисе или учебном заведении":
            $ test_scores = add_points(test_scores, ["педагогика", "цифровизация", "легкая_промышленность"], 2)
        
        "В больнице или лаборатории":
            $ test_scores = add_points(test_scores, ["медицина"], 3)
        
        "На свежем воздухе, на природе":
            $ test_scores = add_points(test_scores, ["сельское_хозяйство", "агротехника", "лесная_промышленность", "туризм"], 2)
        
        "На производстве или в гараже":
            $ test_scores = add_points(test_scores, ["машиностроение", "транспорт", "лесная_промышленность"], 2)

    # Вопрос 4: Хобби и интересы
    label question_4:
    coach "Чем ты любишь заниматься в свободное время?"
    
    menu:
        "Заботиться о животных или растениях":
            $ test_scores = add_points(test_scores, ["сельское_хозяйство", "агротехника", "лесная_промышленность"], 2)
        
        "Мастерить что-то своими руками":
            $ test_scores = add_points(test_scores, ["машиностроение", "транспорт", "легкая_промышленность"], 2)
        
        "Изучать новые технологии и программы":
            $ test_scores = add_points(test_scores, ["цифровизация", "машиностроение"], 2)
        
        "Помогать друзьям, заниматься с детьми":
            $ test_scores = add_points(test_scores, ["педагогика", "медицина", "туризм"], 2)

    # Вопрос 5: Школьные предметы
    label question_5:
    coach "Какие школьные предметы тебе нравятся больше всего?"
    
    menu:
        "Биология, химия, природоведение":
            $ test_scores = add_points(test_scores, ["медицина", "сельское_хозяйство", "агротехника", "лесная_промышленность"], 2)
        
        "Физика, математика, информатика":
            $ test_scores = add_points(test_scores, ["цифровизация", "машиностроение", "транспорт"], 2)
        
        "Технология, труд, черчение":
            $ test_scores = add_points(test_scores, ["легкая_промышленность", "машиностроение", "транспорт", "лесная_промышленность"], 2)
        
        "Литература, история, обществознание":
            $ test_scores = add_points(test_scores, ["педагогика", "туризм"], 2)

    # Вопрос 6: Важные качества
    label question_6:
    coach "Какое качество для тебя самое важное в работе?"
    
    menu:
        "Творческий подход и креативность":
            $ test_scores = add_points(test_scores, ["легкая_промышленность", "туризм", "педагогика"], 2)
        
        "Точность и аккуратность":
            $ test_scores = add_points(test_scores, ["медицина", "цифровизация", "машиностроение"], 2)
        
        "Физическая выносливость и сила":
            $ test_scores = add_points(test_scores, ["транспорт", "сельское_хозяйство", "лесная_промышленность"], 2)
        
        "Ответственность и забота о других":
            $ test_scores = add_points(test_scores, ["педагогика", "медицина", "агротехника"], 2)

    # Вопрос 7: Будущее развитие
    label question_7:
    coach "Как ты видишь свое профессиональное развитие?"
    
    menu:
        "Хочу постоянно учиться и развиваться":
            $ test_scores = add_points(test_scores, ["педагогика", "медицина", "цифровизация"], 2)
        
        "Хочу освоить конкретное ремесло":
            $ test_scores = add_points(test_scores, ["легкая_промышленность", "машиностроение", "транспорт"], 2)
        
        "Хочу работать на земле или с природой":
            $ test_scores = add_points(test_scores, ["сельское_хозяйство", "агротехника", "лесная_промышленность"], 2)
        
        "Хочу работать в сфере услуг и общения":
            $ test_scores = add_points(test_scores, ["туризм", "педагогика", "медицина"], 2)

    # Завершение теста
    coach "Отлично! Это все."
    coach "Сейчас я проанализирую твои ответы..."
    
    pause 2.0
    
    # Определяем кластеры с максимальным баллом
    $ max_clusters_list = get_max_score_clusters(test_scores)
    
    # Переходим к результатам
    jump show_max_clusters

# Показ максимальных кластеров
label show_max_clusters:
    show coach at left
    if player_gender == "guy":
        show guy at right
    else:
        show girl at right
    
    # Определяем сколько кластеров с максимальным баллом
    $ max_clusters_count = len(max_clusters_list)
    
    if max_clusters_count == 1:
        # Один максимальный кластер
        $ best_cluster = max_clusters_list[0]
        $ selected_cluster = clusters[best_cluster]
        
        coach "Результаты готовы! У тебя явно выраженные склонности к одному направлению."
        coach "По моему анализу, тебе идеально подходит..."
        pause 1.0
        coach "[selected_cluster['name']]!"
        
        # Показываем информацию об этом кластере
        call show_cluster_details(best_cluster)
        
        # После показа спрашиваем, хочет ли игрок узнать о других вариантах
        coach "Хочешь рассмотреть другие возможные направления?"
        
        menu:
            "Да, показать другие варианты":
                # Находим кластеры со вторым по величине баллом
                $ second_best = get_second_best_clusters(test_scores, max_clusters_list)
                if second_best:
                    $ max_clusters_list = second_best
                    coach "Хорошо, давай посмотрим на другие перспективные направления."
                    jump show_max_clusters_choice
                else:
                    coach "К сожалению, других направлений с высоким баллом нет."
                    jump end_conversation
            
            "Нет, этого достаточно":
                jump end_conversation
    
    else:
        # Несколько максимальных кластеров
        coach "Результаты интересные! У тебя несколько направлений показали одинаково высокий результат."
        
        # Сообщаем сколько кластеров
        if max_clusters_count == 2:
            coach "Два направления набрали максимальное количество баллов."
        elif max_clusters_count == 3:
            coach "Три направления набрали максимальное количество баллов."
        else:
            coach "[max_clusters_count] направлений набрали максимальное количество баллов."
        
        coach "Это говорит о твоей разносторонности!"
        
        # Переходим к выбору
        jump show_max_clusters_choice

# Показ выбора из максимальных кластеров
label show_max_clusters_choice:
    show coach at left
    if player_gender == "guy":
        show guy at right
    else:
        show girl at right
    
    coach "Расскажу про все максимальные направления. С какого начнем?"
    
    # Определяем, сколько у нас максимальных кластеров
    $ cluster_count = len(max_clusters_list)
    
    if cluster_count == 1:
        # Если только один кластер, просто переходим к нему
        $ selected_cluster_key = max_clusters_list[0]
        call show_cluster_details(selected_cluster_key)
        jump end_conversation
    
    elif cluster_count == 2:
        # Два кластера
        $ cluster1 = max_clusters_list[0]
        $ cluster2 = max_clusters_list[1]
        
        # Получаем понятные названия
        $ name1 = get_cluster_short_name(cluster1)
        $ name2 = get_cluster_short_name(cluster2)
        
        menu:
            "[name1]":
                $ selected_cluster_key = cluster1
                call show_cluster_details(selected_cluster_key)
                $ remaining_clusters = [cluster2]
            
            "[name2]":
                $ selected_cluster_key = cluster2
                call show_cluster_details(selected_cluster_key)
                $ remaining_clusters = [cluster1]
    
    elif cluster_count == 3:
        # Три кластера
        $ cluster1 = max_clusters_list[0]
        $ cluster2 = max_clusters_list[1]
        $ cluster3 = max_clusters_list[2]
        
        $ name1 = get_cluster_short_name(cluster1)
        $ name2 = get_cluster_short_name(cluster2)
        $ name3 = get_cluster_short_name(cluster3)
        
        menu:
            "[name1]":
                $ selected_cluster_key = cluster1
                call show_cluster_details(selected_cluster_key)
                $ remaining_clusters = [cluster2, cluster3]
            
            "[name2]":
                $ selected_cluster_key = cluster2
                call show_cluster_details(selected_cluster_key)
                $ remaining_clusters = [cluster1, cluster3]
            
            "[name3]":
                $ selected_cluster_key = cluster3
                call show_cluster_details(selected_cluster_key)
                $ remaining_clusters = [cluster1, cluster2]
    
    elif cluster_count >= 4:
        # Много кластеров - показываем первые 5
        coach "Выбери направление для подробного изучения:"
        
        # Создаем меню для первых 5 кластеров
        menu:
            # Кластер 1
            "[get_cluster_short_name(max_clusters_list[0])]" if len(max_clusters_list) > 0:
                $ selected_cluster_key = max_clusters_list[0]
                call show_cluster_details(selected_cluster_key)
                $ remaining_clusters = max_clusters_list[1:]
            
            # Кластер 2
            "[get_cluster_short_name(max_clusters_list[1])]" if len(max_clusters_list) > 1:
                $ selected_cluster_key = max_clusters_list[1]
                call show_cluster_details(selected_cluster_key)
                $ remaining_clusters = [max_clusters_list[0]] + max_clusters_list[2:]
            
            # Кластер 3
            "[get_cluster_short_name(max_clusters_list[2])]" if len(max_clusters_list) > 2:
                $ selected_cluster_key = max_clusters_list[2]
                call show_cluster_details(selected_cluster_key)
                $ remaining_clusters = max_clusters_list[:2] + max_clusters_list[3:]
            
            # Кластер 4
            "[get_cluster_short_name(max_clusters_list[3])]" if len(max_clusters_list) > 3:
                $ selected_cluster_key = max_clusters_list[3]
                call show_cluster_details(selected_cluster_key)
                $ remaining_clusters = max_clusters_list[:3] + max_clusters_list[4:]
            
            # Кластер 5
            "[get_cluster_short_name(max_clusters_list[4])]" if len(max_clusters_list) > 4:
                $ selected_cluster_key = max_clusters_list[4]
                call show_cluster_details(selected_cluster_key)
                $ remaining_clusters = max_clusters_list[:4] + max_clusters_list[5:]
    
    # После показа спрашиваем, хочет ли игрок узнать о других максимальных кластерах
    if 'remaining_clusters' in locals() and len(remaining_clusters) > 0:
        coach "Хочешь послушать про другое направление, которое тоже набрало максимальное количество баллов?"
        
        menu:
            "Да, рассказать про другой максимальный кластер":
                # Обновляем список для показа
                $ max_clusters_list = remaining_clusters
                jump show_max_clusters_choice
            
            "Нет, завершить":
                jump end_conversation
    else:
        jump end_conversation

# Функция для получения короткого названия кластера
init python:
    def get_cluster_short_name(cluster_key):
        """
        Возвращает короткое понятное название кластера
        Умное приведение к заглавной первой букве для русского языка
        """
        def smart_capitalize(text):
            """Умное приведение к заглавной первой букве"""
            if not text:
                return text
            
            # Находим первую букву (пропускаем пробелы в начале)
            for i, char in enumerate(text):
                if char.isalpha():
                    # Делаем эту букву заглавной
                    return text[:i] + char.upper() + text[i+1:]
            
            # Если не нашли букв, возвращаем как есть
            return text
        
        if cluster_key in clusters:
            full_name = clusters[cluster_key]['name']
            
            # Пытаемся извлечь короткое название
            if "'" in full_name:
                # Формат: Образовательный кластер 'Педагогика'
                parts = full_name.split("'")
                if len(parts) > 1:
                    return smart_capitalize(parts[1])
            
            # Убираем длинные префиксы
            short_name = full_name
            prefixes = [
                "Образовательный кластер ",
                "Образовательно-производственный центр ",
                "Образовательно-производственный центр '",
                "Образовательный кластер '"
            ]
            
            for prefix in prefixes:
                if short_name.startswith(prefix):
                    short_name = short_name.replace(prefix, "")
                    # Убираем возможную закрывающую кавычку
                    if short_name.endswith("'"):
                        short_name = short_name[:-1]
                    break
            
            return smart_capitalize(short_name)
        else:
            return smart_capitalize(cluster_key)
# Показ детальной информации о кластере
label show_cluster_details(cluster_key):
    $ cluster_data = clusters[cluster_key]
    
    # Получаем путь к логотипу
    $ logo_path = get_cluster_logo(cluster_key)
    
    # Очищаем экран и показываем логотип на фоне
    scene
    
    if logo_path and renpy.loadable(logo_path):
        show expression logo_path as cluster_logo at center with dissolve
        pause 0.5
        show coach at left with moveinleft
        if player_gender == "guy":
            show guy at right with moveinright
        else:
            show girl at right with moveinright
    else:
        # Если логотипа нет, используем стандартный фон
        show bg
        show coach at left with dissolve
        if player_gender == "guy":
            show guy at right with dissolve
        else:
            show girl at right with dissolve
    
    coach "Отличный выбор! Давай подробнее рассмотрим [cluster_data['name']]."
    
    # Профессии
    coach "В этой области очень востребованы такие профессии как:"
    
    python:
        professions = cluster_data['professions']
        chunk_size = 4
        
        for i in range(0, len(professions), chunk_size):
            chunk = professions[i:i + chunk_size]
            renpy.say(coach, ", ".join(chunk))
            
            if i + chunk_size < len(professions):
                renpy.say(coach, "А также:")
    
    pause
    
    # Работодатели
    if cluster_data['employers']:
        coach "Из работодателей, готовых взять тебя:"
        
        python:
            employers = cluster_data['employers']
            chunk_size = 4
            
            for i in range(0, len(employers), chunk_size):
                chunk = employers[i:i + chunk_size]
                renpy.say(coach, ", ".join(chunk))
                
                if i + chunk_size < len(employers):
                    renpy.say(coach, "А также:")
    
    pause
    
    # Колледжи
    if cluster_data['colleges']:
        coach "Обучение на эти профессии можно пройти в:"
        
        python:
            colleges = cluster_data['colleges']
            chunk_size = 4
            
            for i in range(0, len(colleges), chunk_size):
                chunk = colleges[i:i + chunk_size]
                renpy.say(coach, ", ".join(chunk))
                
                if i + chunk_size < len(colleges):
                    renpy.say(coach, "А также:")
    
    pause
    
    # Базовая организация
    if cluster_data['base']:
        coach "Базовой организацией этого кластера является:"
        coach "[cluster_data['base']]"
    
    return