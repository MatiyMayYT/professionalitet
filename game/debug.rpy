# debug.rpy — файл для отладки и тестирования кластеров

init python:
    # Функция для отладки - позволяет выбрать любой кластер
    def debug_select_cluster():
        """
        Позволяет выбрать любой кластер для тестирования
        Возвращает ключ выбранного кластера
        """
        # Создаем список кластеров для выбора
        cluster_choices = []
        
        for cluster_key, cluster_data in clusters.items():
            short_name = get_cluster_short_name(cluster_key)
            cluster_choices.append((short_name, cluster_key))
        
        # Сортируем по алфавиту для удобства
        cluster_choices.sort(key=lambda x: x[0])
        
        # Добавляем вариант для выхода
        cluster_choices.append(("Вернуться к обычному тесту", "back_to_test"))
        
        # Создаем меню выбора
        menu_items = []
        for display_name, cluster_key in cluster_choices:
            menu_items.append((display_name, cluster_key))
        
        return renpy.display_menu(menu_items)

# Метка для отладочного режима
label debug_mode:
    scene bg
    show coach at left with dissolve
    
    coach "Режим отладки активирован!"
    coach "Здесь ты можешь выбрать любой кластер для просмотра."
    coach "Это полезно для тестирования и отладки игры."
    
    # Показываем игрока
    if player_gender == "guy":
        show guy at right with dissolve
    else:
        show girl at right with dissolve
    
    # Основной цикл отладки
    label debug_loop:
        $ chosen_cluster = debug_select_cluster()
        
        if chosen_cluster == "back_to_test":
            coach "Возвращаюсь к обычному тесту..."
            jump start_test
        else:
            # Показываем выбранный кластер
            call show_cluster_details(chosen_cluster)
            
            # Спрашиваем, хочет ли продолжить отладку
            coach "Хочешь посмотреть другой кластер или завершить отладку?"
            
            menu:
                "Посмотреть другой кластер":
                    jump debug_loop
                "Вернуться к обычному тесту":
                    coach "Хорошо, возвращаюсь к обычному тесту..."
                    jump start_test
                "Завершить отладку и выйти":
                    coach "Завершаю отладку. До встречи!"
                    jump end_conversation

# Краткая версия отладки (без лишних вопросов)
label quick_debug:
    scene bg
    show coach at left with dissolve
    
    coach "Быстрая отладка. Выбери кластер для просмотра:"
    
    # Создаем меню выбора кластера
    python:
        cluster_choices = []
        for cluster_key, cluster_data in clusters.items():
            short_name = get_cluster_short_name(cluster_key)
            cluster_choices.append((f"{short_name} ({cluster_data['name']})", cluster_key))
        
        # Сортируем
        cluster_choices.sort(key=lambda x: x[0])
        
        # Выбор
        chosen_cluster = renpy.display_menu(cluster_choices)
    
    # Показываем выбранный кластер
    call show_cluster_details(chosen_cluster)
    
    # Сразу завершаем
    coach "Отладка завершена. Возвращаюсь к началу игры."
    jump start