import networkx as nx
import matplotlib.pyplot as plt

# Исходный автомат на основе графа с изображения
automat = {
    'X': {'i': 'I', 'j': 'K'},
    'Y': {'n': 'X', 'm': 'I'},
    'Z': {'n': 'X', 'm': 'K'},
    'I': {'j': 'J', 'n': 'L'},
    'J': {'m': 'X', 'k': 'N'},
    'K': {'j': 'J', 'n': 'M'},
    'L': {'m': 'J', '!': 'N', '/':'L'},
    'M':{'m': 'J', '!': 'N', '/':'M'},
    'N': {}
}
start_state = 'X'
final_states = {'N'}  # Конечные состояния согласно графу

# Функция для отображения графа автомата
def draw_automat(automat, title="Automat Graph"):
    G = nx.DiGraph()
    for state, transitions in automat.items():
        for symbol, next_state in transitions.items():
            G.add_edge(state, next_state, label=symbol)
    
    pos = nx.spring_layout(G)
    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.title(title)
    plt.show()

# 1. Отображение исходного графа
draw_automat(automat, "Initial Automat")

# Функция для устранения недостижимых состояний
def remove_unreachable_states(automat, start_state):
    reachable = set([start_state])  # Шаг 1: начальное состояние добавляем в список достижимых
    queue = [start_state]  # очередь для обхода состояний

    # Шаг 2 и Шаг 3: расширение достижимых состояний, пока список не перестанет меняться
    while queue:
        state = queue.pop(0)
        for next_state in automat.get(state, {}).values():
            if next_state not in reachable:
                reachable.add(next_state)
                queue.append(next_state)

    # Шаг 4 и Шаг 5: удаление недостижимых состояний и соответствующих переходов
    reachable_automat = {state: {symbol: next_state for symbol, next_state in transitions.items() if next_state in reachable}
                           for state, transitions in automat.items() if state in reachable}
    
    return reachable_automat

# Применение функции устранения недостижимых состояний
automat = remove_unreachable_states(automat, start_state)
draw_automat(automat, "Automat without Unreachable States")

# Функция для минимизации автомата (объединения эквивалентных состояний)
def min_automat(automat, final_states):
    # Шаг 1: Начальное разбиение R(0) на финальные и нефинальные состояния
    partition = [set(final_states), set(automat.keys()) - set(final_states)]
    
    def get_partition_index(state, partition):
        """Вспомогательная функция для определения индекса подмножества, к которому принадлежит состояние"""
        for i, group in enumerate(partition):
            if state in group:
                return i
        return -1

    # Шаг 2 и Шаг 3: Разбиение на классы эквивалентности до тех пор, пока разбиение не стабилизируется
    while True:
        new_partition = []
        for group in partition:
            subgroups = {}
            for state in group:
                # Формируем "подпись" для состояния — переходы в эквивалентные состояния
                signature = tuple((symbol, get_partition_index(automat[state].get(symbol), partition)) for symbol in automat[state])
                if signature not in subgroups:
                    subgroups[signature] = set()
                subgroups[signature].add(state)
            new_partition.extend(subgroups.values())
        
        if new_partition == partition:
            break
        partition = new_partition

    # Шаг 4: Создание новой структуры для минимизированного автомата
    minimized_automat = {}
    state_mapping = {}
    
    # Переименовываем группы состояний, присваивая каждой группе уникальное имя
    for i, group in enumerate(partition):
        representative = next(iter(group))  # Выбираем представителя группы
        for state in group:
            state_mapping[state] = f"Q{i}"  # Переименовываем каждое состояние в группе как Q0, Q1, и т.д.

    # Создаем минимизированный автомат, используя переименованные состояния
    for state, transitions in automat.items():
        new_state = state_mapping[state]
        minimized_automat[new_state] = {}
        
        for symbol, next_state in transitions.items():
            new_next_state = state_mapping[next_state]  # Переименовываем состояния переходов
            minimized_automat[new_state][symbol] = new_next_state

    return minimized_automat

# Применение функции минимизации автомата
automat = min_automat(automat, final_states)
draw_automat(automat, "Minimized Automat")
