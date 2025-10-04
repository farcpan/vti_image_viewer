import numpy as np
import nrrd
import vtk
from vtk.util.numpy_support import numpy_to_vtk


def main(user_input):
    """
    指定した名称のnrrdファイルをvti形式に変換する
    """
    
    # input/output path
    input_path = f"{user_input}.nrrd"
    output_path = f"{user_input}.vti"

    """
    1. nrrd読み込み
    """
    data, header = nrrd.read(input_path)
    print("NRRD shape:", data.shape)

    ## nrrdファイル内でspacingとoriginが定義されている場合は取得する。取得できない場合は第2引数の初期値を採用する
    spacings = header.get('spacings', [1.0,1.0,1.0])
    origin = header.get('space origin', [0.0,0.0,0.0])

    # nrrdの座標系情報
    ## 基本的には left-posterior-superior を想定する
    space = header.get('space', 'unknown')

    """
    2. nrrdの座標系をvtkに合わせる
    - vtkの右手系XYZに変換する場合、LPS -> RAS は X, Y を反転
    - Zは上向きで共通
    """
    if space.lower() in ['left-posterior-superior', 'lps']:
        print("Applying LPS -> RAS conversion...")
        data = np.flip(data, axis=(2,1))  # X, Y 軸反転
        origin[0] = -origin[0]
        origin[1] = -origin[1]

    """
    3. vtk ImageData作成
    """
    image_data = vtk.vtkImageData()
    dims = data.shape  # (z, y, x)
    image_data.SetDimensions(dims[2], dims[1], dims[0])
    image_data.SetSpacing(spacings[2], spacings[1], spacings[0])
    image_data.SetOrigin(origin[0], origin[1], origin[2])

    """
    4. データをvtk配列に変換
    """
    flat_data = data.ravel(order='C')
    vtk_array = numpy_to_vtk(flat_data, deep=True, array_type=vtk.VTK_FLOAT)
    vtk_array.SetName("Scalars")
    image_data.GetPointData().SetScalars(vtk_array)

    """
    5. .vtiとして保存
    """
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName(output_path)
    writer.SetInputData(image_data)
    writer.Write()

    print("NRRD -> VTI conversion done with coordinate system preserved!")


if __name__ == '__main__':
    print("Input the file name (without exention, ex. output): ")
    user_input = input()
    main(user_input=user_input)
