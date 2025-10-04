import numpy as np
import vtk


def main(filename, ext):
    # NRRDファイルの読み込み
    path = f"{filename}.{ext}"
    reader = vtk.vtkNrrdReader() if ext == "nrrd" else vtk.vtkXMLImageDataReader()
    reader.SetFileName(path)  # nrrd file name
    reader.Update()


    def setup_volume_rendering(reader):
        """
        3Dボリュームレンダリング
        """
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


    def setup_window(renderer):
        """
        ウィンドウ・カメラ操作設定
        """
        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)
        render_window.SetSize(800, 800)

        interactor = vtk.vtkRenderWindowInteractor()
        interactor.SetRenderWindow(render_window)
        style = vtk.vtkInteractorStyleTrackballCamera()  # 3D回転/ズーム用
        interactor.SetInteractorStyle(style)

        render_window.Render()
        interactor.Start()


    # 3Dボリュームレンダリング
    print("Rendering 3D volume...")
    renderer_3d = setup_volume_rendering(reader)
    setup_window(renderer_3d)


if __name__ == '__main__':
    print("Input the file name (without exention, ex. output): ")
    filename = input()
    print("Input the ext: nrrd or vti: ")
    ext = input()
    if ext != "nrrd" and ext != "vti":
        exit()

    main(filename=filename, ext=ext)
