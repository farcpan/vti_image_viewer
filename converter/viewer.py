import vtk
from vtk.util.numpy_support import numpy_to_vtk
import numpy as np

path = "./Data_Sep-24-2025_11-49-32.nrrd"
#path = "./output.nrrd"
#path = "./sample.nrrd"
#path = "./fool.nrrd"

# 1. NRRDファイルの読み込み
reader = vtk.vtkNrrdReader()
reader.SetFileName(path)  # 前回のコードで生成したNRRDファイル
reader.Update()

# 2. 3Dボリュームレンダリング
def setup_volume_rendering(reader):
    # ボリュームプロパティの設定（不透明度とカラー）
    volume_property = vtk.vtkVolumeProperty()
    color_func = vtk.vtkColorTransferFunction()
    color_func.AddRGBPoint(0, 0.0, 0.0, 0.0)    # 黒（背景）
    color_func.AddRGBPoint(128, 1.0, 1.0, 1.0)  # 白（楕円の輝度128）
    opacity_func = vtk.vtkPiecewiseFunction()
    opacity_func.AddPoint(0, 0.0)    # 背景は透明
    opacity_func.AddPoint(128, 1.0)  # 楕円は不透明
    volume_property.SetColor(color_func)
    volume_property.SetScalarOpacity(opacity_func)

    # ボリュームマッパーの設定
    volume_mapper = vtk.vtkSmartVolumeMapper()
    volume_mapper.SetInputConnection(reader.GetOutputPort())

    # ボリュームアクター
    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_property)

    # レンダラーの設定
    renderer = vtk.vtkRenderer()
    renderer.AddVolume(volume)
    renderer.SetBackground(0.1, 0.2, 0.3)  # 背景色（ダークブルー）

    return renderer

# 3. 2Dスライス表示
def setup_slice_view(reader, slice_index = 50):
    # 画像データの取得
    image_data = reader.GetOutput()

    # スライス表示用のリサンプラ
    reslice = vtk.vtkImageReslice()
    reslice.SetInputData(image_data)
    reslice.SetOutputDimensionality(2)  # 2Dスライス
    reslice.SetResliceAxesDirectionCosines(1, 0, 0, 0, 1, 0, 0, 0, 1)  # Z軸スライス
    reslice.SetResliceAxesOrigin(0, 0, slice_index)

    # カラーマッピング
    color_map = vtk.vtkImageMapToColors()
    color_table = vtk.vtkLookupTable()
    color_table.SetRange(0, 255)
    color_table.SetHueRange(0, 0)  # グレースケール
    color_table.SetSaturationRange(0, 0)
    color_table.SetValueRange(0, 1)
    color_table.Build()
    color_map.SetLookupTable(color_table)
    color_map.SetInputConnection(reslice.GetOutputPort())

    # 2Dアクター
    actor = vtk.vtkImageActor()
    actor.GetMapper().SetInputConnection(color_map.GetOutputPort())

    # レンダラーの設定
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.2, 0.3)

    return renderer, reslice

# 4. ウィンドウとインタラクションの設定
def setup_window(renderer):
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(800, 800)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    style = vtk.vtkInteractorStyleTrackballCamera()  # 3D回転/ズーム用
    interactor.SetInteractorStyle(style)

    render_window.Render()
    interactor.Start()

# 5. 実行（3Dボリュームレンダリング）
print("Rendering 3D volume...")
renderer_3d = setup_volume_rendering(reader)
setup_window(renderer_3d)

# 6. 実行（2Dスライス表示、オプション）
#print("Rendering 2D slice...")
#v = input()
#slice_index = int(v)
#print(f"index: {slice_index}")
#renderer_2d, reslice = setup_slice_view(reader, slice_index=slice_index)
#setup_window(renderer_2d)
