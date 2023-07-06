import maya.cmds as cmds

def simplify_mesh(mesh, simplify_type):
    # Упрощение сетки с сохранением формы
    cmds.select(mesh)
    if simplify_type == "Треугольники":
        cmds.polyTriangulate()
    elif simplify_type == "Квадраты":
        cmds.polyQuad()
    elif simplify_type == "Многоугольники":
        cmds.polySubdivideFacet()

def convert_triangles_to_quads(mesh):
    # Преобразование треугольников в квадраты
    cmds.select(mesh)
    cmds.polyTriangulate()
    cmds.polyQuad()

def preserve_edge_angles(mesh, angle_strength):
    # Сохранение углов ребер меша
    cmds.select(mesh)
    cmds.polySoftEdge(angle=angle_strength)

def retopology(mesh, target_polygon_count, simplify_type, smoothing_level, angle_strength, preserve_angles):
    # Создание дубликата меша
    duplicated_mesh = cmds.duplicate(mesh)[0]

    # Ретопология дублированного меша
    cmds.select(duplicated_mesh)
    cmds.polyRetopo(targetFaceCount=target_polygon_count)

    # Установка степени сглаживания
    cmds.select(duplicated_mesh)
    cmds.polySmooth(duplicated_mesh, dv=smoothing_level)

    # Упрощение сетки
    simplify_mesh(duplicated_mesh, simplify_type)

    # Сохранение углов ребер меша, если чекбокс активирован
    if preserve_angles:
        preserve_edge_angles(duplicated_mesh, angle_strength)

    return duplicated_mesh

def remove_triangles(*args):
    # Получить выбранный меш
    selected_meshes = cmds.ls(selection=True)
    if not selected_meshes:
        cmds.warning("Не выбран меш.")
        return

    # Преобразование треугольников в квадраты
    for mesh in selected_meshes:
        convert_triangles_to_quads(mesh)

    cmds.select(clear=True)

def apply_smooth_mesh(*args):
    # Получить выбранный меш
    selected_meshes = cmds.ls(selection=True)
    if not selected_meshes:
        cmds.warning("Не выбран меш.")
        return

    # Сглаживание сетки
    for mesh in selected_meshes:
        cmds.select(mesh)
        cmds.polySmooth(dv=1)

    cmds.select(clear=True)

def apply_hard_mesh(*args):
    # Получить выбранный меш
    selected_meshes = cmds.ls(selection=True)
    if not selected_meshes:
        cmds.warning("Не выбран меш.")
        return

    # Сохранение ребер сетки
    for mesh in selected_meshes:
        cmds.select(mesh)
        cmds.polySoftEdge(angle=0)

    cmds.select(clear=True)

def retopology_plugin(*args):
    # Получить выбранный меш
    selected_meshes = cmds.ls(selection=True)
    if not selected_meshes:
        cmds.warning("Не выбран меш для ретопологии.")
        return

    # Получить значения параметров ретопологии
    target_polygon_count = cmds.intSliderGrp("polygonCountSlider", query=True, value=True)
    simplify_type = cmds.optionMenuGrp("simplifyTypeOptionMenu", query=True, value=True)
    smoothing_level = cmds.floatSliderGrp("smoothingLevelSlider", query=True, value=True)
    angle_strength = cmds.floatSliderGrp("angleStrengthSlider", query=True, value=True)
    preserve_angles = cmds.checkBox("smoothEdgesCheckBox", query=True, value=True)

    # Ваш код для выполнения ретопологии выбранного меша здесь
    for mesh in selected_meshes:
        duplicated_mesh = retopology(mesh, target_polygon_count, simplify_type, smoothing_level, angle_strength, preserve_angles)
        cmds.hide(mesh)

    cmds.select(clear=True)

def create_button_on_panel():
    # Создание кнопки на панели
    if cmds.window("myWindow", exists=True):
        cmds.deleteUI("myWindow", window=True)

    cmds.window("myWindow", title="Моя Панель")
    cmds.columnLayout(adjustableColumn=True)

    # Добавление меню выбора формы упрощения сетки
    cmds.optionMenuGrp("simplifyTypeOptionMenu", label="Форма упрощения сетки")
    cmds.menuItem(label="Треугольники")
    cmds.menuItem(label="Квадраты")
    cmds.menuItem(label="Многоугольники")

    # Добавление кнопки для удаления треугольников
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="Убрать треугольники", command=remove_triangles, width=120)
    cmds.setParent("..")

    # Добавление чекбокса для активации сглаживания полигонов
    cmds.checkBox("smoothEdgesCheckBox", label="Сглаживание полигонов", value=False)

    # Добавление кнопок для применения сглаженных и жестких полигонов
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="Сглаженные полигоны", command=apply_smooth_mesh, width=120)
    cmds.button(label="Жесткие полигоны", command=apply_hard_mesh, width=120)
    cmds.setParent("..")

    # Добавление слайдера для настройки количества полигонов
    cmds.intSliderGrp("polygonCountSlider", label="Количество полигонов", field=True, min=100, max=10000, value=1000)

    # Добавление ползунка для настройки степени сглаживания
    cmds.floatSliderGrp("smoothingLevelSlider", label="Степень сглаживания", field=True, min=0, max=3, value=1)

    # Добавление ползунка для настройки силы диапазона углов
    cmds.floatSliderGrp("angleStrengthSlider", label="Сила диапазона углов", field=True, min=0, max=10, value=0)

    # Добавление кнопки для выполнения ретопологии
    cmds.button(label="Ретопология", command=retopology_plugin)

    cmds.setParent("..")
    cmds.showWindow("myWindow")

create_button_on_panel()
