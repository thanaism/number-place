import pytest
import PySimpleGUI as sg


def test_progress_bar():
    layout = [
        [sg.Text("生成中…", font=('Courier', 20))],
        [sg.ProgressBar(1000, orientation="h", size=(40, 40), key="progbar")],
        # [sg.Cancel(font='Courier 20')],
    ]

    window = sg.Window("ナンプレメーカー", layout)
    for i in range(1000):
        # event, values = window.read(timeout=0)
        window.read(timeout=0)
        # if event == "Cancel" or event is None:
        #     break
        window["progbar"].update_bar(i + 1)

    window.close()


if __name__ == '__main__':
    parameter = '-sv'
    pytest.main([parameter, __file__])
