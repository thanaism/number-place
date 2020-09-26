import PySimpleGUI as sg


def show_on_gui(digits, lines, draw_box_line):
    """
    GUIでGridを表示する

    Parameters
    ----------
    digits : str
        81文字の数字
    lines : str
        81文字の16進数
    """
    margin = 4
    CELL_SIZE = 50
    graph = sg.Graph(
        (CELL_SIZE * 9 + margin, CELL_SIZE * 9 + margin),
        (0, CELL_SIZE * 9 + margin),
        (CELL_SIZE * 9 + margin, 0),
        key="_GRAPH_",
        change_submits=True,
    )

    def btn(str):
        return sg.Button(str, font='Courier 30')

    layout = [
        [graph],
        [btn('Exit')],  # btn('Refresh')],
    ]

    def linedraw(index, hex):
        for bit in range(4):
            if hex & 1 << bit:
                row = index // 9
                col = index % 9
                line_color = '#cccccc' if draw_box_line else '#000000'
                line_width = 7 if draw_box_line else 4
                h = line_width / 2
                if bit == 0:
                    bgn = (
                        CELL_SIZE * (col + 0) - h + margin / 2,
                        CELL_SIZE * (row + 0) + margin / 2,
                    )
                    end = (
                        CELL_SIZE * (col + 1) + h + margin / 2,
                        CELL_SIZE * (row + 0) + margin / 2,
                    )
                if bit == 1:
                    bgn = (
                        CELL_SIZE * (col + 1) + margin / 2,
                        CELL_SIZE * (row + 0) - h + margin / 2,
                    )
                    end = (
                        CELL_SIZE * (col + 1) + margin / 2,
                        CELL_SIZE * (row + 1) + h + margin / 2,
                    )
                if bit == 2:
                    bgn = (
                        CELL_SIZE * (col + 1) + h + margin / 2,
                        CELL_SIZE * (row + 1) + margin / 2,
                    )
                    end = (
                        CELL_SIZE * (col + 0) - h + margin / 2,
                        CELL_SIZE * (row + 1) + margin / 2,
                    )
                if bit == 3:
                    bgn = (
                        CELL_SIZE * (col + 0) + margin / 2,
                        CELL_SIZE * (row + 1) + h + margin / 2,
                    )
                    end = (
                        CELL_SIZE * (col + 0) + margin / 2,
                        CELL_SIZE * (row + 0) - h + margin / 2,
                    )
                graph.draw_line(
                    bgn,
                    end,
                    width=line_width,
                    color=line_color,
                )

    window = sg.Window("Grid's information", layout, finalize=True)
    # g = window.FindElement("_GRAPH_")
    label = [None] * 81
    cell = [None] * 81
    for row in range(9):
        for col in range(9):
            index = row * 9 + col
            linedraw(index, eval('0x' + lines[index]))
            cell[index] = graph.draw_rectangle(
                (col * CELL_SIZE + margin / 2, row * CELL_SIZE + margin / 2),
                (
                    col * CELL_SIZE + CELL_SIZE + margin / 2,
                    row * CELL_SIZE + CELL_SIZE + margin / 2,
                ),
                # line_color='black',
                line_width=0.25
                # fill_color='white',
            )
            graph.DrawText(
                text=str(index),
                location=(
                    col * CELL_SIZE + 12 + margin / 2,
                    row * CELL_SIZE + 10 + margin / 2,
                ),
                font='Courier 13',
            )
            label[index] = graph.DrawText(
                text=digits[index],
                location=(
                    col * CELL_SIZE + 25 + margin / 2,
                    row * CELL_SIZE + 30 + margin / 2,
                ),
                font=('Courier', 40),
            )
    for i in range(81):
        graph.bring_figure_to_front(cell[i])

    graph.draw_rectangle(
        (0, 0),
        (CELL_SIZE * 9 + margin / 2, CELL_SIZE * 9 + margin / 2),
        line_width=margin,
    )
    if draw_box_line:
        graph.draw_rectangle(
            (CELL_SIZE * 3 + margin / 2, 0 + margin / 2),
            (CELL_SIZE * 6 + margin / 2, CELL_SIZE * 9 + margin / 2),
            line_width=2,
        )
        graph.draw_rectangle(
            (0, CELL_SIZE * 3),
            (CELL_SIZE * 9 + margin / 2, CELL_SIZE * 6 + margin / 2),
            line_width=2,
        )

    while True:  # Event Loop
        event, values = window.Read()
        # print(event, values)
        # position = values['_GRAPH_']
        # if event == '_GRAPH_':
        #     row_clicked = position[1] // CELL_SIZE
        #     col_clicked = position[0] // CELL_SIZE
        #     print(f'cell clicked: {row_clicked, col_clicked}')
        #     graph.delete_figure(cell[row_clicked * 9 + col_clicked])
        # if event == 'Refresh':
        #     for i in range(81):
        #         graph.delete_figure(cell[i])
        #     for row in range(9):
        #         for col in range(9):
        #             cell[row * 9 + col] = graph.DrawText(
        #                 text='A',
        #                 location=(col * CELL_SIZE + 30, row * CELL_SIZE + 30),
        #                 font='Courier 40',
        #             )
        if event is None or event == 'Exit':
            break

    window.Close()
